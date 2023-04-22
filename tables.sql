CREATE TABLE IF NOT EXISTS users
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        admin BOOLEAN DEFAULT TRUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        hash TEXT NOT NULL,
        name TEXT,
        joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
    );

-- Codes (id, admin, code, email, validity)
CREATE TABLE IF NOT EXISTS codes
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        admin BOOLEAN DEFAULT TRUE NOT NULL,
        code TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        valid DATE
    );