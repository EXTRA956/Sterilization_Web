-- Enums
CREATE TABLE enum_comment_types (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE enum_packaging (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE enum_set_state (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- Data Tables
CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    type_id INTEGER NOT NULL,
    FOREIGN KEY (type_id) REFERENCES enum_comment_types(id),
    content TEXT NOT NULL,
    author TEXT NOT NULL,
    date_time TEXT NOT NULL
);

CREATE TABLE sets (
    serial_number INTEGER PRIMARY KEY,
    active_comment_id INTEGER,
    FOREIGN KEY (active_comment_id) REFERENCES comments(id),
    packaging_id INTEGER,
    FOREIGN KEY (packaging_id) REFERENCES enum_packaging(id),
    name TEXT NOT NULL,
    customer TEXT NOT NULL
);

CREATE TABLE set_states (
    id INTEGER PRIMARY KEY,
    set_id INTEGER NOT NULL,
    FOREIGN KEY (set_id) REFERENCES sets(serial_number),
    state_id INTEGER,
    FOREIGN KEY (state_id) REFERENCES enum_set_state(id),
    comment_id INTEGER,
    FOREIGN KEY (comment_id) REFERENCES comments(id),
    user TEXT NOT NULL,
    date TEXT NOT NULL
);

CREATE TABLE instruments (
    id INTEGER PRIMARY KEY,
    set_id INTEGER NOT NULL,
    FOREIGN KEY (set_id) REFERENCES sets(serial_number),
    comment_id INTEGER,
    FOREIGN KEY (comment_id) REFERENCES comments(id),
    remaining_uses INTEGER
);