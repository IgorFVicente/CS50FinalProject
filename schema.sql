DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS records;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    min_study_time INTEGER DEFAULT 60,
    streak TEXT DEFAULT '0'
);

CREATE TABLE records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT (datetime('now', 'localtime')),
    hours TEXT NOT NULL,
    minutes TEXT NOT NULL,
    seconds TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);