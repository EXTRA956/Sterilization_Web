import sqlite3
from models import EnumCommentType, EnumPackaging, EnumSetState, Comment, Instrument, Set, SetState

def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect("sterilization.db")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def seed_enum_table(cursor: sqlite3.Cursor, table_name: str, enum_class: EnumCommentType | EnumPackaging | EnumSetState) -> None:
    for member in enum_class:
        cursor.execute(
            f"INSERT OR IGNORE INTO {table_name} (id, name) VALUES (?, ?)", 
            (member.value, member.name)
        )

def seed_all_enum_tables(cursor: sqlite3.Cursor) -> None:
    seed_enum_table(cursor, "enum_comment_type", EnumCommentType)
    seed_enum_table(cursor, "enum_packaging", EnumPackaging)
    seed_enum_table(cursor, "enum_set_state", EnumSetState)

def insert_comment(cursor: sqlite3.Cursor, comment: Comment) -> int:
    cursor.execute(
        f"INSERT INTO comments (content, user, date_time, type_id) VALUES (?, ?, ?, ?)",
        (comment.content, comment.user, comment.date_time.isoformat(), comment.type.value)
    )

    comment_id = cursor.lastrowid

    # Intentional bypass of frozen=true. data_base_id is ease of use only, doesnt need immutability for an audit.
    object.__setattr__(comment, "data_base_id", comment_id)

    return comment_id

def insert_instrument(cursor: sqlite3.Cursor, instrument: Instrument, set_id : int) -> int:
    comment_id = None
    if instrument.comment is not None:
        if instrument.comment.data_base_id is None:
            comment_id = insert_comment(cursor, instrument.comment)
        else:
            comment_id = instrument.comment.data_base_id
       
    cursor.execute(
        f"INSERT INTO instruments (name, remaining_uses, set_id, comment_id) VALUES (?, ?, ?, ?)",
        (instrument.name, instrument.remaining_uses, set_id, comment_id)
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