CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        admin BOOLEAN DEFAULT TRUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        hash TEXT NOT NULL,
        name TEXT,
        joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
    );

-- Codes (id, admin, code, email, validity)
CREATE TABLE IF NOT EXISTS codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        admin BOOLEAN DEFAULT TRUE NOT NULL,
        code TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        valid DATE
    );

-- Latest version doesn't have time_updt
CREATE TABLE IF NOT EXISTS journals (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        user_id INTEGER NOT NULL,
        resp_id INTEGER,
        content TEXT,
        response TEXT,
        time_crte TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
        time_updt TIMESTAMP,
        time_resp TIMESTAMP, 
        submitted BOOLEAN DEFAULT 0,
        resp_draft BOOLEAN DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (resp_id) REFERENCES users(id)
);