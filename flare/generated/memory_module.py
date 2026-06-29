### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class ExpirableValue:
    ttl: long

@struct
class GolemDetectedRecently(ExpirableValue):
    value: bool

@struct
class AngryAt(ExpirableValue):
    value: Any

@struct
class HasHuntingCooldown(ExpirableValue):
    value: bool

@struct
class IsPregnant(ExpirableValue):
    value: dict

@struct
class AdmiringDisable(ExpirableValue):
    value: bool

@struct
class RamCooldownTicks(ExpirableValue):
    value: int

@struct
class JobSite(ExpirableValue):
    value: 'GlobalPos'

@struct
class SonicBoomCooldown(ExpirableValue):
    value: dict

@struct
class LastWorkedAtPoi(ExpirableValue):
    value: long

@struct
class UnreachableTransportBlockPositions(ExpirableValue):
    value: list['GlobalPos']

@struct
class SniffCooldown(ExpirableValue):
    value: dict

@struct
class IsPanicking(ExpirableValue):
    value: bool

@struct
class LikedNoteblock(ExpirableValue):
    value: 'GlobalPos'

@struct
class BreezeLeavingWater(ExpirableValue):
    value: dict

@struct
class LastSlept(ExpirableValue):
    value: long

@struct
class BreezeShootCooldown(ExpirableValue):
    value: dict

@struct
class TouchCooldown(ExpirableValue):
    value: dict

@struct
class BreezeJumpCooldown(ExpirableValue):
    value: dict

@struct
class RoarSoundDelay(ExpirableValue):
    value: dict

@struct
class MeetingPoint(ExpirableValue):
    value: 'GlobalPos'

@struct
class SnifferExploredPositions(ExpirableValue):
    value: list[Any]

@struct
class GlobalPos:
    pos: Any
    dimension: str

@struct
class LastWoken(ExpirableValue):
    value: long

@struct
class SonicBoomSoundDelay(ExpirableValue):
    value: dict

@struct
class VibrationCooldown(ExpirableValue):
    value: dict

@struct
class BreezeShoot(ExpirableValue):
    value: dict

@struct
class PlayDeadTicks(ExpirableValue):
    value: int

@struct
class AdmiringItem(ExpirableValue):
    value: bool

@struct
class IsEmerging(ExpirableValue):
    value: dict

@struct
class IsSniffing(ExpirableValue):
    value: dict

@struct
class RecentProjectile(ExpirableValue):
    value: dict

@struct
class Home(ExpirableValue):
    value: 'GlobalPos'

@struct
class LikedPlayer(ExpirableValue):
    value: Any

@struct
class IsTempted(ExpirableValue):
    value: bool

@struct
class ItemPickupCooldownTicks(ExpirableValue):
    value: int

@struct
class LikedNoteblockCooldownTicks(ExpirableValue):
    value: int

@struct
class LongJumpCoolingDown(ExpirableValue):
    value: int

@struct
class AttackTargetCooldown(ExpirableValue):
    value: int

@struct
class GazeCooldownTicks(ExpirableValue):
    value: int

@struct
class PotentialJobSite(ExpirableValue):
    value: 'GlobalPos'

@struct
class SonicBoomSoundCooldown(ExpirableValue):
    value: dict

@struct
class BreezeShootRecover(ExpirableValue):
    value: dict

@struct
class VisitedBlockPositions(ExpirableValue):
    value: list['GlobalPos']

@struct
class BreezeJumpTarget(ExpirableValue):
    value: Any

@struct
class DangerDetectedRecently(ExpirableValue):
    value: bool

@struct
class RoarSoundCooldown(ExpirableValue):
    value: dict

@struct
class BreezeJumpInhaling(ExpirableValue):
    value: dict

@struct
class BreezeShootCharging(ExpirableValue):
    value: dict

@struct
class UniversalAnger(ExpirableValue):
    value: bool

@struct
class IsInWater(ExpirableValue):
    value: dict

@struct
class ChargeCooldownTicks(ExpirableValue):
    value: int

@struct
class HuntedRecently(ExpirableValue):
    value: bool

@struct
class TemptationCooldownTicks(ExpirableValue):
    value: int

@struct
class DigCooldown(ExpirableValue):
    value: dict