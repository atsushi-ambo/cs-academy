ALTER TABLE review_cards ADD COLUMN answer_hash TEXT;
ALTER TABLE review_cards ADD COLUMN revision INTEGER NOT NULL DEFAULT 0;

ALTER TABLE review_logs RENAME TO previous_review_logs;
CREATE TABLE review_logs (
    id INTEGER PRIMARY KEY,
    card_id TEXT NOT NULL REFERENCES review_cards(id),
    day TEXT NOT NULL,
    event TEXT NOT NULL CHECK (event IN ('practice', 'due', 'retry')),
    grade INTEGER NOT NULL CHECK (grade BETWEEN 1 AND 4),
    stability REAL NOT NULL,
    difficulty REAL NOT NULL,
    revision INTEGER NOT NULL DEFAULT 0,
    UNIQUE (card_id, day, event, revision)
);
INSERT INTO review_logs (id, card_id, day, event, grade, stability, difficulty)
SELECT id, card_id, day, event, grade, stability, difficulty FROM previous_review_logs;
DROP TABLE previous_review_logs;
CREATE INDEX review_logs_day ON review_logs(day, event);
