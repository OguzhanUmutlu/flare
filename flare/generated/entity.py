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
class BlockPredicate:
    block: str
    blocks: Union[str, list[str]]
    tag: str
    state: 'BlockPredicateState'
    nbt: Union[str, Any]
    components: 'DataComponentExactPredicate'
    predicates: 'DataComponentPredicate'

@struct
class BlockPredicateState:
    pass

@struct
class PaintingVariant:
    asset_id: str
    width: int
    height: int
    title: 'Text'
    author: 'Text'

@struct
class GlobalPos:
    pos: Any
    dimension: str
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
RGB = Union[int, list[float]]
RGBA = Union[int, list[float]]
EffectId = Union[int, int]
MobEffectInstance = Union[{'Id': 'EffectId', 'Amplifier': Union[byte, int], 'Duration': Union[int, Any], 'Ambient': bool, 'ShowParticles': bool, 'ShowIcon': bool, 'HiddenEffect': 'MobEffectInstance'}, {'id': str, 'amplifier': Union[byte, int], 'duration': Union[Any, int], 'ambient': bool, 'show_particles': bool, 'show_icon': bool, 'hidden_effect': 'MobEffectInstance'}]

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
class Memories:
    pass

@struct
class Particle:
    type: str

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
class BaseCommandBlock:
    Command: str
    SuccessCount: int
    LastOutput: Union[str, 'Text']
    TrackOutput: bool
    UpdateLastExecution: bool
    LastExecution: long

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
class SpawnerEntry:
    entity: 'AnyEntity'
    custom_spawn_rules: 'CustomSpawnRules'
    equipment: 'SpawnEquipment'
CustomData = Union['CustomDataMap', str]

@struct
class CustomDataMap:
    pass

@struct
class DataComponentExactPredicate:
    pass

@struct
class DataComponentPredicate:
    pass
AdventureModePredicate = Union[{'predicates': list['BlockPredicate'], 'show_in_tooltip': bool}, list['BlockPredicate'], 'BlockPredicate']

@struct
class AnyEntity:
    id: str

@struct
class EntityBase:
    Pos: list[double]
    Motion: list[double]
    Rotation: list[float]
    FallDistance: float
    fall_distance: double
    Fire: short
    Air: short
    HasVisualFire: bool
    OnGround: bool
    NoGravity: bool
    Invulnerable: bool
    PortalCooldown: int
    UUIDMost: long
    UUIDLeast: long
    UUID: Any
    CustomName: Union[str, 'Text']
    CustomNameVisible: bool
    Silent: bool
    Passengers: list['AnyEntity']
    Glowing: bool
    Tags: list[str]
    Team: str
    data: 'CustomData'
    TicksFrozen: int

@struct
class BlockAttachedEntity(EntityBase):
    TileX: int
    TileY: int
    TileZ: int
    block_pos: Any

@struct
class AreaEffectCloud(EntityBase):
    Age: int
    Color: int
    Duration: int
    ReapplicationDelay: int
    WaitTime: int
    DurationOnUse: int
    OwnerUUIDMost: long
    OwnerUUIDLeast: long
    Owner: Any
    Radius: float
    RadiusOnUse: float
    RadiusPerTick: float
    Particle: Union[str, 'Particle']
    custom_particle: 'Particle'
    Potion: str
    Effects: list['MobEffectInstance']
    effects: list['MobEffectInstance']
    potion_contents: Any
    potion_duration_scale: float

@struct
class Boat(EntityBase):
    Type: str

@struct
class ChestBoat(Boat):
    LootTable: str
    LootTableSeed: long
    Items: list['SlottedItem']

@struct
class Cushion(BlockAttachedEntity):
    color: 'DyeColor'

@struct
class AxisAngle:
    axis: list[float]
    angle: float

@struct
class DisplayBase(EntityBase):
    transformation: 'Transformation'
    shadow_radius: float
    shadow_strength: float
    start_interpolation: int
    interpolation_duration: int
    teleport_duration: int
    billboard: str
    brightness: 'Brightness'
    view_range: float
    width: float
    height: float
    glow_color_override: Union[Any, int]

@struct
class BlockDisplay(DisplayBase):
    block_state: 'BlockState'

@struct
class Brightness:
    sky: int
    block: int

@struct
class ItemDisplay(DisplayBase):
    item: 'ItemStack'
    item_display: str
Rotation = Union[list[float], 'AxisAngle']

@struct
class TextDisplay(DisplayBase):
    text: Union[str, 'Text']
    line_width: int
    text_opacity: int
    background: int
    default_background: bool
    shadow: bool
    see_through: bool
Transformation = Union[{'translation': list[float], 'left_rotation': 'Rotation', 'right_rotation': 'Rotation', 'scale': list[float]}, Union[list[float]]]

@struct
class BeamTarget:
    X: int
    Y: int
    Z: int

@struct
class EndCrystal(EntityBase):
    ShowBottom: bool
    BeamTarget: 'BeamTarget'
    beam_target: Any

@struct
class EvokerFangs(EntityBase):
    Warmup: int
    Owner: Union['Owner', Any]

@struct
class Owner:
    OwnerUUIDMost: long
    OwnerUUIDLeast: long

@struct
class ExperienceOrb(EntityBase):
    Age: short
    Health: short
    Value: short
    Count: int

@struct
class EyeOfEnder(EntityBase):
    Item: 'ItemStack'

@struct
class FallingBlock(EntityBase):
    TileEntityData: Any
    BlockState: 'BlockState'
    Time: int
    DropItem: bool
    HurtEntities: bool
    FallHurtMax: int
    FallHurtAmount: float
    CancelDrop: bool

@struct
class Action:
    player: Any
    timestamp: long

@struct
class Interaction(EntityBase):
    width: float
    height: float
    response: bool
    attack: 'Action'
    interaction: 'Action'

@struct
class Item(EntityBase):
    Age: short
    Health: short
    PickupDelay: short
    Owner: Union['Uuid', Any]
    Thrower: Union['Uuid', Any]
    Item: 'ItemStack'

@struct
class Uuid:
    L: long
    M: long

@struct
class ItemFrame(BlockAttachedEntity):
    Facing: int
    Item: 'ItemStack'
    ItemDropChance: float
    ItemRotation: byte
    Invisible: bool
    Fixed: bool

@struct
class Marker(EntityBase):
    data: dict

@struct
class Minecart(EntityBase):
    CustomDisplayTile: bool
    DisplayState: 'BlockState'
    DisplayOffset: int

@struct
class ContainerMinecart:
    LootTable: str
    LootTableSeed: long

@struct
class ChestMinecart(Minecart, ContainerMinecart):
    Items: list['SlottedItem']

@struct
class CommandBlockMinecart(Minecart, BaseCommandBlock):
    pass

@struct
class FurnaceMinecart(Minecart):
    PushX: double
    PushZ: double
    Fuel: short

@struct
class HopperMinecart(Minecart, ContainerMinecart):
    Items: list['SlottedItem']
    TransferCooldown: int
    Enabled: bool

@struct
class SpawnerMinecart(Minecart):
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
class TntMinecart(Minecart):
    TNTFuse: int
    fuse: int
    explosion_power: float
    explosion_speed_factor: float

@struct
class AgeableMob:
    Age: int
    ForcedAge: int
    AgeLocked: bool

@struct
class Attribute:
    Name: Union[Union[str, str], str]
    Base: double
    Modifiers: list['AttributeModifier']
    id: str
    base: double
    modifiers: list['AttributeModifier']
AttributeModifier = Union[{'id': str, 'amount': double, 'operation': str}, {'Name': str, 'Slot': str, 'Operation': int, 'Amount': double, 'UUIDMost': long, 'UUIDLeast': long, 'UUID': Any}]

@struct
class BlockLeash:
    X: int
    Y: int
    Z: int

@struct
class DropChances:
    pass

@struct
class EntityEquipment:
    pass

@struct
class FallDamageLogicData:
    current_explosion_impact_pos: list[double]

@struct
class LivingEntity(EntityBase, FallDamageLogicData):
    Health: float
    AbsorptionAmount: float
    HurtTime: short
    HurtByTimestamp: int
    DeathTime: short
    FallFlying: bool
    SleepingX: int
    SleepingY: int
    SleepingZ: int
    sleeping_pos: Any
    Brain: {'memories': 'Memories'}
    Attributes: list['Attribute']
    attributes: list['Attribute']
    ActiveEffects: list['MobEffectInstance']
    active_effects: list['MobEffectInstance']
    Team: str
    last_hurt_by_player: Any
    last_hurt_by_player_memory_time: int
    last_hurt_by_mob: Any
    ticks_since_last_hurt_by_mob: int
    locator_bar_icon: 'WaypointIcon'

@struct
class MobBase(LivingEntity):
    DeathLootTable: str
    DeathLootTableSeed: long
    CanPickUpLoot: bool
    PersistenceRequired: bool
    LeftHanded: bool
    NoAI: bool
    Leash: Union['UUIDLeash', 'BlockLeash']
    leash: Union[Any, {'UUID': Any}]
    home_radius: int
    home_pos: Any

@struct
class NeutralMob:
    AngerTime: int
    anger_end_time: long
    AngryAt: Any
    angry_at: Any

@struct
class Squid(MobBase, AgeableMob):
    pass

@struct
class UUIDLeash:
    UUIDMost: long
    UUIDLeast: long

@struct
class WaypointIcon:
    style: str
    color: 'RGB'

@struct
class Allay(MobBase):
    CanDuplicate: bool
    DuplicationCooldown: int
    Inventory: list['ItemStack']
    listener: 'VibrationListener'

@struct
class ArmorStand(LivingEntity):
    HandItems: list[Union['ItemStack', dict]]
    ArmorItems: list[Union['ItemStack', dict]]
    equipment: 'EntityEquipment'
    Invisible: bool
    Marker: bool
    NoBasePlate: bool
    ShowArms: bool
    Small: bool
    DisabledSlots: int
    Pose: 'Pose'

@struct
class Pose:
    Body: list[float]
    LeftArm: list[float]
    RightArm: list[float]
    LeftLeg: list[float]
    RightLeg: list[float]
    Head: list[float]

@struct
class Bat(MobBase):
    BatFlags: bool

@struct
class Bogged(MobBase):
    sheared: bool

@struct
class Breedable(MobBase, AgeableMob):
    InLove: int
    LoveCauseLeast: long
    LoveCauseMost: long
    LoveCause: Any

@struct
class Armadillo(Breedable):
    state: str
    scute_time: int

@struct
class Axolotl(Breedable):
    Variant: int
    FromBucket: bool

@struct
class Bee(Breedable, NeutralMob):
    HivePos: 'HivePos'
    hive_pos: Any
    FlowerPos: 'FlowerPos'
    flower_pos: Any
    HasNectar: bool
    HasStung: bool
    TicksSincePollination: int
    CannotEnterHiveTicks: int
    CropsGrownSincePollination: int
    Anger: int
    HurtBy: Union[str, Any]

@struct
class FlowerPos:
    X: int
    Y: int
    Z: int

@struct
class HivePos:
    X: int
    Y: int
    Z: int

@struct
class Chicken(Breedable):
    IsChickenJockey: bool
    EggLayTime: int
    variant: str
    sound_variant: str

@struct
class Cow(Breedable):
    variant: str
    sound_variant: str

@struct
class Fox(Breedable):
    TrustedUUIDs: list['TrustedUUID']
    Trusted: list[Any]
    Sleeping: bool
    Type: str
    Sitting: bool
    Crouching: bool

@struct
class TrustedUUID:
    L: long
    M: long

@struct
class Frog(Breedable):
    variant: str

@struct
class Goat(Breedable):
    HasLeftHorn: bool
    HasRightHorn: bool
    IsScreamingGoat: bool

@struct
class Hoglin(Breedable):
    IsImmuneToZombification: bool
    CannotBeHunted: bool
    TimeInOverworld: int

@struct
class HorseBase(Breedable):
    Bred: bool
    EatingHaystack: bool
    Tame: bool
    Temper: int
    OwnerUUID: str
    Owner: Any
    SaddleItem: 'ItemStack'

@struct
class Camel(HorseBase):
    IsSitting: bool
    LastPoseTick: long

@struct
class ChestedHorse(HorseBase):
    ChestedHorse: bool
    Items: list[Union['SlottedItem', dict]]

@struct
class Horse(HorseBase):
    Variant: int

@struct
class Llama(ChestedHorse):
    Strength: int
    Variant: int

@struct
class SkeletonHorse(HorseBase):
    SkeletonTrap: bool
    SkeletonTrapTime: int

@struct
class TraderLlama(Llama):
    DespawnDelay: int

@struct
class Mooshroom(Breedable):
    Type: str
    EffectId: 'EffectId'
    EffectDuration: int
    stew_effects: Any

@struct
class Ocelot(Breedable):
    Trusting: bool

@struct
class Panda(Breedable):
    MainGene: str
    HiddenGene: str

@struct
class PolarBear(Breedable, NeutralMob):
    pass

@struct
class Rabbit(Breedable):
    RabbitType: int
    MoreCarrotTicks: int

@struct
class Saddled(Breedable):
    Saddle: bool

@struct
class Pig(Saddled):
    variant: str
    sound_variant: str

@struct
class Sheep(Breedable):
    Sheared: bool
    Color: 'DyeColorByte'

@struct
class Tamable(Breedable):
    OwnerUUID: str
    Owner: Any
    Sitting: bool

@struct
class Cat(Tamable):
    CatType: int
    CollarColor: 'DyeColorByte'
    variant: str
    sound_variant: str

@struct
class Parrot(Tamable):
    Variant: int

@struct
class Wolf(Tamable, NeutralMob):
    Angry: bool
    CollarColor: 'DyeColorByte'
    variant: str
    sound_variant: str

@struct
class Turtle(Breedable):
    HasEgg: bool
    has_egg: bool
    HomePosX: int
    HomePosY: int
    HomePosZ: int
    home_pos: Any
    TravelPosX: int
    TravelPosY: int
    TravelPosZ: int

@struct
class Offers:
    Recipes: list['Recipe']

@struct
class PlayerReputationPart:
    Type: str
    Value: Any
    Target: Any

@struct
class Recipe:
    rewardExp: bool
    maxUses: int
    uses: int
    buy: 'ItemCost'
    buyB: 'ItemCost'
    sell: 'ItemStack'
    xp: int
    priceMultiplier: float
    specialPrice: int
    demand: int

@struct
class VillagerBase:
    Inventory: list['ItemStack']
    Offers: 'Offers'

@struct
class Villager(Breedable, VillagerBase):
    VillagerData: 'VillagerData'
    FoodLevel: byte
    Gossips: list['PlayerReputationPart']
    LastGossipDecay: long
    LastRestock: long
    RestocksToday: int
    Xp: int

@struct
class VillagerData:
    level: int
    profession: str
    type: str

@struct
class WanderTarget:
    X: int
    Y: int
    Z: int

@struct
class WanderingTrader(MobBase, VillagerBase):
    DespawnDelay: int
    WanderTarget: 'WanderTarget'
    wander_target: Any

@struct
class CopperGolem(MobBase):
    next_weather_age: long
    weather_state: str

@struct
class Creaking(MobBase):
    home_pos: list[int]

@struct
class Creeper(MobBase):
    powered: bool
    ExplosionRadius: byte
    Fuse: short
    ignited: bool

@struct
class Dolphin(MobBase, AgeableMob):
    TreasurePosX: int
    TreasurePosY: int
    TreasurePosZ: int
    GotFish: bool
    Moistness: int

@struct
class EnderDragon(MobBase):
    DragonPhase: int

@struct
class Enderman(MobBase, NeutralMob):
    carriedBlockState: 'BlockState'

@struct
class Endermite(MobBase):
    Lifetime: int
    PlayerSpawned: bool

@struct
class Fish(MobBase):
    FromBucket: bool

@struct
class Pufferfish(Fish):
    PuffState: int

@struct
class Salmon(Fish):
    type: str

@struct
class TropicalFish(Fish):
    Variant: int

@struct
class Ghast(MobBase):
    ExplosionPower: int

@struct
class GlowSquid(MobBase, AgeableMob):
    DarkTicksRemaining: int

@struct
class HappyGhast(MobBase, AgeableMob):
    still_timeout: int

@struct
class IronGolem(MobBase, NeutralMob):
    PlayerCreated: bool

@struct
class Mannequin(LivingEntity):
    profile: 'Profile'
    hidden_layers: list[str]
    main_hand: str
    pose: str
    immovable: bool
    description: 'Text'
    hide_description: bool
    equipment: 'EntityEquipment'

@struct
class Phantom(MobBase):
    AX: int
    AY: int
    AZ: int
    anchor_pos: Any
    Size: int
    size: int

@struct
class PiglinBase(MobBase):
    IsImmuneToZombification: bool
    TimeInOverworld: int

@struct
class Piglin(PiglinBase):
    IsBaby: bool
    CannotHunt: bool
    Inventory: list['ItemStack']

@struct
class Abilities:
    walkSpeed: float
    flySpeed: float
    mayfly: bool
    flying: bool
    invulnerable: bool
    mayBuild: bool
    instabuild: bool

@struct
class EnderPearl(AnyEntity):
    ender_pearl_dimension: str

@struct
class EnteredNetherPosition:
    x: double
    y: double
    z: double

@struct
class Player(LivingEntity, FallDamageLogicData):
    DataVersion: int
    Dimension: Union['Dimension', str]
    LastDeathLocation: 'GlobalPos'
    playerGameType: int
    previousPlayerGameType: int
    Score: int
    SelectedItemSlot: int
    SelectedItem: 'SlottedItem'
    equipment: 'PlayerEquipment'
    SpawnDimension: str
    SpawnAngle: float
    SpawnX: int
    SpawnY: int
    SpawnZ: int
    SpawnForced: bool
    respawn: 'Respawn'
    SleepTimer: short
    foodLevel: int
    foodExhaustionLevel: float
    foodSaturationLevel: float
    foodTickTimer: int
    XpLevel: int
    XpP: float
    XpTotal: int
    XpSeed: int
    Inventory: list['SlottedItem']
    EnderItems: list['SlottedItem']
    abilities: 'Abilities'
    enteredNetherPosition: 'EnteredNetherPosition'
    entered_nether_pos: list[double]
    raid_omen_position: Any
    RootVehicle: 'RootVehicle'
    ShoulderEntityLeft: 'AnyEntity'
    ShoulderEntityRight: 'AnyEntity'
    seenCredits: bool
    recipeBook: 'RecipeBook'
    warden_spawn_tracker: 'WardenSpawnTracker'
    ender_pearls: list['EnderPearl']
    post_effects: list[str]
    last_explosion_impact_pos: list[double]
    spawn_extra_particles_on_fall: bool
    CustomName: Any
    CustomNameVisible: Any

@struct
class PlayerEquipment:
    pass

@struct
class RecipeBook:
    recipes: list[str]
    toBeDisplayed: list[str]
    isFilteringCraftable: bool
    isGuiOpen: bool
    isFurnaceFilteringCraftable: bool
    isFurnaceGuiOpen: bool

@struct
class Respawn:
    pos: Any
    angle: float
    yaw: float
    pitch: float
    forced: bool

@struct
class RootVehicle:
    AttachMost: long
    AttachLeast: long
    Attach: Any
    Entity: 'AnyEntity'

@struct
class WardenSpawnTracker:
    cooldown_ticks: int
    ticks_since_last_warning: int
    warning_level: int

@struct
class PatrolTarget:
    X: int
    Y: int
    Z: int

@struct
class RaiderBase(MobBase):
    Patrolling: bool
    PatrolLeader: bool
    PatrolTarget: 'PatrolTarget'
    patrol_target: Any
    CanJoinRaid: bool
    RaidId: int
    Wave: int

@struct
class Pillager(RaiderBase):
    Inventory: list['ItemStack']

@struct
class Ravager(RaiderBase):
    AttackTick: int
    RoarTick: int
    StunTick: int

@struct
class Spellcaster(RaiderBase):
    SpellTicks: int

@struct
class Vindicator(RaiderBase):
    Johnny: bool

@struct
class Shulker(MobBase):
    Peek: bool
    AttachFace: int
    Color: Union['DyeColorByte', int]
    APX: int
    APY: int
    APZ: int

@struct
class Skeleton(MobBase):
    StrayConversionTime: int

@struct
class CubeMob:
    Size: Union[int, int]
    wasOnGround: bool

@struct
class Slime(MobBase, CubeMob):
    pass

@struct
class SulfurCube(MobBase, AgeableMob, CubeMob):
    pickup_timer: int
    from_bucket: bool
    fuse: int

@struct
class SnowGolem(MobBase):
    Pumpkin: bool

@struct
class Tadpole(MobBase):
    Age: int
    FromBucket: bool

@struct
class Vex(MobBase):
    BoundX: int
    BoundY: int
    BoundZ: int
    bound_pos: Any
    LifeTicks: int
    life_ticks: int
    owner: Any

@struct
class AngerManagement:
    suspects: list['Suspect']

@struct
class Suspect:
    anger: int
    uuid: Any

@struct
class Warden(MobBase):
    anger: 'AngerManagement'
    listener: 'VibrationListener'

@struct
class Wither(MobBase):
    Invul: int

@struct
class Zoglin(MobBase):
    IsBaby: bool

@struct
class Zombie(MobBase):
    IsBaby: bool
    CanBreakDoors: bool
    DrownedConversionTime: int
    InWaterTime: int

@struct
class ZombieVillager(Zombie):
    VillagerData: 'VillagerData'
    Gossips: list['PlayerReputationPart']
    Offers: 'Offers'
    ConversionTime: int
    ConversionPlayerLeast: long
    ConversionPlayerMost: long
    ConversionPlayer: Any

@struct
class ZombiePigman(MobBase, NeutralMob):
    IsBaby: bool
    Anger: short
    HurtBy: str

@struct
class OminousItemSpawner(EntityBase):
    item: 'ItemStack'
    spawn_item_after_ticks: long

@struct
class Painting(BlockAttachedEntity):
    Facing: int
    facing: int
    Motive: str
    variant: Union[str, 'PaintingVariant']

@struct
class ProjectileBase(EntityBase):
    HasBeenShot: bool
    Owner: Any
    LeftOwner: bool
    can_break: 'AdventureModePredicate'

@struct
class LlamaSpit(ProjectileBase):
    Owner: 'OwnerUuid'

@struct
class OwnerUuid:
    OwnerUUIDMost: long
    OwnerUUIDLeast: long

@struct
class ArrowBase(ProjectileBase):
    shake: byte
    pickup: int
    player: bool
    life: short
    damage: double
    inGround: bool
    inBlockState: 'BlockState'
    crit: bool
    ShotFromCrossbow: bool
    weapon: 'ItemStack'
    PierceLevel: byte
    SoundEvent: str
    OwnerUUIDMost: long
    OwnerUUIDLeast: long
    item: 'ItemStack'

@struct
class Arrow(ArrowBase):
    Color: int
    CustomPotionEffects: list['MobEffectInstance']
    custom_potion_effects: list['MobEffectInstance']
    Potion: str

@struct
class SpectralArrow(ArrowBase):
    Duration: int

@struct
class Trident(ArrowBase):
    Trident: 'ItemStack'
    DealtDamage: bool

@struct
class AcceleratingProjectileBase(ProjectileBase):
    power: list[double]
    acceleration_power: double

@struct
class DespawnableProjectileBase(AcceleratingProjectileBase):
    direction: list[double]
    life: short

@struct
class FireballBase(DespawnableProjectileBase):
    Item: 'ItemStack'

@struct
class LargeFireball(FireballBase):
    ExplosionPower: int

@struct
class WitherSkull(DespawnableProjectileBase):
    dangerous: bool

@struct
class FireWorkRocket(ProjectileBase):
    Life: int
    LifeTime: int
    ShotAtAngle: bool
    FireworksItem: 'ItemStack'

@struct
class BulletTarget:
    M: long
    L: long
    UUID: Any
    X: int
    Y: int
    Z: int

@struct
class ShulkerBullet(ProjectileBase):
    Owner: 'BulletTarget'
    Steps: int
    Target: 'BulletTarget'
    Dir: int
    TXD: double
    TYD: double
    TZD: double

@struct
class Throwable(ProjectileBase):
    xTile: int
    yTile: int
    zTile: int
    shake: byte
    owner: 'Owner'
    inGround: bool

@struct
class Potion(Throwable):
    Potion: 'ItemStack'
    Item: 'ItemStack'

@struct
class ThrowableItem(Throwable):
    Item: 'ItemStack'

@struct
class Tnt(EntityBase):
    Fuse: short
    fuse: short
    block_state: 'BlockState'
    explosion_power: float
    owner: Any