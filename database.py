import sqlite3
from models import EnumCommentType, EnumPackaging, EnumSetState

def get_connection() -> sqlite3.Connection:
    return sqlite3.connect("sterilization.db")

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