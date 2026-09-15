from models import Set, SetState, EnumSetState, EnumPackaging, Instrument, Comment, EnumCommentType

s = Set(_serial_number=101, packaging=EnumPackaging.GEM_4, _active_comment=None)

i = Instrument(name="Forceps", comment=None, _remaining_uses=5)
s.add_instrument(i)
print(s.instruments)

s.add_state(SetState(author="ID_000", state=EnumSetState.NEW, comment=None))
print(s.active_state)

c = Comment(author="ID_000", text="Damaged tip", type=EnumCommentType.DAMAGED)
s.add_state(SetState(author="ID_000", state=EnumSetState.ACCEPTED_AT_SSD, comment=c))
print(s.active_comment)

s.add_state(SetState(author="ID_000", state=EnumSetState.PRE_WASHED, comment=None))
print(s.active_comment)