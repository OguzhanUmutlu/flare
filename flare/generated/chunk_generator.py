### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

CubicSpline = Union[Union[float, {'coordinate': Union[str, 'DensityFunctionRef'], 'points': list['SplinePoint']}], Any]

DensityFunction = Union[Union['NoiseRange', {'type': str}], Any]

DensityFunctionRef = Union[Union[str, 'DensityFunction'], Any]

class SplinePoint:
    def __init__(
            self,
            location: Optional[Union[float, Any]] = None,
            derivative: Optional[Union[float, Any]] = None,
            value: Optional[Union['CubicSpline', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if location is not None:
            self.components["location"] = location
        if derivative is not None:
            self.components["derivative"] = derivative
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

class BiomeSource:
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

ClimateParameter = Union[Union[float, list[float]], Any]

class ClimateParameters:
    def __init__(
            self,
            temperature: Optional[Union['ClimateParameter', Any]] = None,
            humidity: Optional[Union['ClimateParameter', Any]] = None,
            altitude: Optional[Union[float, Any]] = None,
            continentalness: Optional[Union['ClimateParameter', Any]] = None,
            erosion: Optional[Union['ClimateParameter', Any]] = None,
            weirdness: Optional[Union['ClimateParameter', Any]] = None,
            depth: Optional[Union['ClimateParameter', Any]] = None,
            offset: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if temperature is not None:
            self.components["temperature"] = temperature
        if humidity is not None:
            self.components["humidity"] = humidity
        if altitude is not None:
            self.components["altitude"] = altitude
        if continentalness is not None:
            self.components["continentalness"] = continentalness
        if erosion is not None:
            self.components["erosion"] = erosion
        if weirdness is not None:
            self.components["weirdness"] = weirdness
        if depth is not None:
            self.components["depth"] = depth
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

class Flat:
    def __init__(
            self,
            settings: Optional[Union['FlatGeneratorSettings', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if settings is not None:
            self.components["settings"] = settings

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

class FlatGeneratorLayer:
    def __init__(
            self,
            height: Optional[Union[int, Any]] = None,
            block: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if height is not None:
            self.components["height"] = height
        if block is not None:
            self.components["block"] = block

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

class FlatGeneratorSettings:
    def __init__(
            self,
            biome: Optional[Union[str, Any]] = None,
            lakes: Optional[Union[bool, Any]] = None,
            features: Optional[Union[bool, Any]] = None,
            layers: Optional[Union[list['FlatGeneratorLayer'], Any]] = None,
            structures: Optional[Union['StructureSettings', Any]] = None,
            structure_overrides: Optional[Union[Union[list[str], str], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if biome is not None:
            self.components["biome"] = biome
        if lakes is not None:
            self.components["lakes"] = lakes
        if features is not None:
            self.components["features"] = features
        if layers is not None:
            self.components["layers"] = layers
        if structures is not None:
            self.components["structures"] = structures
        if structure_overrides is not None:
            self.components["structure_overrides"] = structure_overrides

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

class Noise:
    def __init__(
            self,
            seed: Optional[Union[long, Any]] = None,
            settings: Optional[Union['NoiseGeneratorSettingsRef', Any]] = None,
            biome_source: Optional[Union['BiomeSource', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if seed is not None:
            self.components["seed"] = seed
        if settings is not None:
            self.components["settings"] = settings
        if biome_source is not None:
            self.components["biome_source"] = biome_source

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

class MaterialRule:
    def __init__(
            self,
            type: Optional[Union[Union[str, str], Any]] = None,
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

MaterialRuleRef = Union[Union[str, 'MaterialRule'], Any]

class Aquifer:
    def __init__(
            self,
            barrier: Optional[Union['DensityFunctionRef', Any]] = None,
            fluid_level_floodedness: Optional[Union['DensityFunctionRef', Any]] = None,
            fluid_level_spread: Optional[Union['DensityFunctionRef', Any]] = None,
            lava: Optional[Union['DensityFunctionRef', Any]] = None,
            exclusion: Optional[Union['DensityFunctionRef', Any]] = None,
            surface_level: Optional[Union['DensityFunctionRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if barrier is not None:
            self.components["barrier"] = barrier
        if fluid_level_floodedness is not None:
            self.components["fluid_level_floodedness"] = fluid_level_floodedness
        if fluid_level_spread is not None:
            self.components["fluid_level_spread"] = fluid_level_spread
        if lava is not None:
            self.components["lava"] = lava
        if exclusion is not None:
            self.components["exclusion"] = exclusion
        if surface_level is not None:
            self.components["surface_level"] = surface_level

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

class NoiseGeneratorSettings:
    def __init__(
            self,
            default_block: Optional[Union['BlockState', Any]] = None,
            default_fluid: Optional[Union['BlockState', Any]] = None,
            bedrock_roof_position: Optional[Union[Union[int, int], Any]] = None,
            bedrock_floor_position: Optional[Union[Union[int, int], Any]] = None,
            sea_level: Optional[Union[Union[int, int], Any]] = None,
            min_surface_level: Optional[Union[int, Any]] = None,
            disable_mob_generation: Optional[Union[bool, Any]] = None,
            aquifers: Optional[Union['Aquifer', Any]] = None,
            ore_veins: Optional[Union[list['OreVeinifier'], Any]] = None,
            legacy_random_source: Optional[Union[bool, Any]] = None,
            noise: Optional[Union['NoiseSettings', Any]] = None,
            noise_router: Optional[Union['NoiseRouter', Any]] = None,
            spawn_target: Optional[Union[Union[list['ClimateParameters'], list['SpawnTargetPoint']], Any]] = None,
            surface_rule: Optional[Union['MaterialRuleRef', Any]] = None,
            material_rule: Optional[Union['MaterialRuleRef', Any]] = None,
            structures: Optional[Union['StructureSettings', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if default_block is not None:
            self.components["default_block"] = default_block
        if default_fluid is not None:
            self.components["default_fluid"] = default_fluid
        if bedrock_roof_position is not None:
            self.components["bedrock_roof_position"] = bedrock_roof_position
        if bedrock_floor_position is not None:
            self.components["bedrock_floor_position"] = bedrock_floor_position
        if sea_level is not None:
            self.components["sea_level"] = sea_level
        if min_surface_level is not None:
            self.components["min_surface_level"] = min_surface_level
        if disable_mob_generation is not None:
            self.components["disable_mob_generation"] = disable_mob_generation
        if aquifers is not None:
            self.components["aquifers"] = aquifers
        if ore_veins is not None:
            self.components["ore_veins"] = ore_veins
        if legacy_random_source is not None:
            self.components["legacy_random_source"] = legacy_random_source
        if noise is not None:
            self.components["noise"] = noise
        if noise_router is not None:
            self.components["noise_router"] = noise_router
        if spawn_target is not None:
            self.components["spawn_target"] = spawn_target
        if surface_rule is not None:
            self.components["surface_rule"] = surface_rule
        if material_rule is not None:
            self.components["material_rule"] = material_rule
        if structures is not None:
            self.components["structures"] = structures

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

NoiseGeneratorSettingsRef = Union[Union[str, {'name': str}], Any]

class NoiseRouter:
    def __init__(
            self,
            barrier: Optional[Union['DensityFunctionRef', Any]] = None,
            fluid_level_floodedness: Optional[Union['DensityFunctionRef', Any]] = None,
            fluid_level_spread: Optional[Union['DensityFunctionRef', Any]] = None,
            lava: Optional[Union['DensityFunctionRef', Any]] = None,
            vein_toggle: Optional[Union['DensityFunctionRef', Any]] = None,
            vein_ridged: Optional[Union['DensityFunctionRef', Any]] = None,
            vein_gap: Optional[Union['DensityFunctionRef', Any]] = None,
            temperature: Optional[Union['DensityFunctionRef', Any]] = None,
            vegetation: Optional[Union['DensityFunctionRef', Any]] = None,
            continents: Optional[Union['DensityFunctionRef', Any]] = None,
            erosion: Optional[Union['DensityFunctionRef', Any]] = None,
            depth: Optional[Union['DensityFunctionRef', Any]] = None,
            ridges: Optional[Union['DensityFunctionRef', Any]] = None,
            initial_density_without_jaggedness: Optional[Union['DensityFunctionRef', Any]] = None,
            preliminary_surface_level: Optional[Union['DensityFunctionRef', Any]] = None,
            final_density: Optional[Union['DensityFunctionRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if barrier is not None:
            self.components["barrier"] = barrier
        if fluid_level_floodedness is not None:
            self.components["fluid_level_floodedness"] = fluid_level_floodedness
        if fluid_level_spread is not None:
            self.components["fluid_level_spread"] = fluid_level_spread
        if lava is not None:
            self.components["lava"] = lava
        if vein_toggle is not None:
            self.components["vein_toggle"] = vein_toggle
        if vein_ridged is not None:
            self.components["vein_ridged"] = vein_ridged
        if vein_gap is not None:
            self.components["vein_gap"] = vein_gap
        if temperature is not None:
            self.components["temperature"] = temperature
        if vegetation is not None:
            self.components["vegetation"] = vegetation
        if continents is not None:
            self.components["continents"] = continents
        if erosion is not None:
            self.components["erosion"] = erosion
        if depth is not None:
            self.components["depth"] = depth
        if ridges is not None:
            self.components["ridges"] = ridges
        if initial_density_without_jaggedness is not None:
            self.components["initial_density_without_jaggedness"] = initial_density_without_jaggedness
        if preliminary_surface_level is not None:
            self.components["preliminary_surface_level"] = preliminary_surface_level
        if final_density is not None:
            self.components["final_density"] = final_density

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

class NoiseSamplingSettings:
    def __init__(
            self,
            xz_scale: Optional[Union[double, Any]] = None,
            y_scale: Optional[Union[double, Any]] = None,
            xz_factor: Optional[Union[double, Any]] = None,
            y_factor: Optional[Union[double, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if xz_scale is not None:
            self.components["xz_scale"] = xz_scale
        if y_scale is not None:
            self.components["y_scale"] = y_scale
        if xz_factor is not None:
            self.components["xz_factor"] = xz_factor
        if y_factor is not None:
            self.components["y_factor"] = y_factor

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

class NoiseSettings:
    def __init__(
            self,
            min_y: Optional[Union[int, Any]] = None,
            height: Optional[Union[Union[int, int], Any]] = None,
            size_horizontal: Optional[Union[int, Any]] = None,
            size_vertical: Optional[Union[int, Any]] = None,
            density_factor: Optional[Union[double, Any]] = None,
            density_offset: Optional[Union[double, Any]] = None,
            sampling: Optional[Union['NoiseSamplingSettings', Any]] = None,
            top_slide: Optional[Union['NoiseSlideSettings', Any]] = None,
            bottom_slide: Optional[Union['NoiseSlideSettings', Any]] = None,
            terrain_shaper: Optional[Union['TerrainShaper', Any]] = None,
            simplex_surface_noise: Optional[Union[bool, Any]] = None,
            random_density_offset: Optional[Union[bool, Any]] = None,
            island_noise_override: Optional[Union[bool, Any]] = None,
            amplified: Optional[Union[bool, Any]] = None,
            large_biomes: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if min_y is not None:
            self.components["min_y"] = min_y
        if height is not None:
            self.components["height"] = height
        if size_horizontal is not None:
            self.components["size_horizontal"] = size_horizontal
        if size_vertical is not None:
            self.components["size_vertical"] = size_vertical
        if density_factor is not None:
            self.components["density_factor"] = density_factor
        if density_offset is not None:
            self.components["density_offset"] = density_offset
        if sampling is not None:
            self.components["sampling"] = sampling
        if top_slide is not None:
            self.components["top_slide"] = top_slide
        if bottom_slide is not None:
            self.components["bottom_slide"] = bottom_slide
        if terrain_shaper is not None:
            self.components["terrain_shaper"] = terrain_shaper
        if simplex_surface_noise is not None:
            self.components["simplex_surface_noise"] = simplex_surface_noise
        if random_density_offset is not None:
            self.components["random_density_offset"] = random_density_offset
        if island_noise_override is not None:
            self.components["island_noise_override"] = island_noise_override
        if amplified is not None:
            self.components["amplified"] = amplified
        if large_biomes is not None:
            self.components["large_biomes"] = large_biomes

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

class NoiseSlideSettings:
    def __init__(
            self,
            target: Optional[Union[float, Any]] = None,
            size: Optional[Union[int, Any]] = None,
            offset: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if target is not None:
            self.components["target"] = target
        if size is not None:
            self.components["size"] = size
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

class OreVeinifier:
    def __init__(
            self,
            ore_block: Optional[Union['BlockState', Any]] = None,
            raw_ore_block: Optional[Union['BlockState', Any]] = None,
            filler_block: Optional[Union['BlockState', Any]] = None,
            raw_ore_chance: Optional[Union[float, Any]] = None,
            density: Optional[Union['DensityFunctionRef', Any]] = None,
            richness: Optional[Union['DensityFunctionRef', Any]] = None,
            filler_gap: Optional[Union['DensityFunctionRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if ore_block is not None:
            self.components["ore_block"] = ore_block
        if raw_ore_block is not None:
            self.components["raw_ore_block"] = raw_ore_block
        if filler_block is not None:
            self.components["filler_block"] = filler_block
        if raw_ore_chance is not None:
            self.components["raw_ore_chance"] = raw_ore_chance
        if density is not None:
            self.components["density"] = density
        if richness is not None:
            self.components["richness"] = richness
        if filler_gap is not None:
            self.components["filler_gap"] = filler_gap

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

class SpawnTargetPoint:
    def __init__(
            self,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)

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

class StructureSettings:
    def __init__(
            self,
            stronghold: Optional[Union['ConcentricRingsPlacement', Any]] = None,
            structures: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if stronghold is not None:
            self.components["stronghold"] = stronghold
        if structures is not None:
            self.components["structures"] = structures

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

class TerrainShaper:
    def __init__(
            self,
            offset: Optional[Union['CubicSpline', Any]] = None,
            factor: Optional[Union['CubicSpline', Any]] = None,
            jaggedness: Optional[Union['CubicSpline', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if offset is not None:
            self.components["offset"] = offset
        if factor is not None:
            self.components["factor"] = factor
        if jaggedness is not None:
            self.components["jaggedness"] = jaggedness

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

class ConcentricRingsPlacement:
    def __init__(
            self,
            distance: Optional[Union[int, Any]] = None,
            spread: Optional[Union[int, Any]] = None,
            count: Optional[Union[int, Any]] = None,
            preferred_biomes: Optional[Union[Union[list[str], str], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if distance is not None:
            self.components["distance"] = distance
        if spread is not None:
            self.components["spread"] = spread
        if count is not None:
            self.components["count"] = count
        if preferred_biomes is not None:
            self.components["preferred_biomes"] = preferred_biomes

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

class RandomSpreadPlacement:
    def __init__(
            self,
            spacing: Optional[Union[int, Any]] = None,
            separation: Optional[Union[int, Any]] = None,
            salt: Optional[Union[int, Any]] = None,
            spread_type: Optional[Union[str, Any]] = None,
            locate_offset: Optional[Union[list[int], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if spacing is not None:
            self.components["spacing"] = spacing
        if separation is not None:
            self.components["separation"] = separation
        if salt is not None:
            self.components["salt"] = salt
        if spread_type is not None:
            self.components["spread_type"] = spread_type
        if locate_offset is not None:
            self.components["locate_offset"] = locate_offset

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

