CREATE TABLE IF NOT EXISTS Transactions (
    hash TEXT PRIMARY KEY,
    block_no INTEGER,
    amount TEXT,
    ts DATETIME
);
