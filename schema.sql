-- Enums
CREATE TABLE IF NOT EXISTS enum_comment_type (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS enum_packaging (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS enum_set_state (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- Data Tables
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    user TEXT NOT NULL,
    date_time TEXT NOT NULL,
    type_id INTEGER NOT NULL,
    FOREIGN KEY (type_id) REFERENCES enum_comment_types(id)
);

CREATE TABLE IF NOT EXISTS sets (
    serial_number INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    customer TEXT NOT NULL,
    active_comment_id INTEGER,
    packaging_id INTEGER,
    FOREIGN KEY (active_comment_id) REFERENCES comments(id),
    FOREIGN KEY (packaging_id) REFERENCES enum_packaging(id)
);

CREATE TABLE IF NOT EXISTS set_states (
    id INTEGER PRIMARY KEY,
    user TEXT NOT NULL,
    date_time TEXT NOT NULL,
    state_id INTEGER,
    comment_id INTEGER,
    set_id INTEGER NOT NULL,
    FOREIGN KEY (set_id) REFERENCES sets(serial_number),
    FOREIGN KEY (state_id) REFERENCES enum_set_state(id),
    FOREIGN KEY (comment_id) REFERENCES comments(id)
);

CREATE TABLE IF NOT EXISTS instruments (
    id INTEGER PRIMARY KEY,
    remaining_uses INTEGER,
    set_id INTEGER NOT NULL,
    comment_id INTEGER,
    FOREIGN KEY (set_id) REFERENCES sets(serial_number),
    FOREIGN KEY (comment_id) REFERENCES comments(id)
);