### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class GlobalPos:
    def __init__(
            self,
            pos: Optional[Union[Any, Any]] = None,
            dimension: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if pos is not None:
            self.components["pos"] = pos
        if dimension is not None:
            self.components["dimension"] = dimension

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class ExpirableValue:
    def __init__(
            self,
            ttl: Optional[Union[long, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if ttl is not None:
            self.components["ttl"] = ttl

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class AdmiringDisable(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class AdmiringItem(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class AngryAt(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[Any, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class AttackTargetCooldown(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class BreezeJumpCooldown(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class BreezeJumpInhaling(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class BreezeJumpTarget(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[Any, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class BreezeLeavingWater(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class BreezeShoot(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class BreezeShootCharging(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class BreezeShootCooldown(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class BreezeShootRecover(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class ChargeCooldownTicks(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class DangerDetectedRecently(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class DigCooldown(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class GazeCooldownTicks(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class GolemDetectedRecently(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class HasHuntingCooldown(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class Home(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union['GlobalPos', Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class HuntedRecently(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class IsEmerging(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class IsInWater(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class IsPanicking(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class IsPregnant(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class IsSniffing(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class IsTempted(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class ItemPickupCooldownTicks(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class JobSite(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union['GlobalPos', Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class LastSlept(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[long, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class LastWoken(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[long, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class LastWorkedAtPoi(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[long, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class LikedNoteblock(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union['GlobalPos', Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class LikedNoteblockCooldownTicks(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class LikedPlayer(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[Any, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class LongJumpCoolingDown(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class MeetingPoint(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union['GlobalPos', Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class PlayDeadTicks(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class PotentialJobSite(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union['GlobalPos', Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class RamCooldownTicks(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class RecentProjectile(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class RoarSoundCooldown(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class RoarSoundDelay(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class SniffCooldown(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class SnifferExploredPositions(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[list[Any], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class SonicBoomCooldown(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class SonicBoomSoundCooldown(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class SonicBoomSoundDelay(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class TemptationCooldownTicks(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class TouchCooldown(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class UniversalAnger(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class UnreachableTransportBlockPositions(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[list['GlobalPos'], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class VibrationCooldown(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class VisitedBlockPositions(ExpirableValue):
    def __init__(
            self,
            value: Optional[Union[list['GlobalPos'], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

