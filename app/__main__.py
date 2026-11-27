import argparse
import os
import sqlite3
import sys
from pathlib import Path

from .content import ROOT, ContentError, load_catalog
from .learning import Learning
from .server import HOST, PORT, Server
from .storage import BACKUP_DB, Store


def main():
    parser = argparse.ArgumentParser(prog="cs-academy")
    parser.add_argument("command", choices=("run", "validate", "backup", "restore"))
    parser.add_argument("backup_id", nargs="?")
    args = parser.parse_args()
    if (args.command == "restore") != (args.backup_id is not None):
        parser.error("Provide a backup ID only for restore")
    try:
        catalog = load_catalog()
        if args.command == "validate":
            print(f"Content valid ({len(catalog.play)} playable units, "
                  f"{len(catalog.units)} catalog units, {len(catalog.steps)} steps).")
            return 0
        backups = Path(os.environ.get("CS_ACADEMY_BACKUP_DIR", "~/cs-academy-backups"))
        store = Store(ROOT / "data" / BACKUP_DB, backups, catalog)
        if args.command == "run":
            with Server(Learning(store)) as server:
                store.initialize()
                print(f"CS Academy is ready at http://{HOST}:{PORT}", flush=True)
                server.serve_forever()
        elif args.command == "backup":
            print(store.backups / store.backup())
        else:
            previous = store.restore(args.backup_id)
            print(f"Restored {args.backup_id}.")
            if previous:
                print(f"Previous state saved as {previous}.")
    except KeyboardInterrupt:
        return 0
    except (ContentError, OSError, ValueError, sqlite3.Error) as error:
        print(f"CS Academy: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
