CREATE TABLE attempts (
    id INTEGER PRIMARY KEY,
    unit_id TEXT NOT NULL REFERENCES units(id),
    step_id TEXT NOT NULL,
    unit_version INTEGER NOT NULL,
    day TEXT NOT NULL,
    action TEXT NOT NULL,
    result TEXT NOT NULL,
    answer INTEGER
);
CREATE INDEX attempts_by_action ON attempts(step_id, unit_version, action);
CREATE TABLE step_progress (
    step_id TEXT NOT NULL REFERENCES steps(id),
    unit_version INTEGER NOT NULL,
    complete INTEGER NOT NULL DEFAULT 0 CHECK (complete IN (0, 1)),
    hints INTEGER NOT NULL DEFAULT 0 CHECK (hints BETWEEN 0 AND 3),
    failures INTEGER NOT NULL DEFAULT 0 CHECK (failures >= 0),
    PRIMARY KEY (step_id, unit_version)
);
CREATE TABLE review_logs (
    id INTEGER PRIMARY KEY,
    card_id TEXT NOT NULL REFERENCES review_cards(id),
    day TEXT NOT NULL,
    event TEXT NOT NULL CHECK (event IN ('practice', 'due', 'retry')),
    grade INTEGER NOT NULL CHECK (grade BETWEEN 1 AND 4),
    stability REAL NOT NULL,
    difficulty REAL NOT NULL,
    UNIQUE (card_id, day, event)
);
CREATE INDEX review_logs_day ON review_logs(day, event);
CREATE TABLE xp_events (
    event_key TEXT PRIMARY KEY,
    day TEXT NOT NULL,
    points INTEGER NOT NULL CHECK (points > 0)
);
CREATE TABLE daily_quest (
    day TEXT NOT NULL,
    kind TEXT NOT NULL CHECK (kind IN ('step', 'code', 'review')),
    progress INTEGER NOT NULL DEFAULT 0 CHECK (progress >= 0),
    PRIMARY KEY (day, kind)
);
CREATE TABLE placement_results (
    id INTEGER PRIMARY KEY,
    unit_id TEXT NOT NULL REFERENCES units(id),
    unit_version INTEGER NOT NULL,
    day TEXT NOT NULL,
    correct INTEGER NOT NULL,
    questions INTEGER NOT NULL,
    code_passed INTEGER NOT NULL CHECK (code_passed IN (0, 1)),
    passed INTEGER NOT NULL CHECK (passed IN (0, 1))
);
CREATE TABLE unit_skips (
    unit_id TEXT NOT NULL REFERENCES units(id),
    unit_version INTEGER NOT NULL,
    day TEXT NOT NULL,
    recommend INTEGER NOT NULL DEFAULT 0 CHECK (recommend IN (0, 1)),
    PRIMARY KEY (unit_id, unit_version)
);
