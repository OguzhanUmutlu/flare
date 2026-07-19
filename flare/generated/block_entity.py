### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
import typing
from typing import Any
if typing.TYPE_CHECKING:
    from typing import Union
else:

    class _DummyUnion:

        def __getitem__(self, items):
            return typing.Any
    Union = _DummyUnion()

@struct
class EnchantmentPredicate:
    enchantment: str
    enchantments: Union[str, list[str]]
    levels: 'MinMaxBounds'
ItemPredicate = Union[{'item': str, 'items': list[str], 'tag': str, 'durability': 'MinMaxBounds', 'potion': str, 'enchantments': list['EnchantmentPredicate'], 'stored_enchantments': list['EnchantmentPredicate'], 'nbt': str}, {'items': Union[str, list[str]], 'count': 'MinMaxBounds', 'components': 'DataComponentExactPredicate', 'predicates': 'DataComponentPredicate'}]

@struct
class TrialSpawnerConfig:
    spawn_range: int
    total_mobs: float
    total_mobs_added_per_player: float
    simultaneous_mobs: float
    simultaneous_mobs_added_per_player: float
    ticks_between_spawn: int
    spawn_potentials: list['SpawnPotential']
    loot_tables_to_eject: 'WeightedList'
    items_to_drop_when_ominous: str

@struct
class BannerPattern:
    asset_id: str
    translation_key: str
Profile = Union[{'name': str, 'id': Any, 'properties': Union[list['ProfileProperty'], 'ProfilePropertyMap']}, {'name': str, 'id': Any, 'properties': Union[list['ProfileProperty'], list['ProfileProperty'], 'ProfilePropertyMap'], 'texture': str, 'cape': str, 'elytra': str, 'model': str}, str]

@struct
class ProfileProperty:
    name: Union[str, str]
    value: Union[str, str]
    signature: Union[str, str]

@struct
class ProfilePropertyMap:
    pass

@struct
class BlockState:
    Name: str
    Properties: Any
RGBA = Union[int, list[float]]
EffectId = Union[int, int]

@struct
class PositionSource:
    type: str

@struct
class ReceivingEvent:
    game_event: str
    distance: float
    pos: list[float]
    source: list[int]
    projectile_owner: list[int]

@struct
class VibrationListener:
    source: 'PositionSource'
    range: int
    event: 'ReceivingEvent'
    event_distance: float
    event_delay: int

@struct
class ClickEvent:
    action: str

@struct
class HoverEvent:
    action: str

@struct
class ObjectTextConfig:
    fallback: 'Text'
Text = Union[str, 'TextObject', list['Text']]

@struct
class TextStyle:
    color: Union[str, str]
    shadow_color: 'RGBA'
    font: str
    bold: bool
    italic: bool
    underlined: bool
    strikethrough: bool
    obfuscated: bool
    insertion: str
    clickEvent: 'ClickEvent'
    click_event: 'ClickEvent'
    hoverEvent: 'HoverEvent'
    hover_event: 'HoverEvent'

@struct
class TextBase(TextStyle):
    extra: list['Text']

@struct
class TextNbtBase(TextBase):
    interpret: bool
    plain: bool
    separator: 'Text'
TextObject = Union[{'text': str, 'type': Any}, {'translate': str, 'fallback': str, 'with': list['Text'], 'type': Any}, {'score': {'objective': str, 'name': str}, 'type': Any}, {'selector': str, 'separator': 'Text', 'type': Any}, {'keybind': str, 'type': Any}, {'block': str, 'nbt': str, 'source': Any, 'type': Any}, {'entity': str, 'nbt': str, 'source': Any, 'type': Any}, {'storage': str, 'nbt': str, 'source': Any, 'type': Any}, {'atlas': str, 'sprite': str, 'object': Any, 'type': Any}, {'player': 'Profile', 'hat': bool, 'object': Any, 'type': Any}]

@struct
class BlockEntity:
    id: str
    x: int
    y: int
    z: int
    keepPacked: bool
    components: 'DataComponentPatch'

@struct
class Lockable:
    Lock: str
    lock: 'ItemPredicate'

@struct
class Nameable:
    CustomName: Union[str, 'Text']

@struct
class Banner(BlockEntity, Nameable):
    Patterns: list['BannerPatternLayer']
    patterns: list['BannerPatternLayer']
BannerPatternLayer = Union[{'Color': 'DyeColorInt', 'Pattern': str}, {'color': 'DyeColor', 'pattern': Union[str, 'BannerPattern']}]

@struct
class Beacon(BlockEntity, Nameable, Lockable):
    Levels: int
    Primary: Union['NoneId', 'EffectId']
    Secondary: Union['NoneId', 'EffectId']
    primary_effect: str
    secondary_effect: str
NoneId = Union[Any, Any]

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
class FlowerPos:
    X: int
    Y: int
    Z: int

@struct
class LegacyBee:
    MinOccupationTicks: int
    TicksInHive: int
    EntityData: 'AnyEntity'

@struct
class BrewingStand(BlockEntity, Nameable, Lockable):
    Items: list['SlottedItem']
    BrewTime: Union[short, int]
    Fuel: Union[byte, int]
    total_brew_time: int
    total_fuel: int
    speed_multiplier: float

@struct
class BrushableBlock(BlockEntity):
    LootTable: str
    LootTableSeed: long
    item: 'ItemStack'
    hit_direction: int

@struct
class Campfire(BlockEntity):
    Items: list['SlottedItem']
    CookingTimes: Any
    CookingTotalTimes: Any

@struct
class ChiseledBookshelf(BlockEntity):
    Items: list['SlottedItem']
    last_interacted_slot: int

@struct
class BaseCommandBlock:
    Command: str
    SuccessCount: int
    LastOutput: Union[str, 'Text']
    TrackOutput: bool
    UpdateLastExecution: bool
    LastExecution: long

@struct
class CommandBlock(BlockEntity, Nameable, BaseCommandBlock):
    powered: bool
    auto: bool
    conditionMet: bool

@struct
class Comparator(BlockEntity):
    OutputSignal: int

@struct
class Conduit(BlockEntity):
    target_uuid: 'TargetUuid'
    Target: Any

@struct
class TargetUuid:
    M: long
    L: long

@struct
class ContainerBase(BlockEntity, Nameable, Lockable):
    LootTable: str
    LootTableSeed: long

@struct
class Container27(ContainerBase):
    Items: list['SlottedItem']

@struct
class Container9(ContainerBase):
    Items: list['SlottedItem']

@struct
class Hopper(ContainerBase):
    Items: list['SlottedItem']
    TransferCooldown: int

@struct
class Shelf(ContainerBase):
    Items: list['SlottedItem']
    align_items_to_bottom: bool

@struct
class Crafter(Container9):
    crafting_ticks_remaining: int
    disabled_slots: Any
    triggered: Union[Any, Any]

@struct
class CreakingHeart(BlockEntity):
    creaking: list[int]

@struct
class DecoratedPot(BlockEntity):
    LootTable: str
    LootTableSeed: long
    item: 'ItemStack'

@struct
class EnchantingTable(BlockEntity, Nameable):
    pass

@struct
class EndGateway(BlockEntity):
    Age: long
    ExactTeleport: bool
    ExitPortal: 'ExitPortal'
    exit_portal: Any

@struct
class ExitPortal:
    X: int
    Y: int
    Z: int

@struct
class Furnace(BlockEntity, Nameable, Lockable):
    Items: list['SlottedItem']
    RecipesUsed: dict

@struct
class Properties:
    textures: list['Texture']

@struct
class Skull(BlockEntity):
    Owner: 'SkullOwner'
    SkullOwner: 'SkullOwner'
    ExtraType: str
    note_block_sound: Any
    profile: 'Profile'
    custom_name: Any

@struct
class SkullOwner:
    Id: Union[str, Any]
    Name: str
    Properties: 'Properties'

@struct
class Texture:
    Signature: str
    Value: str

@struct
class Jigsaw:
    target_pool: str
    joint: str
    pool: str
    name: str
    target: str
    final_state: str
    attachment_type: str

@struct
class Jukebox(BlockEntity):
    RecordItem: 'ItemStack'
    ticks_since_song_started: long

@struct
class Lectern(BlockEntity):
    Book: 'ItemStack'
    Page: int

@struct
class MovingPiston(BlockEntity):
    blockState: 'BlockState'
    facing: int
    progress: float
    extending: bool
    source: bool

@struct
class PotentSulfur(BlockEntity):
    countdown: int

@struct
class ChargeCursor:
    pos: list[int]
    charge: int
    decay_delay: int
    update_delay: int
    facings: list[str]

@struct
class SculkCatalyst(BlockEntity):
    cursors: list['ChargeCursor']

@struct
class SculkSensor:
    last_vibration_frequency: int
    listener: 'VibrationListener'

@struct
class SculkShrieker:
    warning_level: int
    listener: 'VibrationListener'

@struct
class CustomSpawnRules:
    block_light_limit: 'InclusiveRange'
    sky_light_limit: 'InclusiveRange'

@struct
class SpawnEquipment:
    loot_table: str
    slot_drop_chances: Union[float, dict]
SpawnPotential = Union[{'Entity': 'AnyEntity', 'Weight': Union[int, byte]}, 'WeightedEntry']

@struct
class Spawner(BlockEntity):
    SpawnPotentials: list['SpawnPotential']
    SpawnData: Union['AnyEntity', 'SpawnerEntry']
    SpawnCount: short
    SpawnRange: short
    Delay: short
    MinSpawnDelay: short
    MaxSpawnDelay: short
    MaxNearbyEntities: short
    RequiredPlayerRange: short

@struct
class SpawnerEntry:
    entity: 'AnyEntity'
    custom_spawn_rules: 'CustomSpawnRules'
    equipment: 'SpawnEquipment'

@struct
class TrialSpawner:
    normal_config: Union['TrialSpawnerConfig', str]
    ominous_config: Union['TrialSpawnerConfig', str]
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
    rotation: 'Rotation'
    mirror: str
    mode: str
    ignoreEntities: bool
    showboundingbox: bool
    powered: bool
    showair: bool
    strict: bool
    integrity: float
    seed: long

@struct
class TestBlock(BlockEntity):
    mode: str
    message: str
    powered: bool

@struct
class TestInstanceBlock(BlockEntity):
    data: {'test': str, 'size': Any, 'rotation': 'Rotation', 'ignore_entities': bool, 'status': str, 'error_message': 'Text'}
    errors: list[{'pos': Any, 'text': 'Text'}]

@struct
class Vault:
    server_data: {'state_updating_resumes_at': long, 'rewarded_players': list[Any], 'items_to_eject': list['ItemStack'], 'total_ejections_needed': int}
    config: {'key_item': 'ItemStack', 'loot_table': str, 'override_loot_table_to_display': str, 'activation_range': double, 'deactivation_range': double}
    shared_data: {'display_item': 'ItemStack', 'connected_players': list[Any], 'connected_particles_range': double}

@struct
class DataComponentExactPredicate:
    pass

@struct
class DataComponentPatch:
    pass

@struct
class DataComponentPredicate:
    pass

@struct
class PotDecorations:
    back: 'ItemStackTemplate'
    left: 'ItemStackTemplate'
    right: 'ItemStackTemplate'
    front: 'ItemStackTemplate'

@struct
class AnyEntity:
    id: str
ItemStackTemplate = Union['ItemStack', str]