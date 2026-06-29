### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class ExpirableValue:
    ttl: long

@struct
class AdmiringItem(ExpirableValue):
    value: bool

@struct
class UniversalAnger(ExpirableValue):
    value: bool

@struct
class LastWorkedAtPoi(ExpirableValue):
    value: long

@struct
class AttackTargetCooldown(ExpirableValue):
    value: int

@struct
class SniffCooldown(ExpirableValue):
    value: dict

@struct
class ItemPickupCooldownTicks(ExpirableValue):
    value: int

@struct
class TemptationCooldownTicks(ExpirableValue):
    value: int

@struct
class PlayDeadTicks(ExpirableValue):
    value: int

@struct
class BreezeJumpCooldown(ExpirableValue):
    value: dict

@struct
class IsPanicking(ExpirableValue):
    value: bool

@struct
class HuntedRecently(ExpirableValue):
    value: bool

@struct
class TouchCooldown(ExpirableValue):
    value: dict

@struct
class LikedNoteblock(ExpirableValue):
    value: 'GlobalPos'

@struct
class IsEmerging(ExpirableValue):
    value: dict

@struct
class MeetingPoint(ExpirableValue):
    value: 'GlobalPos'

@struct
class GazeCooldownTicks(ExpirableValue):
    value: int

@struct
class RamCooldownTicks(ExpirableValue):
    value: int

@struct
class SnifferExploredPositions(ExpirableValue):
    value: list[Any]

@struct
class DangerDetectedRecently(ExpirableValue):
    value: bool

@struct
class LikedNoteblockCooldownTicks(ExpirableValue):
    value: int

@struct
class AdmiringDisable(ExpirableValue):
    value: bool

@struct
class DigCooldown(ExpirableValue):
    value: dict

@struct
class IsSniffing(ExpirableValue):
    value: dict

@struct
class LikedPlayer(ExpirableValue):
    value: Any

@struct
class SonicBoomSoundCooldown(ExpirableValue):
    value: dict

@struct
class BreezeJumpInhaling(ExpirableValue):
    value: dict

@struct
class GlobalPos:
    pos: Any
    dimension: str

@struct
class VisitedBlockPositions(ExpirableValue):
    value: list['GlobalPos']

@struct
class BreezeShootCooldown(ExpirableValue):
    value: dict

@struct
class BreezeShootRecover(ExpirableValue):
    value: dict

@struct
class LastSlept(ExpirableValue):
    value: long

@struct
class LongJumpCoolingDown(ExpirableValue):
    value: int

@struct
class RoarSoundDelay(ExpirableValue):
    value: dict

@struct
class RecentProjectile(ExpirableValue):
    value: dict

@struct
class IsInWater(ExpirableValue):
    value: dict

@struct
class SonicBoomCooldown(ExpirableValue):
    value: dict

@struct
class SonicBoomSoundDelay(ExpirableValue):
    value: dict

@struct
class IsPregnant(ExpirableValue):
    value: dict

@struct
class JobSite(ExpirableValue):
    value: 'GlobalPos'

@struct
class BreezeShoot(ExpirableValue):
    value: dict

@struct
class IsTempted(ExpirableValue):
    value: bool

@struct
class BreezeShootCharging(ExpirableValue):
    value: dict

@struct
class VibrationCooldown(ExpirableValue):
    value: dict

@struct
class Home(ExpirableValue):
    value: 'GlobalPos'

@struct
class RoarSoundCooldown(ExpirableValue):
    value: dict

@struct
class PotentialJobSite(ExpirableValue):
    value: 'GlobalPos'

@struct
class GolemDetectedRecently(ExpirableValue):
    value: bool

@struct
class UnreachableTransportBlockPositions(ExpirableValue):
    value: list['GlobalPos']

@struct
class AngryAt(ExpirableValue):
    value: Any

@struct
class ChargeCooldownTicks(ExpirableValue):
    value: int

@struct
class BreezeJumpTarget(ExpirableValue):
    value: Any

@struct
class HasHuntingCooldown(ExpirableValue):
    value: bool

@struct
class LastWoken(ExpirableValue):
    value: long

@struct
class BreezeLeavingWater(ExpirableValue):
    value: dict