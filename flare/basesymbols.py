from typing import Any

from .variables.nbt import struct


@struct
class ItemStack:
    components: dict
    count: int
    id: str


@struct
class BlockPalette:
    palette: list[Any]
    palettes: list[list[Any]]


class DyeColor(Any): ...


class DyeColorByte(Any): ...


class DyeColorInt(Any): ...


class Filterable(Any): ...


class FloatProvider(Any): ...


class GlobalEnvironmentAttributeMap(Any): ...


class InclusiveRange(Any): ...


class IntProvider(Any): ...


class ItemCost(Any): ...


class Layer(Any): ...


class LegacyDustColor(Any): ...


class LegacyTranslucentParticle(Any): ...


class LootCondition(Any): ...


class LootFunction(Any): ...


class MinMaxBounds(Any): ...


class ModelRef(Any): ...


class NoiseRange(Any): ...


class NonEmptyWeightedList(Any): ...


class NonReferenceLootCondition(Any): ...


class NonReferenceLootFunction(Any): ...


class PaletteRef(Any): ...


class PositionalEnvironmentAttributeMap(Any): ...


class SingleItem(Any): ...


class SlotSource(Any): ...


class SlottedItem(Any): ...


class UniformInt(Any): ...


class UniformIntProvider(Any): ...


class WeightedEntry(Any): ...


class WeightedList(Any): ...


class WingsLayer(Any): ...


class CollectionPredicate(Any): ...


class BlockEntityTarget(Any): ...
