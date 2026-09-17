import sqlite3
from datetime import datetime
from models import EnumNoteType, EnumPackaging, EnumSetState, Comment, Instrument, Set, SetState

def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect("sterilization.db")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row
    return connection

# Seeding Funcitons
def seed_enum_table(cursor: sqlite3.Cursor, table_name: str, enum_class: EnumNoteType | EnumPackaging | EnumSetState) -> None:
    for member in enum_class:
        cursor.execute(
            f"INSERT OR IGNORE INTO {table_name} (id, name) VALUES (?, ?)", 
            (member.value, member.name)
        )

def seed_all_enum_tables(cursor: sqlite3.Cursor) -> None:
    seed_enum_table(cursor, "enum_note_type", EnumNoteType)
    seed_enum_table(cursor, "enum_packaging", EnumPackaging)
    seed_enum_table(cursor, "enum_set_state", EnumSetState)

# Insert Functions
def insert_comment(cursor: sqlite3.Cursor, comment: Comment) -> int:
    cursor.execute(
        f"INSERT INTO comments (content, user, date_time) VALUES (?, ?, ?)",
        (comment.content, comment.user, comment.date_time.isoformat())
    )

    comment_id = cursor.lastrowid

    # Intentional bypass of frozen=true. data_base_id is ease of use only, doesnt need immutability for an audit.
    object.__setattr__(comment, "data_base_id", comment_id)

    return comment_id

def insert_instrument(cursor: sqlite3.Cursor, instrument: Instrument, set_id : int) -> int:
    note_type_id = None
    if instrument.note_type is not None:
        note_type_id = instrument.note_type.value

    cursor.execute(
        f"INSERT INTO instruments (name, remaining_uses, note_content, set_id, note_type_id) VALUES (?, ?, ?, ?, ?)",
        (instrument.name, instrument.remaining_uses,  instrument.note_content, set_id, note_type_id)
    )

    instrument_id = cursor.lastrowid
    instrument.data_base_id = instrument_id
    
    return instrument_id

def insert_set(cursor: sqlite3.Cursor, set : Set) -> None:
    comment_id = None
    if set.active_comment is not None:
        if set.active_comment.data_base_id is None:
            comment_id = insert_comment(cursor, set.comment)
        else:
            comment_id = set.active_comment.data_base_id

    cursor.execute(
        f"INSERT INTO sets (serial_number, name, customer, active_comment_id, packaging_id) VALUES (?, ?, ?, ?, ?)",
        (set.serial_number, set.name, set.customer, comment_id, set.packaging.value)
    )

def insert_set_state(cursor: sqlite3.Cursor, set_state : SetState, set_id : int) -> int:
    comment_id = None
    if set_state.comment is not None:
        if set_state.comment.data_base_id is None:
            comment_id = insert_comment(cursor, set_state.comment)
        else:
            comment_id = set_state.comment.data_base_id

    cursor.execute(
        f"INSERT INTO set_states (user, date_time, state_id, comment_id, set_id) VALUES (?, ?, ?, ?, ?)",
        (set_state.user, set_state.date_time.isoformat(), set_state.state.value, comment_id, set_id)
    )

    set_state_id = cursor.lastrowid

     # Intentional bypass of frozen=true. data_base_id is ease of use only, doesnt need immutability for an audit.
    object.__setattr__(set_state, "data_base_id", set_state_id)

    return set_state_id

# Get Functions
def get_comment(cursor: sqlite3.Cursor, comment_id: int) -> Comment | None:
    cursor.execute(
        "SELECT user, content, date_time FROM comments WHERE id = ?",
        (comment_id,)
    )

    data = cursor.fetchone()

    if data is None:
        return None

    return Comment(
        data_base_id=comment_id, 
        user=data["user"], 
        content=data["content"],
        date_time=datetime.fromisoformat(data["date_time"]) 
        )

def get_instrument(cursor: sqlite3.Cursor, instrument_id: int) -> Instrument | None:
    cursor.execute(
        "SELECT name, remaining_uses, note_content, note_type_id FROM instruments WHERE id = ?",
        (instrument_id,)
    )

    data = cursor.fetchone()

    if data is None:
        return None

    note_type = None
    if data["note_type_id"] is not None:
        note_type = EnumNoteType(data["note_type_id"])

    return Instrument(
        data_base_id=instrument_id, 
        name=data["name"],
        note_type=note_type,
        note_content=data["note_content"],
        _remaining_uses=data["remaining_uses"]
        )

def get_set_state(cursor: sqlite3.Cursor, set_state_id: int) -> SetState | None:
    cursor.execute(
        "SELECT user, state_id, comment_id, date_time FROM set_states WHERE id = ?",
        (set_state_id,)
    )

    data = cursor.fetchone()

    if data is None:
        return None

    comment = None
    if data["comment_id"]:
        comment=get_comment(cursor, data["comment_id"])

    return SetState(
        data_base_id=set_state_id,
        user=data["user"],
        state=EnumSetState(data["state_id"]),
        comment=comment,
        date_time=datetime.fromisoformat(data["date_time"])
    )

def get_set(cursor: sqlite3.Cursor, set_serial_number: int) -> Set | None:
    cursor.execute(
        "SELECT name, customer, packaging_id, active_comment_id FROM sets WHERE serial_number = ?",
        (set_serial_number,)
    )

    data = cursor.fetchone()

    if data is None:
        return None

    cursor.execute(
        "SELECT id FROM instruments WHERE set_id = ?",
        (set_serial_number,)
    )

    instrument_data = cursor.fetchall()
    instruments = list()

    if instrument_data is not None:
        for instrument_id in instrument_data:
                instruments.append(get_instrument(cursor, instrument_id["id"]))

    cursor.execute(
        "SELECT id FROM set_states WHERE set_id = ?",
        (set_serial_number,)
    )

    set_state_data = cursor.fetchall()
    set_states = list()

    if set_state_data is not None:
        for set_state_id in set_state_data:
            set_states.append(get_set_state(cursor, set_state_id["id"]))

    return Set(
        name=data["name"],
        customer=data["customer"],
        _serial_number = set_serial_number,
        packaging=EnumPackaging(data["packaging_id"]),
        _active_comment=get_comment(cursor, data["active_comment_id"]),
        _instruments=instruments,
        _state_log=set_states
    )
