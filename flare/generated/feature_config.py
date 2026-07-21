### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class BlockBlobConfig:
    def __init__(
            self,
            state: Optional[Union['BlockState', Any]] = None,
            can_place_on: Optional[Union['BlockPredicate', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if state is not None:
            self.components["state"] = state
        if can_place_on is not None:
            self.components["can_place_on"] = can_place_on

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

class BlockColumnConfig:
    def __init__(
            self,
            direction: Optional[Union[str, Any]] = None,
            allowed_placement: Optional[Union['BlockPredicate', Any]] = None,
            prioritize_tip: Optional[Union[bool, Any]] = None,
            layers: Optional[Union[list['BlockColumnLayer'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if direction is not None:
            self.components["direction"] = direction
        if allowed_placement is not None:
            self.components["allowed_placement"] = allowed_placement
        if prioritize_tip is not None:
            self.components["prioritize_tip"] = prioritize_tip
        if layers is not None:
            self.components["layers"] = layers

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

class BlockColumnLayer:
    def __init__(
            self,
            height: Optional[Union['IntProvider', Any]] = None,
            provider: Optional[Union['BlockStateProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if height is not None:
            self.components["height"] = height
        if provider is not None:
            self.components["provider"] = provider

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

class BlockPileConfig:
    def __init__(
            self,
            state_provider: Optional[Union['BlockStateProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if state_provider is not None:
            self.components["state_provider"] = state_provider

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

class BlockPlacer:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type

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

class ColumnsConfig:
    def __init__(
            self,
            block: Optional[Union['BlockStateProvider', Any]] = None,
            can_replace: Optional[Union['BlockPredicate', Any]] = None,
            continue_through: Optional[Union['BlockPredicate', Any]] = None,
            cannot_place_on: Optional[Union[Union[str, list[str]], Any]] = None,
            reach: Optional[Union[Union['UniformInt', 'IntProvider'], Any]] = None,
            column_reach: Optional[Union['IntProvider', Any]] = None,
            column_count: Optional[Union['IntProvider', Any]] = None,
            height: Optional[Union[Union['UniformInt', 'IntProvider'], Any]] = None,
            cluster_reach: Optional[Union['IntProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if block is not None:
            self.components["block"] = block
        if can_replace is not None:
            self.components["can_replace"] = can_replace
        if continue_through is not None:
            self.components["continue_through"] = continue_through
        if cannot_place_on is not None:
            self.components["cannot_place_on"] = cannot_place_on
        if reach is not None:
            self.components["reach"] = reach
        if column_reach is not None:
            self.components["column_reach"] = column_reach
        if column_count is not None:
            self.components["column_count"] = column_count
        if height is not None:
            self.components["height"] = height
        if cluster_reach is not None:
            self.components["cluster_reach"] = cluster_reach

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

class ConfiguredFeature:
    def __init__(
            self,
            type: Optional[Union[Union[str, str], Any]] = None,
            config: Optional[Union[Any, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type
        if config is not None:
            self.components["config"] = config

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

ConfiguredFeatureRef = Union[Union[str, str, 'ConfiguredFeature'], Any]

class CoralConfig:
    def __init__(
            self,
            feature: Optional[Union['PlacedFeatureRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if feature is not None:
            self.components["feature"] = feature

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

class DecoratedConfig:
    def __init__(
            self,
            decorator: Optional[Union['ConfiguredDecorator', Any]] = None,
            feature: Optional[Union['FeatureRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if decorator is not None:
            self.components["decorator"] = decorator
        if feature is not None:
            self.components["feature"] = feature

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

class DeltaConfig:
    def __init__(
            self,
            contents: Optional[Union['BlockState', Any]] = None,
            rim: Optional[Union['BlockState', Any]] = None,
            size: Optional[Union[Union['UniformInt', 'IntProvider'], Any]] = None,
            rim_size: Optional[Union[Union['UniformInt', 'IntProvider'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if contents is not None:
            self.components["contents"] = contents
        if rim is not None:
            self.components["rim"] = rim
        if size is not None:
            self.components["size"] = size
        if rim_size is not None:
            self.components["rim_size"] = rim_size

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

class DiskConfig:
    def __init__(
            self,
            state: Optional[Union['BlockState', Any]] = None,
            state_provider: Optional[Union[Union['RuleBasedBlockStateProvider', 'BlockStateProvider'], Any]] = None,
            radius: Optional[Union[Union['UniformInt', 'IntProvider'], Any]] = None,
            half_height: Optional[Union[int, Any]] = None,
            targets: Optional[Union[list['BlockState'], Any]] = None,
            target: Optional[Union['BlockPredicate', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if state is not None:
            self.components["state"] = state
        if state_provider is not None:
            self.components["state_provider"] = state_provider
        if radius is not None:
            self.components["radius"] = radius
        if half_height is not None:
            self.components["half_height"] = half_height
        if targets is not None:
            self.components["targets"] = targets
        if target is not None:
            self.components["target"] = target

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

class EmeraldOreConfig:
    def __init__(
            self,
            state: Optional[Union['BlockState', Any]] = None,
            target: Optional[Union['BlockState', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if state is not None:
            self.components["state"] = state
        if target is not None:
            self.components["target"] = target

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

class EndGatewayConfig:
    def __init__(
            self,
            exact: Optional[Union[bool, Any]] = None,
            exit: Optional[Union[list[int], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if exact is not None:
            self.components["exact"] = exact
        if exit is not None:
            self.components["exit"] = exit

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

class EndPodiumConfig:
    def __init__(
            self,
            active: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if active is not None:
            self.components["active"] = active

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

class EndSpike:
    def __init__(
            self,
            centerX: Optional[Union[int, Any]] = None,
            centerZ: Optional[Union[int, Any]] = None,
            radius: Optional[Union[int, Any]] = None,
            height: Optional[Union[int, Any]] = None,
            guarded: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if centerX is not None:
            self.components["centerX"] = centerX
        if centerZ is not None:
            self.components["centerZ"] = centerZ
        if radius is not None:
            self.components["radius"] = radius
        if height is not None:
            self.components["height"] = height
        if guarded is not None:
            self.components["guarded"] = guarded

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

class EndSpikeConfig:
    def __init__(
            self,
            spikes: Optional[Union[list['EndSpike'], Any]] = None,
            crystal_invulnerable: Optional[Union[bool, Any]] = None,
            crystal_beam_target: Optional[Union[list[int], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if spikes is not None:
            self.components["spikes"] = spikes
        if crystal_invulnerable is not None:
            self.components["crystal_invulnerable"] = crystal_invulnerable
        if crystal_beam_target is not None:
            self.components["crystal_beam_target"] = crystal_beam_target

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

FeatureRef = Union[Union['ConfiguredFeatureRef', 'PlacedFeatureRef'], Any]

class FillLayerConfig:
    def __init__(
            self,
            state: Optional[Union['BlockState', Any]] = None,
            height: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if state is not None:
            self.components["state"] = state
        if height is not None:
            self.components["height"] = height

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

class ForestRockConfig:
    def __init__(
            self,
            state: Optional[Union['BlockState', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if state is not None:
            self.components["state"] = state

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

class FossilConfig:
    def __init__(
            self,
            max_empty_corners_allowed: Optional[Union[int, Any]] = None,
            fossil_structures: Optional[Union[list[str], Any]] = None,
            overlay_structures: Optional[Union[list[str], Any]] = None,
            fossil_processors: Optional[Union['ProcessorListRef', Any]] = None,
            overlay_processors: Optional[Union['ProcessorListRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if max_empty_corners_allowed is not None:
            self.components["max_empty_corners_allowed"] = max_empty_corners_allowed
        if fossil_structures is not None:
            self.components["fossil_structures"] = fossil_structures
        if overlay_structures is not None:
            self.components["overlay_structures"] = overlay_structures
        if fossil_processors is not None:
            self.components["fossil_processors"] = fossil_processors
        if overlay_processors is not None:
            self.components["overlay_processors"] = overlay_processors

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

class GeodeBlockSettings:
    def __init__(
            self,
            filling_provider: Optional[Union['BlockStateProvider', Any]] = None,
            inner_layer_provider: Optional[Union['BlockStateProvider', Any]] = None,
            alternate_inner_layer_provider: Optional[Union['BlockStateProvider', Any]] = None,
            middle_layer_provider: Optional[Union['BlockStateProvider', Any]] = None,
            outer_layer_provider: Optional[Union['BlockStateProvider', Any]] = None,
            inner_placements: Optional[Union[list['BlockState'], Any]] = None,
            cannot_replace: Optional[Union[Union[str, str, str, list[str]], Any]] = None,
            invalid_blocks: Optional[Union[Union[str, str, str, list[str]], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if filling_provider is not None:
            self.components["filling_provider"] = filling_provider
        if inner_layer_provider is not None:
            self.components["inner_layer_provider"] = inner_layer_provider
        if alternate_inner_layer_provider is not None:
            self.components["alternate_inner_layer_provider"] = alternate_inner_layer_provider
        if middle_layer_provider is not None:
            self.components["middle_layer_provider"] = middle_layer_provider
        if outer_layer_provider is not None:
            self.components["outer_layer_provider"] = outer_layer_provider
        if inner_placements is not None:
            self.components["inner_placements"] = inner_placements
        if cannot_replace is not None:
            self.components["cannot_replace"] = cannot_replace
        if invalid_blocks is not None:
            self.components["invalid_blocks"] = invalid_blocks

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

class GeodeConfig:
    def __init__(
            self,
            blocks: Optional[Union['GeodeBlockSettings', Any]] = None,
            layers: Optional[Union['GeodeLayerSettings', Any]] = None,
            crack: Optional[Union['GeodeCrackSettings', Any]] = None,
            noise_multiplier: Optional[Union[float, Any]] = None,
            use_potential_placements_chance: Optional[Union[float, Any]] = None,
            use_alternate_layer0_chance: Optional[Union[float, Any]] = None,
            placements_require_layer0_alternate: Optional[Union[bool, Any]] = None,
            outer_wall_distance: Optional[Union['IntProvider', Any]] = None,
            distribution_points: Optional[Union['IntProvider', Any]] = None,
            point_offset: Optional[Union['IntProvider', Any]] = None,
            min_gen_offset: Optional[Union[int, Any]] = None,
            max_gen_offset: Optional[Union[int, Any]] = None,
            invalid_blocks_threshold: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if blocks is not None:
            self.components["blocks"] = blocks
        if layers is not None:
            self.components["layers"] = layers
        if crack is not None:
            self.components["crack"] = crack
        if noise_multiplier is not None:
            self.components["noise_multiplier"] = noise_multiplier
        if use_potential_placements_chance is not None:
            self.components["use_potential_placements_chance"] = use_potential_placements_chance
        if use_alternate_layer0_chance is not None:
            self.components["use_alternate_layer0_chance"] = use_alternate_layer0_chance
        if placements_require_layer0_alternate is not None:
            self.components["placements_require_layer0_alternate"] = placements_require_layer0_alternate
        if outer_wall_distance is not None:
            self.components["outer_wall_distance"] = outer_wall_distance
        if distribution_points is not None:
            self.components["distribution_points"] = distribution_points
        if point_offset is not None:
            self.components["point_offset"] = point_offset
        if min_gen_offset is not None:
            self.components["min_gen_offset"] = min_gen_offset
        if max_gen_offset is not None:
            self.components["max_gen_offset"] = max_gen_offset
        if invalid_blocks_threshold is not None:
            self.components["invalid_blocks_threshold"] = invalid_blocks_threshold

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

class GeodeCrackSettings:
    def __init__(
            self,
            generate_crack_chance: Optional[Union[float, Any]] = None,
            base_crack_size: Optional[Union[float, Any]] = None,
            crack_point_offset: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if generate_crack_chance is not None:
            self.components["generate_crack_chance"] = generate_crack_chance
        if base_crack_size is not None:
            self.components["base_crack_size"] = base_crack_size
        if crack_point_offset is not None:
            self.components["crack_point_offset"] = crack_point_offset

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

class GeodeLayerSettings:
    def __init__(
            self,
            filling: Optional[Union[float, Any]] = None,
            inner_layer: Optional[Union[float, Any]] = None,
            middle_layer: Optional[Union[float, Any]] = None,
            outer_layer: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if filling is not None:
            self.components["filling"] = filling
        if inner_layer is not None:
            self.components["inner_layer"] = inner_layer
        if middle_layer is not None:
            self.components["middle_layer"] = middle_layer
        if outer_layer is not None:
            self.components["outer_layer"] = outer_layer

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

class GrowingPlantConfig:
    def __init__(
            self,
            direction: Optional[Union[str, Any]] = None,
            allow_water: Optional[Union[bool, Any]] = None,
            height_distribution: Optional[Union[list['GrowingPlantHeight'], Any]] = None,
            body_provider: Optional[Union['BlockStateProvider', Any]] = None,
            head_provider: Optional[Union['BlockStateProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if direction is not None:
            self.components["direction"] = direction
        if allow_water is not None:
            self.components["allow_water"] = allow_water
        if height_distribution is not None:
            self.components["height_distribution"] = height_distribution
        if body_provider is not None:
            self.components["body_provider"] = body_provider
        if head_provider is not None:
            self.components["head_provider"] = head_provider

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

class GrowingPlantHeight:
    def __init__(
            self,
            weight: Optional[Union[int, Any]] = None,
            data: Optional[Union['IntProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if weight is not None:
            self.components["weight"] = weight
        if data is not None:
            self.components["data"] = data

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

class HugeFungusConfig:
    def __init__(
            self,
            hat_state: Optional[Union['BlockState', Any]] = None,
            decor_state: Optional[Union['BlockState', Any]] = None,
            stem_state: Optional[Union['BlockState', Any]] = None,
            valid_base_block: Optional[Union['BlockState', Any]] = None,
            planted: Optional[Union[bool, Any]] = None,
            replaceable_blocks: Optional[Union['BlockPredicate', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if hat_state is not None:
            self.components["hat_state"] = hat_state
        if decor_state is not None:
            self.components["decor_state"] = decor_state
        if stem_state is not None:
            self.components["stem_state"] = stem_state
        if valid_base_block is not None:
            self.components["valid_base_block"] = valid_base_block
        if planted is not None:
            self.components["planted"] = planted
        if replaceable_blocks is not None:
            self.components["replaceable_blocks"] = replaceable_blocks

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

class HugeMushroomConfig:
    def __init__(
            self,
            cap_provider: Optional[Union['BlockStateProvider', Any]] = None,
            stem_provider: Optional[Union['BlockStateProvider', Any]] = None,
            foliage_radius: Optional[Union[int, Any]] = None,
            can_place_on: Optional[Union['BlockPredicate', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if cap_provider is not None:
            self.components["cap_provider"] = cap_provider
        if stem_provider is not None:
            self.components["stem_provider"] = stem_provider
        if foliage_radius is not None:
            self.components["foliage_radius"] = foliage_radius
        if can_place_on is not None:
            self.components["can_place_on"] = can_place_on

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

class IcebergConfig:
    def __init__(
            self,
            state: Optional[Union['BlockState', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if state is not None:
            self.components["state"] = state

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

class LakeConfig:
    def __init__(
            self,
            state: Optional[Union['BlockState', Any]] = None,
            fluid: Optional[Union['BlockStateProvider', Any]] = None,
            barrier: Optional[Union['BlockStateProvider', Any]] = None,
            can_place_feature: Optional[Union['BlockPredicate', Any]] = None,
            can_replace_with_air_or_fluid: Optional[Union['BlockPredicate', Any]] = None,
            can_replace_with_barrier: Optional[Union['BlockPredicate', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if state is not None:
            self.components["state"] = state
        if fluid is not None:
            self.components["fluid"] = fluid
        if barrier is not None:
            self.components["barrier"] = barrier
        if can_place_feature is not None:
            self.components["can_place_feature"] = can_place_feature
        if can_replace_with_air_or_fluid is not None:
            self.components["can_replace_with_air_or_fluid"] = can_replace_with_air_or_fluid
        if can_replace_with_barrier is not None:
            self.components["can_replace_with_barrier"] = can_replace_with_barrier

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

class LargeDripstoneConfig:
    def __init__(
            self,
            replaceable_blocks: Optional[Union[Union[list[str], str], Any]] = None,
            floor_to_ceiling_search_range: Optional[Union[int, Any]] = None,
            column_radius: Optional[Union[Union['IntProvider', 'IntProvider'], Any]] = None,
            height_scale: Optional[Union['FloatProvider', Any]] = None,
            max_column_radius_to_cave_height_ratio: Optional[Union[float, Any]] = None,
            stalactite_bluntness: Optional[Union['FloatProvider', Any]] = None,
            stalagmite_bluntness: Optional[Union['FloatProvider', Any]] = None,
            wind_speed: Optional[Union['FloatProvider', Any]] = None,
            min_radius_for_wind: Optional[Union[int, Any]] = None,
            min_bluntness_for_wind: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if replaceable_blocks is not None:
            self.components["replaceable_blocks"] = replaceable_blocks
        if floor_to_ceiling_search_range is not None:
            self.components["floor_to_ceiling_search_range"] = floor_to_ceiling_search_range
        if column_radius is not None:
            self.components["column_radius"] = column_radius
        if height_scale is not None:
            self.components["height_scale"] = height_scale
        if max_column_radius_to_cave_height_ratio is not None:
            self.components["max_column_radius_to_cave_height_ratio"] = max_column_radius_to_cave_height_ratio
        if stalactite_bluntness is not None:
            self.components["stalactite_bluntness"] = stalactite_bluntness
        if stalagmite_bluntness is not None:
            self.components["stalagmite_bluntness"] = stalagmite_bluntness
        if wind_speed is not None:
            self.components["wind_speed"] = wind_speed
        if min_radius_for_wind is not None:
            self.components["min_radius_for_wind"] = min_radius_for_wind
        if min_bluntness_for_wind is not None:
            self.components["min_bluntness_for_wind"] = min_bluntness_for_wind

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

class MultifaceGrowthConfig:
    def __init__(
            self,
            search_range: Optional[Union[int, Any]] = None,
            chance_of_spreading: Optional[Union[float, Any]] = None,
            can_place_on_floor: Optional[Union[bool, Any]] = None,
            can_place_on_ceiling: Optional[Union[bool, Any]] = None,
            can_place_on_wall: Optional[Union[bool, Any]] = None,
            can_be_placed_on: Optional[Union[Union[list['BlockState'], list[str], str], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if search_range is not None:
            self.components["search_range"] = search_range
        if chance_of_spreading is not None:
            self.components["chance_of_spreading"] = chance_of_spreading
        if can_place_on_floor is not None:
            self.components["can_place_on_floor"] = can_place_on_floor
        if can_place_on_ceiling is not None:
            self.components["can_place_on_ceiling"] = can_place_on_ceiling
        if can_place_on_wall is not None:
            self.components["can_place_on_wall"] = can_place_on_wall
        if can_be_placed_on is not None:
            self.components["can_be_placed_on"] = can_be_placed_on

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

class NetherForestVegetationConfig:
    def __init__(
            self,
            state_provider: Optional[Union['BlockStateProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if state_provider is not None:
            self.components["state_provider"] = state_provider

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

class NetherrackReplaceBlobsConfig:
    def __init__(
            self,
            state: Optional[Union['BlockState', Any]] = None,
            target: Optional[Union['BlockState', Any]] = None,
            radius: Optional[Union[Union['UniformInt', 'IntProvider'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if state is not None:
            self.components["state"] = state
        if target is not None:
            self.components["target"] = target
        if radius is not None:
            self.components["radius"] = radius

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

class TargetBlock:
    def __init__(
            self,
            target: Optional[Union['RuleTest', Any]] = None,
            state: Optional[Union['BlockState', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if target is not None:
            self.components["target"] = target
        if state is not None:
            self.components["state"] = state

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

class OreConfig(TargetBlock):
    def __init__(
            self,
            targets: Optional[Union[list['TargetBlock'], Any]] = None,
            size: Optional[Union[int, Any]] = None,
            discard_chance_on_air_exposure: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if targets is not None:
            self.components["targets"] = targets
        if size is not None:
            self.components["size"] = size
        if discard_chance_on_air_exposure is not None:
            self.components["discard_chance_on_air_exposure"] = discard_chance_on_air_exposure

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

class OverlayConfig:
    def __init__(
            self,
            features: Optional[Union['PlacedFeatureListRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if features is not None:
            self.components["features"] = features

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

class ProbabilityConfig:
    def __init__(
            self,
            probability: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if probability is not None:
            self.components["probability"] = probability

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

class ProjectedSquareConfig:
    def __init__(
            self,
            block: Optional[Union['BlockStateProvider', Any]] = None,
            project_through: Optional[Union['BlockPredicate', Any]] = None,
            size: Optional[Union['IntProvider', Any]] = None,
            max_projection_height: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if block is not None:
            self.components["block"] = block
        if project_through is not None:
            self.components["project_through"] = project_through
        if size is not None:
            self.components["size"] = size
        if max_projection_height is not None:
            self.components["max_projection_height"] = max_projection_height

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

class RandomBooleanSelector:
    def __init__(
            self,
            feature_false: Optional[Union['FeatureRef', Any]] = None,
            feature_true: Optional[Union['FeatureRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if feature_false is not None:
            self.components["feature_false"] = feature_false
        if feature_true is not None:
            self.components["feature_true"] = feature_true

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

class RandomNeighborSpreadConfig:
    def __init__(
            self,
            block: Optional[Union['BlockStateProvider', Any]] = None,
            accepted_neighbors: Optional[Union[Union[str, list[str]], Any]] = None,
            can_replace: Optional[Union['BlockPredicate', Any]] = None,
            attempts: Optional[Union['IntProvider', Any]] = None,
            xz_offset: Optional[Union['IntProvider', Any]] = None,
            y_offset: Optional[Union['IntProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if block is not None:
            self.components["block"] = block
        if accepted_neighbors is not None:
            self.components["accepted_neighbors"] = accepted_neighbors
        if can_replace is not None:
            self.components["can_replace"] = can_replace
        if attempts is not None:
            self.components["attempts"] = attempts
        if xz_offset is not None:
            self.components["xz_offset"] = xz_offset
        if y_offset is not None:
            self.components["y_offset"] = y_offset

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

class RandomPatchConfig:
    def __init__(
            self,
            tries: Optional[Union[Union[int, int], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if tries is not None:
            self.components["tries"] = tries

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

class RandomSelector:
    def __init__(
            self,
            features: Optional[Union[list[{'chance': float, 'feature': 'FeatureRef'}], Any]] = None,
            default: Optional[Union['FeatureRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if features is not None:
            self.components["features"] = features
        if default is not None:
            self.components["default"] = default

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

class ReplaceSingleBlockConfig:
    def __init__(
            self,
            targets: Optional[Union[list['TargetBlock'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if targets is not None:
            self.components["targets"] = targets

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

class RootSystemConfig:
    def __init__(
            self,
            required_vertical_space_for_tree: Optional[Union[int, Any]] = None,
            level_test_distance: Optional[Union[int, Any]] = None,
            max_level_deviation: Optional[Union[int, Any]] = None,
            root_radius: Optional[Union[int, Any]] = None,
            root_placement_attempts: Optional[Union[int, Any]] = None,
            root_column_max_height: Optional[Union[int, Any]] = None,
            hanging_root_radius: Optional[Union[int, Any]] = None,
            hanging_roots_vertical_span: Optional[Union[int, Any]] = None,
            hanging_root_placement_attempts: Optional[Union[int, Any]] = None,
            allowed_vertical_water_for_tree: Optional[Union[int, Any]] = None,
            root_replaceable: Optional[Union[Union[str, str, str, list[str]], Any]] = None,
            root_state_provider: Optional[Union['BlockStateProvider', Any]] = None,
            hanging_root_state_provider: Optional[Union['BlockStateProvider', Any]] = None,
            allowed_tree_position: Optional[Union['BlockPredicate', Any]] = None,
            feature: Optional[Union['FeatureRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if required_vertical_space_for_tree is not None:
            self.components["required_vertical_space_for_tree"] = required_vertical_space_for_tree
        if level_test_distance is not None:
            self.components["level_test_distance"] = level_test_distance
        if max_level_deviation is not None:
            self.components["max_level_deviation"] = max_level_deviation
        if root_radius is not None:
            self.components["root_radius"] = root_radius
        if root_placement_attempts is not None:
            self.components["root_placement_attempts"] = root_placement_attempts
        if root_column_max_height is not None:
            self.components["root_column_max_height"] = root_column_max_height
        if hanging_root_radius is not None:
            self.components["hanging_root_radius"] = hanging_root_radius
        if hanging_roots_vertical_span is not None:
            self.components["hanging_roots_vertical_span"] = hanging_roots_vertical_span
        if hanging_root_placement_attempts is not None:
            self.components["hanging_root_placement_attempts"] = hanging_root_placement_attempts
        if allowed_vertical_water_for_tree is not None:
            self.components["allowed_vertical_water_for_tree"] = allowed_vertical_water_for_tree
        if root_replaceable is not None:
            self.components["root_replaceable"] = root_replaceable
        if root_state_provider is not None:
            self.components["root_state_provider"] = root_state_provider
        if hanging_root_state_provider is not None:
            self.components["hanging_root_state_provider"] = hanging_root_state_provider
        if allowed_tree_position is not None:
            self.components["allowed_tree_position"] = allowed_tree_position
        if feature is not None:
            self.components["feature"] = feature

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

class RuleBasedBlockStateProvider:
    def __init__(
            self,
            rules: Optional[Union[list[{'if_true': 'BlockPredicate', 'then': 'BlockStateProvider'}], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if rules is not None:
            self.components["rules"] = rules

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

class SculkPatchConfig:
    def __init__(
            self,
            charge_count: Optional[Union[int, Any]] = None,
            amount_per_charge: Optional[Union[int, Any]] = None,
            spread_attempts: Optional[Union[int, Any]] = None,
            growth_rounds: Optional[Union[int, Any]] = None,
            spread_rounds: Optional[Union[int, Any]] = None,
            extra_rare_growths: Optional[Union['IntProvider', Any]] = None,
            catalyst_chance: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if charge_count is not None:
            self.components["charge_count"] = charge_count
        if amount_per_charge is not None:
            self.components["amount_per_charge"] = amount_per_charge
        if spread_attempts is not None:
            self.components["spread_attempts"] = spread_attempts
        if growth_rounds is not None:
            self.components["growth_rounds"] = growth_rounds
        if spread_rounds is not None:
            self.components["spread_rounds"] = spread_rounds
        if extra_rare_growths is not None:
            self.components["extra_rare_growths"] = extra_rare_growths
        if catalyst_chance is not None:
            self.components["catalyst_chance"] = catalyst_chance

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

class SeaPickleConfig:
    def __init__(
            self,
            count: Optional[Union[Union['UniformInt', 'IntProvider'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if count is not None:
            self.components["count"] = count

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

class SequenceConfig:
    def __init__(
            self,
            features: Optional[Union['PlacedFeatureListRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if features is not None:
            self.components["features"] = features

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

class SimpleBlockConfig:
    def __init__(
            self,
            to_place: Optional[Union[Union['BlockState', 'BlockStateProvider'], Any]] = None,
            schedule_tick: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if to_place is not None:
            self.components["to_place"] = to_place
        if schedule_tick is not None:
            self.components["schedule_tick"] = schedule_tick

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

class SimpleRandomSelectorConfig:
    def __init__(
            self,
            features: Optional[Union[Union[list['FeatureRef'], 'PlacedFeatureListRef'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if features is not None:
            self.components["features"] = features

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

class SingleBlockPillarConfig:
    def __init__(
            self,
            block: Optional[Union['BlockStateProvider', Any]] = None,
            can_replace: Optional[Union['BlockPredicate', Any]] = None,
            direction: Optional[Union[str, Any]] = None,
            chance_to_continue: Optional[Union[float, Any]] = None,
            cap_feature: Optional[Union['PlacedFeatureRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if block is not None:
            self.components["block"] = block
        if can_replace is not None:
            self.components["can_replace"] = can_replace
        if direction is not None:
            self.components["direction"] = direction
        if chance_to_continue is not None:
            self.components["chance_to_continue"] = chance_to_continue
        if cap_feature is not None:
            self.components["cap_feature"] = cap_feature

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

class SmallDripstoneConfig:
    def __init__(
            self,
            max_placements: Optional[Union[int, Any]] = None,
            empty_space_search_radius: Optional[Union[int, Any]] = None,
            max_offset_from_origin: Optional[Union[int, Any]] = None,
            chance_of_taller_dripstone: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if max_placements is not None:
            self.components["max_placements"] = max_placements
        if empty_space_search_radius is not None:
            self.components["empty_space_search_radius"] = empty_space_search_radius
        if max_offset_from_origin is not None:
            self.components["max_offset_from_origin"] = max_offset_from_origin
        if chance_of_taller_dripstone is not None:
            self.components["chance_of_taller_dripstone"] = chance_of_taller_dripstone

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

class SpeleothemClusterConfig:
    def __init__(
            self,
            base_block: Optional[Union['BlockState', Any]] = None,
            pointed_block: Optional[Union['BlockState', Any]] = None,
            replaceable_blocks: Optional[Union[Union[list[str], str], Any]] = None,
            floor_to_ceiling_search_range: Optional[Union[int, Any]] = None,
            height: Optional[Union['IntProvider', Any]] = None,
            radius: Optional[Union['IntProvider', Any]] = None,
            max_stalagmite_stalactite_height_diff: Optional[Union[int, Any]] = None,
            height_deviation: Optional[Union[int, Any]] = None,
            dripstone_block_layer_thickness: Optional[Union['IntProvider', Any]] = None,
            speleothem_block_layer_thickness: Optional[Union['IntProvider', Any]] = None,
            density: Optional[Union['FloatProvider', Any]] = None,
            wetness: Optional[Union['FloatProvider', Any]] = None,
            chance_of_dripstone_column_at_max_distance_from_center: Optional[Union[float, Any]] = None,
            chance_of_speleothem_at_max_distance_from_center: Optional[Union[float, Any]] = None,
            max_distance_from_edge_affecting_chance_of_dripstone_column: Optional[Union[int, Any]] = None,
            max_distance_from_edge_affecting_chance_of_speleothem: Optional[Union[int, Any]] = None,
            max_distance_from_center_affecting_height_bias: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if base_block is not None:
            self.components["base_block"] = base_block
        if pointed_block is not None:
            self.components["pointed_block"] = pointed_block
        if replaceable_blocks is not None:
            self.components["replaceable_blocks"] = replaceable_blocks
        if floor_to_ceiling_search_range is not None:
            self.components["floor_to_ceiling_search_range"] = floor_to_ceiling_search_range
        if height is not None:
            self.components["height"] = height
        if radius is not None:
            self.components["radius"] = radius
        if max_stalagmite_stalactite_height_diff is not None:
            self.components["max_stalagmite_stalactite_height_diff"] = max_stalagmite_stalactite_height_diff
        if height_deviation is not None:
            self.components["height_deviation"] = height_deviation
        if dripstone_block_layer_thickness is not None:
            self.components["dripstone_block_layer_thickness"] = dripstone_block_layer_thickness
        if speleothem_block_layer_thickness is not None:
            self.components["speleothem_block_layer_thickness"] = speleothem_block_layer_thickness
        if density is not None:
            self.components["density"] = density
        if wetness is not None:
            self.components["wetness"] = wetness
        if chance_of_dripstone_column_at_max_distance_from_center is not None:
            self.components["chance_of_dripstone_column_at_max_distance_from_center"] = chance_of_dripstone_column_at_max_distance_from_center
        if chance_of_speleothem_at_max_distance_from_center is not None:
            self.components["chance_of_speleothem_at_max_distance_from_center"] = chance_of_speleothem_at_max_distance_from_center
        if max_distance_from_edge_affecting_chance_of_dripstone_column is not None:
            self.components["max_distance_from_edge_affecting_chance_of_dripstone_column"] = max_distance_from_edge_affecting_chance_of_dripstone_column
        if max_distance_from_edge_affecting_chance_of_speleothem is not None:
            self.components["max_distance_from_edge_affecting_chance_of_speleothem"] = max_distance_from_edge_affecting_chance_of_speleothem
        if max_distance_from_center_affecting_height_bias is not None:
            self.components["max_distance_from_center_affecting_height_bias"] = max_distance_from_center_affecting_height_bias

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

class SpeleothemConfig:
    def __init__(
            self,
            base_block: Optional[Union['BlockState', Any]] = None,
            pointed_block: Optional[Union['BlockState', Any]] = None,
            replaceable_blocks: Optional[Union[Union[list[str], str], Any]] = None,
            chance_of_taller_dripstone: Optional[Union[float, Any]] = None,
            chance_of_taller_generation: Optional[Union[float, Any]] = None,
            chance_of_directional_spread: Optional[Union[float, Any]] = None,
            chance_of_spread_radius2: Optional[Union[float, Any]] = None,
            chance_of_spread_radius3: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if base_block is not None:
            self.components["base_block"] = base_block
        if pointed_block is not None:
            self.components["pointed_block"] = pointed_block
        if replaceable_blocks is not None:
            self.components["replaceable_blocks"] = replaceable_blocks
        if chance_of_taller_dripstone is not None:
            self.components["chance_of_taller_dripstone"] = chance_of_taller_dripstone
        if chance_of_taller_generation is not None:
            self.components["chance_of_taller_generation"] = chance_of_taller_generation
        if chance_of_directional_spread is not None:
            self.components["chance_of_directional_spread"] = chance_of_directional_spread
        if chance_of_spread_radius2 is not None:
            self.components["chance_of_spread_radius2"] = chance_of_spread_radius2
        if chance_of_spread_radius3 is not None:
            self.components["chance_of_spread_radius3"] = chance_of_spread_radius3

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

class SpikeConfig:
    def __init__(
            self,
            state: Optional[Union['BlockState', Any]] = None,
            can_place_on: Optional[Union['BlockPredicate', Any]] = None,
            can_replace: Optional[Union['BlockPredicate', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if state is not None:
            self.components["state"] = state
        if can_place_on is not None:
            self.components["can_place_on"] = can_place_on
        if can_replace is not None:
            self.components["can_replace"] = can_replace

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

class SpringConfig:
    def __init__(
            self,
            state: Optional[Union['FluidState', Any]] = None,
            rock_count: Optional[Union[int, Any]] = None,
            hole_count: Optional[Union[int, Any]] = None,
            requires_block_below: Optional[Union[bool, Any]] = None,
            valid_blocks: Optional[Union[Union[list[str], str], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if state is not None:
            self.components["state"] = state
        if rock_count is not None:
            self.components["rock_count"] = rock_count
        if hole_count is not None:
            self.components["hole_count"] = hole_count
        if requires_block_below is not None:
            self.components["requires_block_below"] = requires_block_below
        if valid_blocks is not None:
            self.components["valid_blocks"] = valid_blocks

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

class TemplateConfig:
    def __init__(
            self,
            templates: Optional[Union['WeightedList', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if templates is not None:
            self.components["templates"] = templates

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

class TwistingVinesConfig:
    def __init__(
            self,
            spread_width: Optional[Union[int, Any]] = None,
            spread_height: Optional[Union[int, Any]] = None,
            max_height: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if spread_width is not None:
            self.components["spread_width"] = spread_width
        if spread_height is not None:
            self.components["spread_height"] = spread_height
        if max_height is not None:
            self.components["max_height"] = max_height

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

class UnderwaterMagmaConfig:
    def __init__(
            self,
            floor_search_range: Optional[Union[int, Any]] = None,
            placement_radius_around_floor: Optional[Union[int, Any]] = None,
            placement_probability_per_valid_position: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if floor_search_range is not None:
            self.components["floor_search_range"] = floor_search_range
        if placement_radius_around_floor is not None:
            self.components["placement_radius_around_floor"] = placement_radius_around_floor
        if placement_probability_per_valid_position is not None:
            self.components["placement_probability_per_valid_position"] = placement_probability_per_valid_position

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

class VegetationPatchConfig:
    def __init__(
            self,
            surface: Optional[Union['CaveSurface', Any]] = None,
            depth: Optional[Union['IntProvider', Any]] = None,
            vertical_range: Optional[Union[int, Any]] = None,
            extra_bottom_block_chance: Optional[Union[float, Any]] = None,
            extra_edge_column_chance: Optional[Union[float, Any]] = None,
            vegetation_chance: Optional[Union[float, Any]] = None,
            xz_radius: Optional[Union['IntProvider', Any]] = None,
            replaceable: Optional[Union[Union[str, str, str, list[str]], Any]] = None,
            ground_state: Optional[Union['BlockStateProvider', Any]] = None,
            vegetation_feature: Optional[Union['FeatureRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if surface is not None:
            self.components["surface"] = surface
        if depth is not None:
            self.components["depth"] = depth
        if vertical_range is not None:
            self.components["vertical_range"] = vertical_range
        if extra_bottom_block_chance is not None:
            self.components["extra_bottom_block_chance"] = extra_bottom_block_chance
        if extra_edge_column_chance is not None:
            self.components["extra_edge_column_chance"] = extra_edge_column_chance
        if vegetation_chance is not None:
            self.components["vegetation_chance"] = vegetation_chance
        if xz_radius is not None:
            self.components["xz_radius"] = xz_radius
        if replaceable is not None:
            self.components["replaceable"] = replaceable
        if ground_state is not None:
            self.components["ground_state"] = ground_state
        if vegetation_feature is not None:
            self.components["vegetation_feature"] = vegetation_feature

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

class WeightedRandomFeatureConfig:
    def __init__(
            self,
            features: Optional[Union['WeightedList', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if features is not None:
            self.components["features"] = features

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

class BlockPredicate:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type

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

class BlockStateProvider:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type

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

class ConfiguredDecorator:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            config: Optional[Union[Any, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type
        if config is not None:
            self.components["config"] = config

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

class PlacedFeature:
    def __init__(
            self,
            feature: Optional[Union['ConfiguredFeatureRef', Any]] = None,
            placement: Optional[Union[list['PlacementModifier'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if feature is not None:
            self.components["feature"] = feature
        if placement is not None:
            self.components["placement"] = placement

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

PlacedFeatureListRef = Union[Union['PlacedFeature', list['PlacedFeature'], str, list[Union[str, 'PlacedFeature']]], Any]

PlacedFeatureRef = Union[Union['PlacedFeature', str], Any]

class PlacementModifier:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type

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

class AboveRootPlacement:
    def __init__(
            self,
            above_root_provider: Optional[Union['BlockStateProvider', Any]] = None,
            above_root_placement_chance: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if above_root_provider is not None:
            self.components["above_root_provider"] = above_root_provider
        if above_root_placement_chance is not None:
            self.components["above_root_placement_chance"] = above_root_placement_chance

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

class FallenTreeConfig:
    def __init__(
            self,
            trunk_provider: Optional[Union['BlockStateProvider', Any]] = None,
            log_length: Optional[Union['IntProvider', Any]] = None,
            stump_decorators: Optional[Union[list['TreeDecorator'], Any]] = None,
            log_decorators: Optional[Union[list['TreeDecorator'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if trunk_provider is not None:
            self.components["trunk_provider"] = trunk_provider
        if log_length is not None:
            self.components["log_length"] = log_length
        if stump_decorators is not None:
            self.components["stump_decorators"] = stump_decorators
        if log_decorators is not None:
            self.components["log_decorators"] = log_decorators

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

class FeatureSize:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type

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

class FoliagePlacer:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            radius: Optional[Union[Union['UniformInt', 'IntProvider'], Any]] = None,
            offset: Optional[Union[Union['UniformInt', 'IntProvider'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type
        if radius is not None:
            self.components["radius"] = radius
        if offset is not None:
            self.components["offset"] = offset

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

class RootPlacer:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            root_provider: Optional[Union['BlockStateProvider', Any]] = None,
            trunk_offset_y: Optional[Union['IntProvider', Any]] = None,
            above_root_placement: Optional[Union['AboveRootPlacement', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type
        if root_provider is not None:
            self.components["root_provider"] = root_provider
        if trunk_offset_y is not None:
            self.components["trunk_offset_y"] = trunk_offset_y
        if above_root_placement is not None:
            self.components["above_root_placement"] = above_root_placement

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

class TreeConfig:
    def __init__(
            self,
            max_water_depth: Optional[Union[int, Any]] = None,
            ignore_vines: Optional[Union[bool, Any]] = None,
            heightmap: Optional[Union[str, Any]] = None,
            minimum_size: Optional[Union['FeatureSize', Any]] = None,
            force_dirt: Optional[Union[bool, Any]] = None,
            dirt_provider: Optional[Union['BlockStateProvider', Any]] = None,
            sapling_provider: Optional[Union['BlockStateProvider', Any]] = None,
            trunk_provider: Optional[Union['BlockStateProvider', Any]] = None,
            leaves_provider: Optional[Union['BlockStateProvider', Any]] = None,
            foliage_provider: Optional[Union['BlockStateProvider', Any]] = None,
            root_placer: Optional[Union['RootPlacer', Any]] = None,
            trunk_placer: Optional[Union['TrunkPlacer', Any]] = None,
            foliage_placer: Optional[Union['FoliagePlacer', Any]] = None,
            decorators: Optional[Union[list['TreeDecorator'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if max_water_depth is not None:
            self.components["max_water_depth"] = max_water_depth
        if ignore_vines is not None:
            self.components["ignore_vines"] = ignore_vines
        if heightmap is not None:
            self.components["heightmap"] = heightmap
        if minimum_size is not None:
            self.components["minimum_size"] = minimum_size
        if force_dirt is not None:
            self.components["force_dirt"] = force_dirt
        if dirt_provider is not None:
            self.components["dirt_provider"] = dirt_provider
        if sapling_provider is not None:
            self.components["sapling_provider"] = sapling_provider
        if trunk_provider is not None:
            self.components["trunk_provider"] = trunk_provider
        if leaves_provider is not None:
            self.components["leaves_provider"] = leaves_provider
        if foliage_provider is not None:
            self.components["foliage_provider"] = foliage_provider
        if root_placer is not None:
            self.components["root_placer"] = root_placer
        if trunk_placer is not None:
            self.components["trunk_placer"] = trunk_placer
        if foliage_placer is not None:
            self.components["foliage_placer"] = foliage_placer
        if decorators is not None:
            self.components["decorators"] = decorators

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

class TreeDecorator:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type

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

class TrunkPlacer:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            base_height: Optional[Union[int, Any]] = None,
            height_rand_a: Optional[Union[int, Any]] = None,
            height_rand_b: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type
        if base_height is not None:
            self.components["base_height"] = base_height
        if height_rand_a is not None:
            self.components["height_rand_a"] = height_rand_a
        if height_rand_b is not None:
            self.components["height_rand_b"] = height_rand_b

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

class Processor:
    def __init__(
            self,
            processor_type: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if processor_type is not None:
            self.components["processor_type"] = processor_type

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

ProcessorList = Union[Union[list['Processor'], {'processors': list['Processor']}], Any]

ProcessorListRef = Union[Union[str, 'ProcessorList'], Any]

class RuleTest:
    def __init__(
            self,
            predicate_type: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if predicate_type is not None:
            self.components["predicate_type"] = predicate_type

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

class BlockState:
    def __init__(
            self,
            Name: Optional[Union[str, Any]] = None,
            Properties: Optional[Union[Any, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if Name is not None:
            self.components["Name"] = Name
        if Properties is not None:
            self.components["Properties"] = Properties

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

class FluidState:
    def __init__(
            self,
            Name: Optional[Union[str, Any]] = None,
            Properties: Optional[Union[Any, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if Name is not None:
            self.components["Name"] = Name
        if Properties is not None:
            self.components["Properties"] = Properties

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

