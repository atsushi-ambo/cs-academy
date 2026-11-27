PRAGMA application_id = 1129529665;

CREATE TABLE schema_version (version INTEGER PRIMARY KEY);

CREATE TABLE stages (
    number INTEGER PRIMARY KEY,
    title TEXT NOT NULL
);
CREATE TABLE modules (
    id TEXT PRIMARY KEY,
    stage INTEGER NOT NULL REFERENCES stages(number),
    title TEXT NOT NULL
);
CREATE TABLE units (
    id TEXT PRIMARY KEY,
    module_id TEXT NOT NULL REFERENCES modules(id),
    title TEXT NOT NULL,
    version INTEGER NOT NULL,
    status TEXT NOT NULL
);
CREATE TABLE steps (
    id TEXT PRIMARY KEY,
    unit_id TEXT NOT NULL REFERENCES units(id),
    position INTEGER NOT NULL,
    kind TEXT NOT NULL,
    definition TEXT NOT NULL
);
CREATE TABLE review_cards (
    id TEXT PRIMARY KEY,
    unit_id TEXT NOT NULL REFERENCES units(id),
    definition TEXT NOT NULL,
    due_day TEXT,
    last_day TEXT,
    stability REAL,
    difficulty REAL,
    CHECK ((last_day IS NULL AND stability IS NULL AND difficulty IS NULL)
        OR (last_day IS NOT NULL AND due_day IS NOT NULL AND stability > 0
            AND difficulty BETWEEN 1 AND 10))
);
CREATE INDEX review_due ON review_cards(due_day);
