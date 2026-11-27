import fcntl
import json
import os
import re
import shutil
import sqlite3
import stat
import tempfile
from contextlib import closing, contextmanager
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from .content import ROOT

APP_ID = 1129529665
MIGRATIONS = sorted(Path(__file__).with_name("migrations").glob("[0-9][0-9][0-9]_*.sql"))
BACKUP_ID = re.compile(r"[0-9]{8}T[0-9]{6}-[a-f0-9]{12}")
BACKUP_DB = "academy.sqlite3"


def private_directory(path):
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    if path.is_symlink() or not path.is_dir() or stat.S_IMODE(path.stat().st_mode) != 0o700:
        raise ValueError(f"Use a private directory with mode 0700: {path}")


def connect(path, *, readonly=False):
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise ValueError("The database must be a regular file")
    uri = f"{path.absolute().as_uri()}?mode={'ro' if readonly else 'rwc'}"
    db = sqlite3.connect(uri, uri=True, timeout=5)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("PRAGMA trusted_schema = OFF")
    return db


def migrate(db):
    app_id = db.execute("PRAGMA application_id").fetchone()[0]
    tables = db.execute("SELECT name FROM sqlite_schema WHERE type = 'table'").fetchall()
    if app_id != APP_ID and (app_id != 0 or tables):
        raise ValueError("The database does not belong to CS Academy")
    applied = []
    if app_id == APP_ID:
        applied = [row[0] for row in db.execute(
            "SELECT version FROM schema_version ORDER BY version"
        )]
    versions = [int(path.name[:3]) for path in MIGRATIONS]
    if versions != list(range(1, len(versions) + 1)) or applied != versions[:len(applied)]:
        raise ValueError("Unsupported CS Academy database schema")

    for version, path in zip(versions[len(applied):], MIGRATIONS[len(applied):], strict=True):
        script = path.read_text(encoding="utf-8")
        db.executescript(
            f"BEGIN IMMEDIATE;\n{script}\nINSERT INTO schema_version VALUES ({version});\nCOMMIT;"
        )


def import_catalog(db, catalog):
    db.executemany(
        "INSERT INTO stages VALUES (?, ?) ON CONFLICT(number) DO UPDATE SET title=excluded.title",
        catalog.stages.items(),
    )
    db.executemany(
        """INSERT INTO modules VALUES (?, ?, ?) ON CONFLICT(id) DO UPDATE SET
           stage=excluded.stage, title=excluded.title""",
        ((key, obj["stage"], obj["title"]) for key, obj in catalog.modules.items()),
    )
    db.executemany(
        """INSERT INTO units VALUES (?, ?, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET
           module_id=excluded.module_id, title=excluded.title, version=excluded.version,
           status=excluded.status""",
        ((key, obj["module_id"], obj["title"], obj["version"], obj["status"])
         for key, obj in catalog.units.items()),
    )
    db.executemany(
        """INSERT INTO steps VALUES (?, ?, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET
           position=excluded.position, kind=excluded.kind, definition=excluded.definition""",
        ((key, key.split("/")[0], position, obj["type"], json.dumps(obj, ensure_ascii=False))
         for position, (key, obj) in enumerate(catalog.steps.items())),
    )
    db.executemany(
        """INSERT INTO review_cards (id, unit_id, definition) VALUES (?, ?, ?)
           ON CONFLICT(id) DO UPDATE SET definition=excluded.definition""",
        ((key, obj["unit"], json.dumps(obj, ensure_ascii=False))
         for key, obj in catalog.cards.items()),
    )


class Store:
    def __init__(self, database, backups, catalog):
        self.path = Path(database).absolute()
        self.backups = Path(backups).expanduser().absolute()
        if self.backups.resolve().is_relative_to(ROOT):
            raise ValueError("Backups must be outside the repository")
        self.catalog = catalog

    @contextmanager
    def locked(self):
        private_directory(self.path.parent)
        # Restore and request transactions share a process-independent lock.
        lock = os.open(self.path.parent / ".academy.lock",
                       os.O_CREAT | os.O_NOFOLLOW | os.O_RDONLY, 0o600)
        try:
            fcntl.flock(lock, fcntl.LOCK_EX)
            yield
        finally:
            os.close(lock)

    @contextmanager
    def transaction(self):
        with self.locked(), closing(connect(self.path)) as db, db:
            yield db

    def initialize(self):
        with self.transaction() as db:
            migrate(db)
            self.path.chmod(0o600)
            import_catalog(db, self.catalog)

    def backups_list(self):
        if not self.backups.exists():
            return []
        private_directory(self.backups)
        return sorted(
            (entry.name for entry in self.backups.iterdir()
             if BACKUP_ID.fullmatch(entry.name) and entry.is_dir() and not entry.is_symlink()
             and (entry / BACKUP_DB).is_file() and not (entry / BACKUP_DB).is_symlink()),
            reverse=True,
        )

    def snapshot(self):
        private_directory(self.backups)
        stamp = datetime.now().strftime("%Y%m%dT%H%M%S")
        identifier = f"{stamp}-{uuid4().hex[:12]}"
        folder = Path(tempfile.mkdtemp(prefix=".pending-", dir=self.backups))
        try:
            with closing(connect(self.path, readonly=True)) as source:
                with closing(connect(folder / BACKUP_DB)) as target:
                    source.backup(target)
            (folder / BACKUP_DB).chmod(0o600)
            folder.rename(self.backups / identifier)
        finally:
            if folder.exists():
                shutil.rmtree(folder)
        return identifier

    def backup(self):
        with self.locked():
            return self.snapshot()

    def restore(self, identifier):
        with self.locked():
            if identifier not in self.backups_list():
                raise ValueError("Backup ID was not found")
            origin = self.backups / identifier / BACKUP_DB
            with tempfile.TemporaryDirectory(dir=self.path.parent) as temporary:
                staged = Path(temporary) / BACKUP_DB
                with closing(connect(origin, readonly=True)) as source:
                    if source.execute("PRAGMA application_id").fetchone()[0] != APP_ID:
                        raise ValueError("The backup does not belong to CS Academy")
                    if source.execute("PRAGMA quick_check").fetchone()[0] != "ok":
                        raise ValueError("The backup failed SQLite integrity checks")
                    with closing(connect(staged)) as candidate:
                        source.backup(candidate)
                with closing(connect(staged)) as candidate:
                    migrate(candidate)
                    with candidate:
                        import_catalog(candidate, self.catalog)
                        if candidate.execute("PRAGMA foreign_key_check").fetchone():
                            raise ValueError("The backup has invalid references")
                    previous = self.snapshot() if self.path.exists() else None
                    with closing(connect(self.path)) as target:
                        candidate.backup(target)
                    self.path.chmod(0o600)
            return previous
