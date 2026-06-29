### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class BlockEntity:
    id: str
    x: int
    y: int
    z: int
    keepPacked: bool
    components: 'DataComponentPatch'

@struct
class PotentSulfur(BlockEntity):
    countdown: int

@struct
class Nameable:
    CustomName: Any

@struct
class Lockable:
    Lock: str
    lock: 'Any'

@struct
class ContainerBase(BlockEntity, Nameable, Lockable):
    LootTable: str
    LootTableSeed: long

@struct
class Shelf(ContainerBase):
    Items: list['Any']
    align_items_to_bottom: bool

@struct
class CustomSpawnRules:
    block_light_limit: 'Any'
    sky_light_limit: 'Any'

@struct
class ReceivingEvent:
    game_event: str
    distance: float
    pos: list[float]
    source: list[int]
    projectile_owner: list[int]

@struct
class TestInstanceBlock(BlockEntity):
    data: dict
    errors: list[dict]

@struct
class Jukebox(BlockEntity):
    RecordItem: 'ItemStack'
    ticks_since_song_started: long

@struct
class SculkCatalyst(BlockEntity):
    cursors: list['ChargeCursor']

@struct
class Container9(ContainerBase):
    Items: list['Any']

@struct
class Crafter(Container9):
    crafting_ticks_remaining: int
    disabled_slots: Any
    triggered: Any

@struct
class MovingPiston(BlockEntity):
    blockState: 'BlockState'
    facing: 'Any'
    progress: float
    extending: bool
    source: bool

@struct
class Jigsaw:
    target_pool: str
    joint: 'Any'
    pool: str
    name: str
    target: str
    final_state: str
    attachment_type: str

@struct
class Bee:
    min_ticks_in_hive: int
    ticks_in_hive: int
    entity_data: 'AnyEntity'

@struct
class Beehive(BlockEntity):
    FlowerPos: 'FlowerPos'
    flower_pos: Any
    Bees: list['LegacyBee']
    bees: list['Bee']

@struct
class Banner(BlockEntity, Nameable):
    Patterns: list['BannerPatternLayer']
    patterns: list['BannerPatternLayer']

@struct
class EnchantingTable(BlockEntity, Nameable):
    pass

@struct
class Spawner(BlockEntity):
    SpawnPotentials: list['Any']
    SpawnData: Any
    SpawnCount: short
    SpawnRange: short
    Delay: short
    MinSpawnDelay: short
    MaxSpawnDelay: short
    MaxNearbyEntities: short
    RequiredPlayerRange: short

@struct
class TestBlock(BlockEntity):
    mode: 'Any'
    message: str
    powered: bool

@struct
class StructureBlock(BlockEntity):
    name: str
    author: str
    metadata: str
    posX: int
    posY: int
    posZ: int
    sizeX: int
    sizeY: int
    sizeZ: int
    rotation: 'Any'
    mirror: 'Any'
    mode: 'Any'
    ignoreEntities: bool
    showboundingbox: bool
    powered: bool
    showair: bool
    strict: bool
    integrity: float
    seed: long

@struct
class Conduit(BlockEntity):
    target_uuid: 'TargetUuid'
    Target: Any

@struct
class Container27(ContainerBase):
    Items: list['Any']

@struct
class Campfire(BlockEntity):
    Items: list['Any']
    CookingTimes: Any
    CookingTotalTimes: Any

@struct
class BrushableBlock(BlockEntity):
    LootTable: str
    LootTableSeed: long
    item: 'ItemStack'
    hit_direction: 'Any'

@struct
class SkullOwner:
    Id: Any
    Name: str
    Properties: 'Properties'

@struct
class ChiseledBookshelf(BlockEntity):
    Items: list['Any']
    last_interacted_slot: int

@struct
class DecoratedPot(BlockEntity):
    LootTable: str
    LootTableSeed: long
    item: 'ItemStack'

@struct
class Texture:
    Signature: str
    Value: str

@struct
class Vault:
    server_data: dict
    config: dict
    shared_data: dict

@struct
class SpawnEquipment:
    loot_table: str
    slot_drop_chances: Any

@struct
class Skull(BlockEntity):
    Owner: 'SkullOwner'
    SkullOwner: 'SkullOwner'
    ExtraType: str
    note_block_sound: Any
    profile: 'Any'
    custom_name: Any

@struct
class ExitPortal:
    X: int
    Y: int
    Z: int

@struct
class Beacon(BlockEntity, Nameable, Lockable):
    Levels: int
    Primary: Any
    Secondary: Any
    primary_effect: str
    secondary_effect: str

@struct
class PositionSource:
    type: str

@struct
class ChargeCursor:
    pos: list[int]
    charge: int
    decay_delay: int
    update_delay: int
    facings: list['Any']

@struct
class SpawnerEntry:
    entity: 'AnyEntity'
    custom_spawn_rules: 'CustomSpawnRules'
    equipment: 'SpawnEquipment'

@struct
class CreakingHeart(BlockEntity):
    creaking: list[int]

@struct
class AnyEntity:
    id: str

@struct
class TrialSpawner:
    normal_config: Any
    ominous_config: Any
    required_player_range: int
    target_cooldown_length: int
    registered_players: list[list[int]]
    current_mobs: list[list[int]]
    cooldown_ends_at: long
    next_mob_spawns_at: long
    total_mobs_spawned: int
    spawn_data: 'SpawnerEntry'
    ejecting_loot_table: str

@struct
class DataComponentPatch:
    pass

@struct
class Lectern(BlockEntity):
    Book: 'ItemStack'
    Page: int

@struct
class BrewingStand(BlockEntity, Nameable, Lockable):
    Items: list['Any']
    BrewTime: short
    Fuel: byte

@struct
class Properties:
    textures: list['Texture']

@struct
class EndGateway(BlockEntity):
    Age: long
    ExactTeleport: bool
    ExitPortal: 'ExitPortal'
    exit_portal: Any

@struct
class Comparator(BlockEntity):
    OutputSignal: int

@struct
class TargetUuid:
    M: long
    L: long

@struct
class Hopper(ContainerBase):
    Items: list['Any']
    TransferCooldown: int

@struct
class BlockState:
    Name: str
    Properties: Any

@struct
class Furnace(BlockEntity, Nameable, Lockable):
    Items: list['Any']
    RecipesUsed: dict

@struct
class SculkSensor:
    last_vibration_frequency: int
    listener: 'VibrationListener'

@struct
class SculkShrieker:
    warning_level: int
    listener: 'VibrationListener'

@struct
class LegacyBee:
    MinOccupationTicks: int
    TicksInHive: int
    EntityData: 'AnyEntity'

@struct
class BaseCommandBlock:
    Command: str
    SuccessCount: int
    LastOutput: Any
    TrackOutput: bool
    UpdateLastExecution: bool
    LastExecution: long

@struct
class VibrationListener:
    source: 'PositionSource'
    range: int
    event: 'ReceivingEvent'
    event_distance: float
    event_delay: int

@struct
class CommandBlock(BlockEntity, Nameable, BaseCommandBlock):
    powered: bool
    auto: bool
    conditionMet: bool

@struct
class FlowerPos:
    X: int
    Y: int
    Z: int