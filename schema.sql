DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS records;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    min_study_time INTEGER DEFAULT 60,
    streak TEXT DEFAULT '0',
    last_day TEXT
);

CREATE TABLE records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT (datetime('now', 'localtime')),
    created_date TEXT NOT NULL DEFAULT (date('now', 'localtime')),
    created_time TEXT NOT NULL DEFAULT (time('now', 'localtime')),
    hours TEXT NOT NULL,
    minutes TEXT NOT NULL,
    seconds TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);