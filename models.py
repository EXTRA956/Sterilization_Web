from dataclasses import dataclass, field
from datetime import datetime

from enum import Enum, auto

# Enums
class EnumSetState(Enum):
	NEW = auto()
	ACCEPTED_AT_SSD = auto()
	PRE_WASHED = auto()
	ASSOCIATED_TO_WASHER = auto()
	WASHED = auto()
	PACKED = auto()
	ASSOCIATED_TO_STERILIZER = auto()
	STERILIZED = auto()
	ASSOCIATED_TO_TROLLEY = auto()
	DISPATCHED = auto()
	ACCEPTED_AT_CUSTOMER = auto()
	DIRTY = auto()
	INVALIDATED = auto()

class EnumCommentType(Enum):
	DAMAGED = auto()
	MISSING = auto()
	EXTRA = auto()
	MISC = auto()

class EnumPackaging(Enum):
	GEM_4 = auto()
	GEM_4_AND_GEM_1 = auto()
	CONTAINER_AND_LID = auto()
	DOUBLE_PEEL_POUCH = auto()
	GREEN_PAPER_AND_BAG = auto()

# Data Classes
@dataclass(frozen = True)
class Comment:
	data_base_id: int | None
	user: str
	content: str
	type : EnumCommentType
	date_time: datetime = field(default_factory = datetime.now)

@dataclass(frozen = True)
class SetState:
	data_base_id : int | None
	user: str
	state : EnumSetState
	comment : Comment | None
	date_time: datetime = field(default_factory = datetime.now)

@dataclass
class Instrument:
	data_base_id: int | None
	name : str
	comment : Comment | None
	_remaining_uses: int | None
	
	@property
	def remaining_uses(self) -> int | None:
		return self._remaining_uses

	def use_instrument(self) -> None:
		if self._remaining_uses is None:
			return

		self._remaining_uses -= 1

@dataclass
class Set:
	name : str
	customer : str
	_serial_number : int
	packaging : EnumPackaging
	_active_comment : Comment
	_instruments : list[Instrument] = field(default_factory=list)
	_state_log : list[SetState] = field(default_factory=list)
	
	@property
	def serial_number(self) -> int:
		return self._serial_number

	@property
	def instruments(self) -> list[Instrument]:
		return self._instruments

	def add_instrument(self, instrument : Instrument):
		self._instruments.append(instrument)

	def remove_instrument(self, instrument : Instrument):
		self._instruments.remove(instrument)

	@property
	def state_log(self) -> list[SetState]:
		return self._state_log

	@property
	def active_state(self) -> SetState:
		return self._state_log[-1]

	def add_state(self, state : SetState, clear_comment : bool):
		self._state_log.append(state)

		if clear_comment == True:
			self._active_comment = None
			return

		if state.comment:
			self._active_comment = state.comment

	@property
	def active_comment(self) -> Comment:
		return self._active_comment
