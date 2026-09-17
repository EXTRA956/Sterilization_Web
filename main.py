import os
from database import get_connection, seed_all_enum_tables, insert_instrument, insert_set, insert_set_state, get_set
from models import EnumPackaging, Instrument, Set, SetState, EnumSetState

# Toggle this to True only when schema.sql has changed and you need a clean rebuild
WIPE_DATABASE = True

if WIPE_DATABASE and os.path.exists("sterilization.db"):
    os.remove("sterilization.db")

connection = get_connection()
cursor = connection.cursor()

with open("schema.sql", "r") as f:
    cursor.executescript(f.read())

seed_all_enum_tables(cursor)

print("Database ready")

with open("schema.sql", "r") as f:
    cursor.executescript(f.read())
seed_all_enum_tables(cursor)

s = Set(name="Ortho Tray B", customer="Ward 2", _serial_number=777, packaging=EnumPackaging.GEM_4, _active_comment=None)
i = Instrument(data_base_id=None, name="Scissors", note_type=None, note_content=None, _remaining_uses=10)
s.add_instrument(i)

insert_set(cursor, s)
insert_instrument(cursor, i, set_id=s.serial_number)

state = SetState(data_base_id=None, user="ID_001", state=EnumSetState.WASHED, comment=None)
insert_set_state(cursor, state, set_id=s.serial_number)

connection.commit()
connection.close()

# Simulate a completely fresh run, reopening the database from scratch
connection2 = get_connection()
cursor2 = connection2.cursor()

loaded_set = get_set(cursor2, 777)
print(loaded_set)
print("Instruments:", loaded_set.instruments)
print("State log:", loaded_set.state_log)

connection2.close()