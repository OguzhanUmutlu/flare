### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

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
    CustomName: Any
    CustomNameVisible: bool
    Silent: bool
    Passengers: list['AnyEntity']
    Glowing: bool
    Tags: list[str]
    data: 'Any'
    TicksFrozen: int

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
    Brain: dict
    Attributes: list['Attribute']
    attributes: list['Attribute']
    ActiveEffects: list['Any']
    active_effects: list['Any']
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
    Leash: Any
    leash: Any
    home_radius: int
    home_pos: Any

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
class AgeableMob:
    Age: int
    ForcedAge: int
    AgeLocked: bool

@struct
class Breedable(MobBase, AgeableMob):
    InLove: int
    LoveCauseLeast: long
    LoveCauseMost: long
    LoveCause: Any

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
class ChestedHorse(HorseBase):
    ChestedHorse: bool
    Items: list[Any]

@struct
class Player(LivingEntity, FallDamageLogicData):
    DataVersion: int
    Dimension: Any
    LastDeathLocation: 'GlobalPos'
    playerGameType: 'Any'
    previousPlayerGameType: 'Any'
    Score: int
    SelectedItemSlot: int
    SelectedItem: 'Any'
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
    Inventory: list['Any']
    EnderItems: list['Any']
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
    last_explosion_impact_pos: list[double]
    spawn_extra_particles_on_fall: bool
    CustomName: Any
    CustomNameVisible: Any

@struct
class EyeOfEnder(EntityBase):
    Item: 'ItemStack'

@struct
class Llama(ChestedHorse):
    Strength: int
    Variant: 'Any'

@struct
class Tnt(EntityBase):
    Fuse: short
    fuse: short
    block_state: 'BlockState'
    explosion_power: float
    owner: Any

@struct
class EnderDragon(MobBase):
    DragonPhase: 'Any'

@struct
class Fish(MobBase):
    FromBucket: bool

@struct
class Pufferfish(Fish):
    PuffState: 'Any'

@struct
class Action:
    player: Any
    timestamp: long

@struct
class Mooshroom(Breedable):
    Type: 'Any'
    EffectId: 'Any'
    EffectDuration: int
    stew_effects: Any

@struct
class Endermite(MobBase):
    Lifetime: int
    PlayerSpawned: bool

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
class PlayerEquipment:
    pass

@struct
class WardenSpawnTracker:
    cooldown_ticks: int
    ticks_since_last_warning: int
    warning_level: int

@struct
class DisplayBase(EntityBase):
    transformation: 'Any'
    shadow_radius: float
    shadow_strength: float
    start_interpolation: int
    interpolation_duration: int
    teleport_duration: int
    billboard: 'Any'
    brightness: 'Brightness'
    view_range: float
    width: float
    height: float
    glow_color_override: Any

@struct
class BlockDisplay(DisplayBase):
    block_state: 'BlockState'

@struct
class Tamable(Breedable):
    OwnerUUID: str
    Owner: Any
    Sitting: bool

@struct
class Parrot(Tamable):
    Variant: 'Any'

@struct
class ProjectileBase(EntityBase):
    HasBeenShot: bool
    Owner: Any
    LeftOwner: bool

@struct
class ShulkerBullet(ProjectileBase):
    Owner: 'BulletTarget'
    Steps: int
    Target: 'BulletTarget'
    Dir: 'Any'
    TXD: double
    TYD: double
    TZD: double

@struct
class AcceleratingProjectileBase(ProjectileBase):
    power: list[double]
    acceleration_power: double

@struct
class TropicalFish(Fish):
    Variant: int

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
class Creaking(MobBase):
    home_pos: list[int]

@struct
class NeutralMob:
    AngerTime: int
    anger_end_time: long
    AngryAt: Any
    angry_at: Any

@struct
class Enderman(MobBase, NeutralMob):
    carriedBlockState: 'BlockState'

@struct
class ArrowBase(ProjectileBase):
    shake: byte
    pickup: 'Any'
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
class BeamTarget:
    X: int
    Y: int
    Z: int

@struct
class Rabbit(Breedable):
    RabbitType: 'Any'
    MoreCarrotTicks: int

@struct
class PatrolTarget:
    X: int
    Y: int
    Z: int

@struct
class Respawn:
    pos: Any
    angle: float
    yaw: float
    pitch: float
    forced: bool

@struct
class Bat(MobBase):
    BatFlags: bool

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
    Items: list['Any']

@struct
class Arrow(ArrowBase):
    Color: int
    CustomPotionEffects: list['Any']
    custom_potion_effects: list['Any']
    Potion: str

@struct
class BlockState:
    Name: str
    Properties: Any

@struct
class Shulker(MobBase):
    Peek: bool
    AttachFace: 'Any'
    Color: Any
    APX: int
    APY: int
    APZ: int

@struct
class Chicken(Breedable):
    IsChickenJockey: bool
    EggLayTime: int
    variant: str
    sound_variant: str

@struct
class BaseCommandBlock:
    Command: str
    SuccessCount: int
    LastOutput: Any
    TrackOutput: bool
    UpdateLastExecution: bool
    LastExecution: long

@struct
class CommandBlockMinecart(Minecart, BaseCommandBlock):
    pass

@struct
class Item(EntityBase):
    Age: short
    Health: short
    PickupDelay: short
    Owner: Any
    Thrower: Any
    Item: 'ItemStack'

@struct
class OminousItemSpawner(EntityBase):
    item: 'ItemStack'
    spawn_item_after_ticks: long

@struct
class Throwable(ProjectileBase):
    xTile: int
    yTile: int
    zTile: int
    shake: byte
    owner: 'Owner'
    inGround: bool

@struct
class ThrowableItem(Throwable):
    Item: 'ItemStack'

@struct
class Offers:
    Recipes: list['Recipe']

@struct
class ReceivingEvent:
    game_event: str
    distance: float
    pos: list[float]
    source: list[int]
    projectile_owner: list[int]

@struct
class VillagerData:
    level: int
    profession: str
    type: str

@struct
class Tadpole(MobBase):
    Age: int
    FromBucket: bool

@struct
class Boat(EntityBase):
    Type: 'Any'

@struct
class IronGolem(MobBase, NeutralMob):
    PlayerCreated: bool

@struct
class WanderingTrader(MobBase, VillagerBase):
    DespawnDelay: int
    WanderTarget: 'WanderTarget'
    wander_target: Any

@struct
class Pose:
    Body: list[float]
    LeftArm: list[float]
    RightArm: list[float]
    LeftLeg: list[float]
    RightLeg: list[float]
    Head: list[float]

@struct
class Mannequin(LivingEntity):
    profile: 'Any'
    hidden_layers: list['Any']
    main_hand: 'Any'
    pose: 'Any'
    immovable: bool
    description: 'Any'
    hide_description: bool
    equipment: 'EntityEquipment'

@struct
class Camel(HorseBase):
    IsSitting: bool
    LastPoseTick: long

@struct
class Saddled(Breedable):
    Saddle: bool

@struct
class TntMinecart(Minecart):
    TNTFuse: int
    fuse: int
    explosion_power: float
    explosion_speed_factor: float

@struct
class Skeleton(MobBase):
    StrayConversionTime: int

@struct
class Armadillo(Breedable):
    state: 'Any'
    scute_time: int

@struct
class EntityEquipment:
    pass

@struct
class Interaction(EntityBase):
    width: float
    height: float
    response: bool
    attack: 'Action'
    interaction: 'Action'

@struct
class PiglinBase(MobBase):
    IsImmuneToZombification: bool
    TimeInOverworld: int

@struct
class BlockAttachedEntity(EntityBase):
    TileX: int
    TileY: int
    TileZ: int
    block_pos: Any

@struct
class RecipeBook:
    recipes: list[str]
    toBeDisplayed: list[str]
    isFilteringCraftable: bool
    isGuiOpen: bool
    isFurnaceFilteringCraftable: bool
    isFurnaceGuiOpen: bool

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
class Ravager(RaiderBase):
    AttackTick: int
    RoarTick: int
    StunTick: int

@struct
class Recipe:
    rewardExp: bool
    maxUses: int
    uses: int
    buy: 'Any'
    buyB: 'Any'
    sell: 'ItemStack'
    xp: int
    priceMultiplier: float
    specialPrice: int
    demand: int

@struct
class Piglin(PiglinBase):
    IsBaby: bool
    CannotHunt: bool
    Inventory: list['ItemStack']

@struct
class TextDisplay(DisplayBase):
    text: Any
    line_width: int
    text_opacity: int
    background: int
    default_background: bool
    shadow: bool
    see_through: bool

@struct
class OwnerUuid:
    OwnerUUIDMost: long
    OwnerUUIDLeast: long

@struct
class Particle:
    type: str

@struct
class Phantom(MobBase):
    AX: int
    AY: int
    AZ: int
    anchor_pos: Any
    Size: int
    size: int

@struct
class ZombiePigman(MobBase, NeutralMob):
    IsBaby: bool
    Anger: short
    HurtBy: str

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
class WanderTarget:
    X: int
    Y: int
    Z: int

@struct
class WaypointIcon:
    style: str
    color: 'Any'

@struct
class DespawnableProjectileBase(AcceleratingProjectileBase):
    direction: list[double]
    life: short

@struct
class WitherSkull(DespawnableProjectileBase):
    dangerous: bool

@struct
class Squid(MobBase, AgeableMob):
    pass

@struct
class Attribute:
    Name: Any
    Base: double
    Modifiers: list['AttributeModifier']
    id: str
    base: double
    modifiers: list['AttributeModifier']

@struct
class Cat(Tamable):
    CatType: 'Any'
    CollarColor: 'Any'
    variant: str
    sound_variant: str

@struct
class Frog(Breedable):
    variant: str

@struct
class Goat(Breedable):
    HasLeftHorn: bool
    HasRightHorn: bool
    IsScreamingGoat: bool

@struct
class AngerManagement:
    suspects: list['Suspect']

@struct
class TrustedUUID:
    L: long
    M: long

@struct
class Pig(Saddled):
    variant: str
    sound_variant: str

@struct
class Owner:
    M: long
    L: long

@struct
class CopperGolem(MobBase):
    next_weather_age: long
    weather_state: 'Any'

@struct
class FurnaceMinecart(Minecart):
    PushX: double
    PushZ: double
    Fuel: short

@struct
class Sheep(Breedable):
    Sheared: bool
    Color: 'Any'

@struct
class Cow(Breedable):
    variant: str
    sound_variant: str

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
    HurtBy: Any

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
class PositionSource:
    type: str

@struct
class Fox(Breedable):
    TrustedUUIDs: list['TrustedUUID']
    Trusted: list[Any]
    Sleeping: bool
    Type: 'Any'
    Sitting: bool
    Crouching: bool

@struct
class HivePos:
    X: int
    Y: int
    Z: int

@struct
class RootVehicle:
    AttachMost: long
    AttachLeast: long
    Attach: Any
    Entity: 'AnyEntity'

@struct
class BulletTarget:
    M: long
    L: long
    UUID: Any
    X: int
    Y: int
    Z: int

@struct
class SkeletonHorse(HorseBase):
    SkeletonTrap: bool
    SkeletonTrapTime: int

@struct
class Wolf(Tamable, NeutralMob):
    Angry: bool
    CollarColor: 'Any'
    variant: str
    sound_variant: str

@struct
class FireballBase(DespawnableProjectileBase):
    Item: 'ItemStack'

@struct
class Dolphin(MobBase, AgeableMob):
    TreasurePosX: int
    TreasurePosY: int
    TreasurePosZ: int
    GotFish: bool
    Moistness: int

@struct
class FireWorkRocket(ProjectileBase):
    Life: int
    LifeTime: int
    ShotAtAngle: bool
    FireworksItem: 'ItemStack'

@struct
class Brightness:
    sky: int
    block: int

@struct
class Allay(MobBase):
    CanDuplicate: bool
    DuplicationCooldown: int
    Inventory: list['ItemStack']
    listener: 'VibrationListener'

@struct
class Potion(Throwable):
    Potion: 'ItemStack'
    Item: 'ItemStack'

@struct
class ExperienceOrb(EntityBase):
    Age: short
    Health: short
    Value: short
    Count: int

@struct
class AnyEntity:
    id: str

@struct
class EnderPearl(AnyEntity):
    ender_pearl_dimension: str

@struct
class HappyGhast(MobBase, AgeableMob):
    still_timeout: int

@struct
class Ghast(MobBase):
    ExplosionPower: int

@struct
class TraderLlama(Llama):
    DespawnDelay: int

@struct
class VibrationListener:
    source: 'PositionSource'
    range: int
    event: 'ReceivingEvent'
    event_distance: float
    event_delay: int

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
    Particle: Any
    custom_particle: 'Particle'
    Potion: str
    Effects: list['Any']
    effects: list['Any']
    potion_contents: Any
    potion_duration_scale: float

@struct
class FlowerPos:
    X: int
    Y: int
    Z: int

@struct
class EnteredNetherPosition:
    x: double
    y: double
    z: double

@struct
class Wither(MobBase):
    Invul: int

@struct
class ItemDisplay(DisplayBase):
    item: 'ItemStack'
    item_display: 'Any'

@struct
class Horse(HorseBase):
    Variant: 'Any'

@struct
class Painting(BlockAttachedEntity):
    Facing: 'Any'
    facing: 'Any'
    Motive: str
    variant: Any

@struct
class LargeFireball(FireballBase):
    ExplosionPower: int

@struct
class Suspect:
    anger: int
    uuid: Any

@struct
class Bogged(MobBase):
    sheared: bool

@struct
class GlowSquid(MobBase, AgeableMob):
    DarkTicksRemaining: int

@struct
class Salmon(Fish):
    type: 'Any'

@struct
class SnowGolem(MobBase):
    Pumpkin: bool

@struct
class CubeMob:
    Size: Any
    wasOnGround: bool

@struct
class SulfurCube(MobBase, AgeableMob, CubeMob):
    pickup_timer: int
    from_bucket: bool
    fuse: int

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
class Hoglin(Breedable):
    IsImmuneToZombification: bool
    CannotBeHunted: bool
    TimeInOverworld: int

@struct
class SpectralArrow(ArrowBase):
    Duration: int

@struct
class Zoglin(MobBase):
    IsBaby: bool

@struct
class GlobalPos:
    pos: Any
    dimension: str

@struct
class Slime(MobBase, CubeMob):
    pass

@struct
class ItemFrame(BlockAttachedEntity):
    Facing: 'Any'
    Item: 'ItemStack'
    ItemDropChance: float
    ItemRotation: byte
    Invisible: bool
    Fixed: bool

@struct
class PlayerReputationPart:
    Type: 'Any'
    Value: Any
    Target: Any

@struct
class EvokerFangs(EntityBase):
    Warmup: int
    Owner: Any

@struct
class Spellcaster(RaiderBase):
    SpellTicks: int

@struct
class ChestBoat(Boat):
    LootTable: str
    LootTableSeed: long
    Items: list['Any']

@struct
class Trident(ArrowBase):
    Trident: 'ItemStack'
    DealtDamage: bool

@struct
class Vindicator(RaiderBase):
    Johnny: bool

@struct
class EndCrystal(EntityBase):
    ShowBottom: bool
    BeamTarget: 'BeamTarget'
    beam_target: Any

@struct
class Panda(Breedable):
    MainGene: 'Any'
    HiddenGene: 'Any'

@struct
class SpawnerMinecart(Minecart):
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
class Axolotl(Breedable):
    Variant: 'Any'
    FromBucket: bool

@struct
class Warden(MobBase):
    anger: 'AngerManagement'
    listener: 'VibrationListener'

@struct
class PolarBear(Breedable, NeutralMob):
    pass

@struct
class ArmorStand(LivingEntity):
    HandItems: list[Any]
    ArmorItems: list[Any]
    equipment: 'EntityEquipment'
    Invisible: bool
    Marker: bool
    NoBasePlate: bool
    ShowArms: bool
    Small: bool
    DisabledSlots: int
    Pose: 'Pose'

@struct
class HopperMinecart(Minecart, ContainerMinecart):
    Items: list['Any']
    TransferCooldown: int
    Enabled: bool

@struct
class Ocelot(Breedable):
    Trusting: bool

@struct
class Creeper(MobBase):
    powered: bool
    ExplosionRadius: byte
    Fuse: short
    ignited: bool

@struct
class Marker(EntityBase):
    data: dict

@struct
class LlamaSpit(ProjectileBase):
    Owner: 'OwnerUuid'