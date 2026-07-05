### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class Atlas:
    def __init__(
            self,
            sources: Optional[Union[list['SpriteSource'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if sources is not None:
            self.components["sources"] = sources

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

class SpriteSource:
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

BlockStateDefinition = Union[Union[{'variants': dict}, {'multipart': list[{'when': 'MultiPartCondition', 'apply': 'ModelVariant'}]}], Any]

ModelVariant = Union[Union['ModelVariantBase', list[{'weight': int}]], Any]

class ModelVariantBase:
    def __init__(
            self,
            model: Optional[Union['ModelRef', Any]] = None,
            x: Optional[Union[Union[Any, Any, Any, Any], Any]] = None,
            y: Optional[Union[Union[Any, Any, Any, Any], Any]] = None,
            z: Optional[Union[Union[Any, Any, Any, Any], Any]] = None,
            uvlock: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if model is not None:
            self.components["model"] = model
        if x is not None:
            self.components["x"] = x
        if y is not None:
            self.components["y"] = y
        if z is not None:
            self.components["z"] = z
        if uvlock is not None:
            self.components["uvlock"] = uvlock

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

MultiPartCondition = Union[Union[{'OR': list['MultiPartCondition']}, dict], Any]

class Equipment:
    def __init__(
            self,
            layers: Optional[Union['Layers', Any]] = None,
            trim_palette_replacements: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if layers is not None:
            self.components["layers"] = layers
        if trim_palette_replacements is not None:
            self.components["trim_palette_replacements"] = trim_palette_replacements

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

class Layers:
    def __init__(
            self,
            humanoid: Optional[Union[list['Layer'], Any]] = None,
            humanoid_leggings: Optional[Union[list['Layer'], Any]] = None,
            humanoid_baby: Optional[Union[list['Layer'], Any]] = None,
            wings: Optional[Union[list['WingsLayer'], Any]] = None,
            wolf_body: Optional[Union[list['Layer'], Any]] = None,
            horse_body: Optional[Union[list['Layer'], Any]] = None,
            llama_body: Optional[Union[list['Layer'], Any]] = None,
            happy_ghast_body: Optional[Union[list['Layer'], Any]] = None,
            nautilus_saddle: Optional[Union[list['Layer'], Any]] = None,
            nautilus_body: Optional[Union[list['Layer'], Any]] = None,
            pig_saddle: Optional[Union[list['Layer'], Any]] = None,
            strider_saddle: Optional[Union[list['Layer'], Any]] = None,
            camel_husk_saddle: Optional[Union[list['Layer'], Any]] = None,
            camel_saddle: Optional[Union[list['Layer'], Any]] = None,
            horse_saddle: Optional[Union[list['Layer'], Any]] = None,
            donkey_saddle: Optional[Union[list['Layer'], Any]] = None,
            mule_saddle: Optional[Union[list['Layer'], Any]] = None,
            zombie_horse_saddle: Optional[Union[list['Layer'], Any]] = None,
            skeleton_horse_saddle: Optional[Union[list['Layer'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if humanoid is not None:
            self.components["humanoid"] = humanoid
        if humanoid_leggings is not None:
            self.components["humanoid_leggings"] = humanoid_leggings
        if humanoid_baby is not None:
            self.components["humanoid_baby"] = humanoid_baby
        if wings is not None:
            self.components["wings"] = wings
        if wolf_body is not None:
            self.components["wolf_body"] = wolf_body
        if horse_body is not None:
            self.components["horse_body"] = horse_body
        if llama_body is not None:
            self.components["llama_body"] = llama_body
        if happy_ghast_body is not None:
            self.components["happy_ghast_body"] = happy_ghast_body
        if nautilus_saddle is not None:
            self.components["nautilus_saddle"] = nautilus_saddle
        if nautilus_body is not None:
            self.components["nautilus_body"] = nautilus_body
        if pig_saddle is not None:
            self.components["pig_saddle"] = pig_saddle
        if strider_saddle is not None:
            self.components["strider_saddle"] = strider_saddle
        if camel_husk_saddle is not None:
            self.components["camel_husk_saddle"] = camel_husk_saddle
        if camel_saddle is not None:
            self.components["camel_saddle"] = camel_saddle
        if horse_saddle is not None:
            self.components["horse_saddle"] = horse_saddle
        if donkey_saddle is not None:
            self.components["donkey_saddle"] = donkey_saddle
        if mule_saddle is not None:
            self.components["mule_saddle"] = mule_saddle
        if zombie_horse_saddle is not None:
            self.components["zombie_horse_saddle"] = zombie_horse_saddle
        if skeleton_horse_saddle is not None:
            self.components["skeleton_horse_saddle"] = skeleton_horse_saddle

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

class Font:
    def __init__(
            self,
            providers: Optional[Union[list['GlyphProvider'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if providers is not None:
            self.components["providers"] = providers

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

class GlyphProvider:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            filter: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type
        if filter is not None:
            self.components["filter"] = filter

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

class GpuWarnlist:
    def __init__(
            self,
            renderer: Optional[Union[list[str], Any]] = None,
            version: Optional[Union[list[str], Any]] = None,
            vendor: Optional[Union[list[str], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if renderer is not None:
            self.components["renderer"] = renderer
        if version is not None:
            self.components["version"] = version
        if vendor is not None:
            self.components["vendor"] = vendor

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

class ItemDefinition:
    def __init__(
            self,
            model: Optional[Union['ItemModel', Any]] = None,
            hand_animation_on_swap: Optional[Union[bool, Any]] = None,
            oversized_in_gui: Optional[Union[bool, Any]] = None,
            swap_animation_scale: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if model is not None:
            self.components["model"] = model
        if hand_animation_on_swap is not None:
            self.components["hand_animation_on_swap"] = hand_animation_on_swap
        if oversized_in_gui is not None:
            self.components["oversized_in_gui"] = oversized_in_gui
        if swap_animation_scale is not None:
            self.components["swap_animation_scale"] = swap_animation_scale

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

class ItemModel:
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

class Lang:
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

class LangDeprecated:
    def __init__(
            self,
            removed: Optional[Union[list[str], Any]] = None,
            renamed: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if removed is not None:
            self.components["removed"] = removed
        if renamed is not None:
            self.components["renamed"] = renamed

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

class Model:
    def __init__(
            self,
            parent: Optional[Union[str, Any]] = None,
            ambientocclusion: Optional[Union[bool, Any]] = None,
            gui_light: Optional[Union[Union[Any, Any], Any]] = None,
            textures: Optional[Union[dict, Any]] = None,
            elements: Optional[Union[list['ModelElement'], Any]] = None,
            display: Optional[Union[dict, Any]] = None,
            overrides: Optional[Union[list[{'predicate': dict, 'model': 'ModelRef'}], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if parent is not None:
            self.components["parent"] = parent
        if ambientocclusion is not None:
            self.components["ambientocclusion"] = ambientocclusion
        if gui_light is not None:
            self.components["gui_light"] = gui_light
        if textures is not None:
            self.components["textures"] = textures
        if elements is not None:
            self.components["elements"] = elements
        if display is not None:
            self.components["display"] = display
        if overrides is not None:
            self.components["overrides"] = overrides

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

class ModelElement:
    def __init__(
            self,
            from_: Optional[Union[list[float], Any]] = None,
            to: Optional[Union[list[float], Any]] = None,
            faces: Optional[Union[dict, Any]] = None,
            rotation: Optional[Union['ModelElementRotation', Any]] = None,
            shade: Optional[Union[bool, Any]] = None,
            light_emission: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if from_ is not None:
            self.components["from"] = from_
        if to is not None:
            self.components["to"] = to
        if faces is not None:
            self.components["faces"] = faces
        if rotation is not None:
            self.components["rotation"] = rotation
        if shade is not None:
            self.components["shade"] = shade
        if light_emission is not None:
            self.components["light_emission"] = light_emission

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

ModelElementRotation = Union[Union[{'axis': str, 'angle': Union[Union[Any, Any, Any, Any, Any], float, float]}, dict], Any]

class ModelElementRotationBase:
    def __init__(
            self,
            origin: Optional[Union[list[float], Any]] = None,
            rescale: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if origin is not None:
            self.components["origin"] = origin
        if rescale is not None:
            self.components["rescale"] = rescale

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

class TextureMaterial:
    def __init__(
            self,
            sprite: Optional[Union[str, Any]] = None,
            force_translucent: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if sprite is not None:
            self.components["sprite"] = sprite
        if force_translucent is not None:
            self.components["force_translucent"] = force_translucent

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

class Particle:
    def __init__(
            self,
            textures: Optional[Union[list[str], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if textures is not None:
            self.components["textures"] = textures

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

class Notification:
    def __init__(
            self,
            delay: Optional[Union[long, Any]] = None,
            period: Optional[Union[long, Any]] = None,
            title: Optional[Union[str, Any]] = None,
            message: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if delay is not None:
            self.components["delay"] = delay
        if period is not None:
            self.components["period"] = period
        if title is not None:
            self.components["title"] = title
        if message is not None:
            self.components["message"] = message

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

class RegionalCompliancies:
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

class AuxTarget:
    def __init__(
            self,
            name: Optional[Union[str, Any]] = None,
            id: Optional[Union[str, Any]] = None,
            width: Optional[Union[int, Any]] = None,
            height: Optional[Union[int, Any]] = None,
            bilinear: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if name is not None:
            self.components["name"] = name
        if id is not None:
            self.components["id"] = id
        if width is not None:
            self.components["width"] = width
        if height is not None:
            self.components["height"] = height
        if bilinear is not None:
            self.components["bilinear"] = bilinear

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

class FixedSizedTarget:
    def __init__(
            self,
            width: Optional[Union[int, Any]] = None,
            height: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if width is not None:
            self.components["width"] = width
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

class FullScreenTarget:
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

class InternalTarget:
    def __init__(
            self,
            width: Optional[Union[int, Any]] = None,
            height: Optional[Union[int, Any]] = None,
            persistent: Optional[Union[bool, Any]] = None,
            clear_color: Optional[Union['RGBA', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if width is not None:
            self.components["width"] = width
        if height is not None:
            self.components["height"] = height
        if persistent is not None:
            self.components["persistent"] = persistent
        if clear_color is not None:
            self.components["clear_color"] = clear_color

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

class OldTarget:
    def __init__(
            self,
            name: Optional[Union[str, Any]] = None,
            width: Optional[Union[int, Any]] = None,
            height: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if name is not None:
            self.components["name"] = name
        if width is not None:
            self.components["width"] = width
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

Pass = Union[Union[{'name': str, 'intarget': str, 'outtarget': str, 'auxtargets': list['AuxTarget'], 'use_linear_filter': bool, 'uniforms': Union[list['UniformValue'], 'UniformBlocks']}, {'program': str, 'inputs': list[Union['TargetInput', 'TextureInput']], 'output': str, 'uniforms': Union[list['UniformValue'], 'UniformBlocks']}], Any]

class PostEffect:
    def __init__(
            self,
            targets: Optional[Union[Union[list[Union[str, 'OldTarget']], 'Targets'], Any]] = None,
            passes: Optional[Union[list['Pass'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if targets is not None:
            self.components["targets"] = targets
        if passes is not None:
            self.components["passes"] = passes

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

class TargetInput:
    def __init__(
            self,
            target: Optional[Union[str, Any]] = None,
            sampler_name: Optional[Union[str, Any]] = None,
            use_depth_buffer: Optional[Union[bool, Any]] = None,
            bilinear: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if target is not None:
            self.components["target"] = target
        if sampler_name is not None:
            self.components["sampler_name"] = sampler_name
        if use_depth_buffer is not None:
            self.components["use_depth_buffer"] = use_depth_buffer
        if bilinear is not None:
            self.components["bilinear"] = bilinear

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

class Targets:
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

class TextureInput:
    def __init__(
            self,
            location: Optional[Union[str, Any]] = None,
            sampler_name: Optional[Union[str, Any]] = None,
            width: Optional[Union[int, Any]] = None,
            height: Optional[Union[int, Any]] = None,
            bilinear: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if location is not None:
            self.components["location"] = location
        if sampler_name is not None:
            self.components["sampler_name"] = sampler_name
        if width is not None:
            self.components["width"] = width
        if height is not None:
            self.components["height"] = height
        if bilinear is not None:
            self.components["bilinear"] = bilinear

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

class UniformBlocks:
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

class UniformValue:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            values: Optional[Union[list[float], Any]] = None,
            value: Optional[Union[Any, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type
        if values is not None:
            self.components["values"] = values
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

class BlendMode:
    def __init__(
            self,
            func: Optional[Union[str, Any]] = None,
            srcrgb: Optional[Union[str, Any]] = None,
            dstrgb: Optional[Union[str, Any]] = None,
            srcalpha: Optional[Union[str, Any]] = None,
            dstalpha: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if func is not None:
            self.components["func"] = func
        if srcrgb is not None:
            self.components["srcrgb"] = srcrgb
        if dstrgb is not None:
            self.components["dstrgb"] = dstrgb
        if srcalpha is not None:
            self.components["srcalpha"] = srcalpha
        if dstalpha is not None:
            self.components["dstalpha"] = dstalpha

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

class Defines:
    def __init__(
            self,
            values: Optional[Union[dict, Any]] = None,
            flags: Optional[Union[list[str], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if values is not None:
            self.components["values"] = values
        if flags is not None:
            self.components["flags"] = flags

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

class Sampler:
    def __init__(
            self,
            name: Optional[Union[str, Any]] = None,
            file: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if name is not None:
            self.components["name"] = name
        if file is not None:
            self.components["file"] = file

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

class ShaderProgram:
    def __init__(
            self,
            vertex: Optional[Union[Union[str, str], Any]] = None,
            fragment: Optional[Union[Union[str, str], Any]] = None,
            samplers: Optional[Union[list['Sampler'], Any]] = None,
            attributes: Optional[Union[list[str], Any]] = None,
            uniforms: Optional[Union[list['Uniform'], Any]] = None,
            blend: Optional[Union['BlendMode', Any]] = None,
            cull: Optional[Union[bool, Any]] = None,
            defines: Optional[Union['Defines', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if vertex is not None:
            self.components["vertex"] = vertex
        if fragment is not None:
            self.components["fragment"] = fragment
        if samplers is not None:
            self.components["samplers"] = samplers
        if attributes is not None:
            self.components["attributes"] = attributes
        if uniforms is not None:
            self.components["uniforms"] = uniforms
        if blend is not None:
            self.components["blend"] = blend
        if cull is not None:
            self.components["cull"] = cull
        if defines is not None:
            self.components["defines"] = defines

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

class Uniform:
    def __init__(
            self,
            name: Optional[Union[str, Any]] = None,
            type: Optional[Union[str, Any]] = None,
            count: Optional[Union[int, Any]] = None,
            values: Optional[Union[list[float], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if name is not None:
            self.components["name"] = name
        if type is not None:
            self.components["type"] = type
        if count is not None:
            self.components["count"] = count
        if values is not None:
            self.components["values"] = values

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

class Sound:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            name: Optional[Union[Any, Any]] = None,
            volume: Optional[Union[float, Any]] = None,
            pitch: Optional[Union[float, Any]] = None,
            weight: Optional[Union[int, Any]] = None,
            preload: Optional[Union[bool, Any]] = None,
            stream: Optional[Union[bool, Any]] = None,
            attenuation_distance: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type
        if name is not None:
            self.components["name"] = name
        if volume is not None:
            self.components["volume"] = volume
        if pitch is not None:
            self.components["pitch"] = pitch
        if weight is not None:
            self.components["weight"] = weight
        if preload is not None:
            self.components["preload"] = preload
        if stream is not None:
            self.components["stream"] = stream
        if attenuation_distance is not None:
            self.components["attenuation_distance"] = attenuation_distance

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

class SoundEventRegistration:
    def __init__(
            self,
            sounds: Optional[Union[list[Union[str, 'Sound']], Any]] = None,
            replace: Optional[Union[bool, Any]] = None,
            subtitle: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if sounds is not None:
            self.components["sounds"] = sounds
        if replace is not None:
            self.components["replace"] = replace
        if subtitle is not None:
            self.components["subtitle"] = subtitle

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

class Sounds:
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

class GuiSpriteScaling:
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

class TextureMeta:
    def __init__(
            self,
            animation: Optional[Union[{'interpolate': bool, 'width': int, 'height': int, 'frametime': int, 'frames': list[Union[{'index': int, 'time': int}, int]]}, Any]] = None,
            gui: Optional[Union[{'scaling': 'GuiSpriteScaling'}, Any]] = None,
            villager: Optional[Union[{'hat': str}, Any]] = None,
            texture: Optional[Union[{'blur': bool, 'clamp': bool, 'mipmap_strategy': str, 'alpha_cutoff_bias': float}, Any]] = None,
            palette: Optional[Union[{'base_palette': 'PaletteRef'}, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if animation is not None:
            self.components["animation"] = animation
        if gui is not None:
            self.components["gui"] = gui
        if villager is not None:
            self.components["villager"] = villager
        if texture is not None:
            self.components["texture"] = texture
        if palette is not None:
            self.components["palette"] = palette

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

class WaypointStyle:
    def __init__(
            self,
            near_distance: Optional[Union[int, Any]] = None,
            far_distance: Optional[Union[int, Any]] = None,
            sprites: Optional[Union[list[str], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if near_distance is not None:
            self.components["near_distance"] = near_distance
        if far_distance is not None:
            self.components["far_distance"] = far_distance
        if sprites is not None:
            self.components["sprites"] = sprites

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

class Advancement:
    def __init__(
            self,
            display: Optional[Union['AdvancementDisplay', Any]] = None,
            parent: Optional[Union[str, Any]] = None,
            criteria: Optional[Union[dict, Any]] = None,
            requirements: Optional[Union[list[list[str]], Any]] = None,
            rewards: Optional[Union['AdvancementRewards', Any]] = None,
            sends_telemetry_event: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if display is not None:
            self.components["display"] = display
        if parent is not None:
            self.components["parent"] = parent
        if criteria is not None:
            self.components["criteria"] = criteria
        if requirements is not None:
            self.components["requirements"] = requirements
        if rewards is not None:
            self.components["rewards"] = rewards
        if sends_telemetry_event is not None:
            self.components["sends_telemetry_event"] = sends_telemetry_event

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

class AdvancementCriterion:
    def __init__(
            self,
            trigger: Optional[Union[Union[str, str], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if trigger is not None:
            self.components["trigger"] = trigger

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

class AdvancementDisplay:
    def __init__(
            self,
            icon: Optional[Union[Union['AdvancementIcon', 'ItemStackTemplate'], Any]] = None,
            title: Optional[Union['Text', Any]] = None,
            description: Optional[Union['Text', Any]] = None,
            background: Optional[Union[Union[str, str], Any]] = None,
            frame: Optional[Union[str, Any]] = None,
            show_toast: Optional[Union[bool, Any]] = None,
            announce_to_chat: Optional[Union[bool, Any]] = None,
            hidden: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if icon is not None:
            self.components["icon"] = icon
        if title is not None:
            self.components["title"] = title
        if description is not None:
            self.components["description"] = description
        if background is not None:
            self.components["background"] = background
        if frame is not None:
            self.components["frame"] = frame
        if show_toast is not None:
            self.components["show_toast"] = show_toast
        if announce_to_chat is not None:
            self.components["announce_to_chat"] = announce_to_chat
        if hidden is not None:
            self.components["hidden"] = hidden

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

class AdvancementIcon:
    def __init__(
            self,
            item: Optional[Union[str, Any]] = None,
            nbt: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if item is not None:
            self.components["item"] = item
        if nbt is not None:
            self.components["nbt"] = nbt

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

class AdvancementRewards:
    def __init__(
            self,
            experience: Optional[Union[int, Any]] = None,
            loot: Optional[Union[list[str], Any]] = None,
            recipes: Optional[Union[list[str], Any]] = None,
            function: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if experience is not None:
            self.components["experience"] = experience
        if loot is not None:
            self.components["loot"] = loot
        if recipes is not None:
            self.components["recipes"] = recipes
        if function is not None:
            self.components["function"] = function

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

class DamageType:
    def __init__(
            self,
            message_id: Optional[Union[str, Any]] = None,
            exhaustion: Optional[Union[float, Any]] = None,
            scaling: Optional[Union[str, Any]] = None,
            effects: Optional[Union[str, Any]] = None,
            death_message_type: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if message_id is not None:
            self.components["message_id"] = message_id
        if exhaustion is not None:
            self.components["exhaustion"] = exhaustion
        if scaling is not None:
            self.components["scaling"] = scaling
        if effects is not None:
            self.components["effects"] = effects
        if death_message_type is not None:
            self.components["death_message_type"] = death_message_type

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

class DecoratedPotPattern:
    def __init__(
            self,
            asset_id: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if asset_id is not None:
            self.components["asset_id"] = asset_id

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

class Dialog:
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

class Enchantment:
    def __init__(
            self,
            description: Optional[Union['Text', Any]] = None,
            exclusive_set: Optional[Union[Union[str, list[str]], Any]] = None,
            supported_items: Optional[Union[Union[str, list[str]], Any]] = None,
            primary_items: Optional[Union[Union[str, list[str]], Any]] = None,
            weight: Optional[Union[int, Any]] = None,
            max_level: Optional[Union[int, Any]] = None,
            min_cost: Optional[Union['EnchantmentCost', Any]] = None,
            max_cost: Optional[Union['EnchantmentCost', Any]] = None,
            anvil_cost: Optional[Union[int, Any]] = None,
            slots: Optional[Union[list[str], Any]] = None,
            effects: Optional[Union['EnchantmentEffectComponentMap', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if description is not None:
            self.components["description"] = description
        if exclusive_set is not None:
            self.components["exclusive_set"] = exclusive_set
        if supported_items is not None:
            self.components["supported_items"] = supported_items
        if primary_items is not None:
            self.components["primary_items"] = primary_items
        if weight is not None:
            self.components["weight"] = weight
        if max_level is not None:
            self.components["max_level"] = max_level
        if min_cost is not None:
            self.components["min_cost"] = min_cost
        if max_cost is not None:
            self.components["max_cost"] = max_cost
        if anvil_cost is not None:
            self.components["anvil_cost"] = anvil_cost
        if slots is not None:
            self.components["slots"] = slots
        if effects is not None:
            self.components["effects"] = effects

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

class EnchantmentCost:
    def __init__(
            self,
            base: Optional[Union[int, Any]] = None,
            per_level_above_first: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if base is not None:
            self.components["base"] = base
        if per_level_above_first is not None:
            self.components["per_level_above_first"] = per_level_above_first

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

class EnchantmentEffectComponentMap:
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

class EnchantmentProvider:
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

class TestInstance:
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

class TestEnvironment:
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

ItemModifier = Union[Union['LootFunction', list['LootFunction']], Any]

NonReferenceItemModifier = Union[Union['NonReferenceLootFunction', list['NonReferenceLootFunction']], Any]

class LootPool:
    def __init__(
            self,
            rolls: Optional[Union[Union['RandomIntGenerator', 'NumberProvider'], Any]] = None,
            bonus_rolls: Optional[Union[Union['MinMaxBounds', 'NumberProvider'], Any]] = None,
            entries: Optional[Union[list['LootPoolEntry'], Any]] = None,
            functions: Optional[Union[list['LootFunction'], Any]] = None,
            conditions: Optional[Union[list['LootCondition'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if rolls is not None:
            self.components["rolls"] = rolls
        if bonus_rolls is not None:
            self.components["bonus_rolls"] = bonus_rolls
        if entries is not None:
            self.components["entries"] = entries
        if functions is not None:
            self.components["functions"] = functions
        if conditions is not None:
            self.components["conditions"] = conditions

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

class LootPoolEntry:
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

class LootTable:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            pools: Optional[Union[list['LootPool'], Any]] = None,
            functions: Optional[Union[list['LootFunction'], Any]] = None,
            random_sequence: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type
        if pools is not None:
            self.components["pools"] = pools
        if functions is not None:
            self.components["functions"] = functions
        if random_sequence is not None:
            self.components["random_sequence"] = random_sequence

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

NonReferencePredicate = Union[Union['NonReferenceLootCondition', list['NonReferenceLootCondition']], Any]

Predicate = Union[Union['LootCondition', list['LootCondition']], Any]

class Recipe:
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

class ModernAttributeModifier:
    def __init__(
            self,
            id: Optional[Union[str, Any]] = None,
            amount: Optional[Union[double, Any]] = None,
            operation: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if id is not None:
            self.components["id"] = id
        if amount is not None:
            self.components["amount"] = amount
        if operation is not None:
            self.components["operation"] = operation

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

class AttributeEntry(ModernAttributeModifier):
    def __init__(
            self,
            attribute: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if attribute is not None:
            self.components["attribute"] = attribute

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

class ContactDamage:
    def __init__(
            self,
            damage_type: Optional[Union[str, Any]] = None,
            amount: Optional[Union['FloatProvider', Any]] = None,
            attribute_to_source: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if damage_type is not None:
            self.components["damage_type"] = damage_type
        if amount is not None:
            self.components["amount"] = amount
        if attribute_to_source is not None:
            self.components["attribute_to_source"] = attribute_to_source

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

class ExplosionData:
    def __init__(
            self,
            fuse: Optional[Union[int, Any]] = None,
            power: Optional[Union[int, Any]] = None,
            causes_fire: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if fuse is not None:
            self.components["fuse"] = fuse
        if power is not None:
            self.components["power"] = power
        if causes_fire is not None:
            self.components["causes_fire"] = causes_fire

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

class KnockbackModifiers:
    def __init__(
            self,
            horizontal_power: Optional[Union[float, Any]] = None,
            vertical_power: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if horizontal_power is not None:
            self.components["horizontal_power"] = horizontal_power
        if vertical_power is not None:
            self.components["vertical_power"] = vertical_power

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

class SoundSettings:
    def __init__(
            self,
            hit_sound: Optional[Union['SoundEventRef', Any]] = None,
            push_sound: Optional[Union['SoundEventRef', Any]] = None,
            push_sound_impulse_threshold: Optional[Union[float, Any]] = None,
            push_sound_cooldown: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if hit_sound is not None:
            self.components["hit_sound"] = hit_sound
        if push_sound is not None:
            self.components["push_sound"] = push_sound
        if push_sound_impulse_threshold is not None:
            self.components["push_sound_impulse_threshold"] = push_sound_impulse_threshold
        if push_sound_cooldown is not None:
            self.components["push_sound_cooldown"] = push_sound_cooldown

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

class SulfurCubeArchetype:
    def __init__(
            self,
            items: Optional[Union[Union[str, list[str]], Any]] = None,
            buoyant: Optional[Union[bool, Any]] = None,
            explosion: Optional[Union['ExplosionData', Any]] = None,
            contact_damage: Optional[Union['ContactDamage', Any]] = None,
            knockback_modifiers: Optional[Union['KnockbackModifiers', Any]] = None,
            attribute_modifiers: Optional[Union[list['AttributeEntry'], Any]] = None,
            sound_settings: Optional[Union['SoundSettings', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if items is not None:
            self.components["items"] = items
        if buoyant is not None:
            self.components["buoyant"] = buoyant
        if explosion is not None:
            self.components["explosion"] = explosion
        if contact_damage is not None:
            self.components["contact_damage"] = contact_damage
        if knockback_modifiers is not None:
            self.components["knockback_modifiers"] = knockback_modifiers
        if attribute_modifiers is not None:
            self.components["attribute_modifiers"] = attribute_modifiers
        if sound_settings is not None:
            self.components["sound_settings"] = sound_settings

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

class EnvironmentAttributeTrackMap:
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

class TimeMarker:
    def __init__(
            self,
            ticks: Optional[Union[int, Any]] = None,
            show_in_commands: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if ticks is not None:
            self.components["ticks"] = ticks
        if show_in_commands is not None:
            self.components["show_in_commands"] = show_in_commands

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

class TimeMarkerMap:
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

class Timeline:
    def __init__(
            self,
            period_ticks: Optional[Union[int, Any]] = None,
            clock: Optional[Union[str, Any]] = None,
            time_markers: Optional[Union['TimeMarkerMap', Any]] = None,
            tracks: Optional[Union['EnvironmentAttributeTrackMap', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if period_ticks is not None:
            self.components["period_ticks"] = period_ticks
        if clock is not None:
            self.components["clock"] = clock
        if time_markers is not None:
            self.components["time_markers"] = time_markers
        if tracks is not None:
            self.components["tracks"] = tracks

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

class TradeSet:
    def __init__(
            self,
            trades: Optional[Union[Union[str, list[str]], Any]] = None,
            amount: Optional[Union['NumberProvider', Any]] = None,
            allow_duplicates: Optional[Union[bool, Any]] = None,
            random_sequence: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if trades is not None:
            self.components["trades"] = trades
        if amount is not None:
            self.components["amount"] = amount
        if allow_duplicates is not None:
            self.components["allow_duplicates"] = allow_duplicates
        if random_sequence is not None:
            self.components["random_sequence"] = random_sequence

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

class TrialSpawnerConfig:
    def __init__(
            self,
            spawn_range: Optional[Union[int, Any]] = None,
            total_mobs: Optional[Union[float, Any]] = None,
            total_mobs_added_per_player: Optional[Union[float, Any]] = None,
            simultaneous_mobs: Optional[Union[float, Any]] = None,
            simultaneous_mobs_added_per_player: Optional[Union[float, Any]] = None,
            ticks_between_spawn: Optional[Union[int, Any]] = None,
            spawn_potentials: Optional[Union[list['SpawnPotential'], Any]] = None,
            loot_tables_to_eject: Optional[Union['WeightedList', Any]] = None,
            items_to_drop_when_ominous: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if spawn_range is not None:
            self.components["spawn_range"] = spawn_range
        if total_mobs is not None:
            self.components["total_mobs"] = total_mobs
        if total_mobs_added_per_player is not None:
            self.components["total_mobs_added_per_player"] = total_mobs_added_per_player
        if simultaneous_mobs is not None:
            self.components["simultaneous_mobs"] = simultaneous_mobs
        if simultaneous_mobs_added_per_player is not None:
            self.components["simultaneous_mobs_added_per_player"] = simultaneous_mobs_added_per_player
        if ticks_between_spawn is not None:
            self.components["ticks_between_spawn"] = ticks_between_spawn
        if spawn_potentials is not None:
            self.components["spawn_potentials"] = spawn_potentials
        if loot_tables_to_eject is not None:
            self.components["loot_tables_to_eject"] = loot_tables_to_eject
        if items_to_drop_when_ominous is not None:
            self.components["items_to_drop_when_ominous"] = items_to_drop_when_ominous

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

class TrimMaterial:
    def __init__(
            self,
            asset_name: Optional[Union[str, Any]] = None,
            palette: Optional[Union['PaletteRef', Any]] = None,
            description: Optional[Union['Text', Any]] = None,
            ingredient: Optional[Union[Union[str, str], Any]] = None,
            item_model_index: Optional[Union[float, Any]] = None,
            override_armor_materials: Optional[Union[dict, Any]] = None,
            override_armor_assets: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if asset_name is not None:
            self.components["asset_name"] = asset_name
        if palette is not None:
            self.components["palette"] = palette
        if description is not None:
            self.components["description"] = description
        if ingredient is not None:
            self.components["ingredient"] = ingredient
        if item_model_index is not None:
            self.components["item_model_index"] = item_model_index
        if override_armor_materials is not None:
            self.components["override_armor_materials"] = override_armor_materials
        if override_armor_assets is not None:
            self.components["override_armor_assets"] = override_armor_assets

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

class TrimPattern:
    def __init__(
            self,
            asset_id: Optional[Union[str, Any]] = None,
            description: Optional[Union['Text', Any]] = None,
            template_item: Optional[Union[Union[str, str], Any]] = None,
            decal: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if asset_id is not None:
            self.components["asset_id"] = asset_id
        if description is not None:
            self.components["description"] = description
        if template_item is not None:
            self.components["template_item"] = template_item
        if decal is not None:
            self.components["decal"] = decal

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

NumberProvider = Union[Union[float, {'type': str}], Any]

RandomIntGenerator = Union[Union[int, {'type': str}], Any]

SoundEventRef = Union[Union[str, str, {'sound_id': str, 'range': float}], Any]

class SpawnCondition:
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

class SpawnPrioritySelector:
    def __init__(
            self,
            condition: Optional[Union['SpawnCondition', Any]] = None,
            priority: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if condition is not None:
            self.components["condition"] = condition
        if priority is not None:
            self.components["priority"] = priority

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

class SpawnPrioritySelectors:
    def __init__(
            self,
            spawn_conditions: Optional[Union[list['SpawnPrioritySelector'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if spawn_conditions is not None:
            self.components["spawn_conditions"] = spawn_conditions

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

class BannerPattern:
    def __init__(
            self,
            asset_id: Optional[Union[str, Any]] = None,
            translation_key: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if asset_id is not None:
            self.components["asset_id"] = asset_id
        if translation_key is not None:
            self.components["translation_key"] = translation_key

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

class CatVariant(SpawnPrioritySelectors):
    def __init__(
            self,
            asset_id: Optional[Union[str, Any]] = None,
            baby_asset_id: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if asset_id is not None:
            self.components["asset_id"] = asset_id
        if baby_asset_id is not None:
            self.components["baby_asset_id"] = baby_asset_id

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

class ChickenVariant(SpawnPrioritySelectors):
    def __init__(
            self,
            model: Optional[Union[str, Any]] = None,
            asset_id: Optional[Union[str, Any]] = None,
            baby_asset_id: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if model is not None:
            self.components["model"] = model
        if asset_id is not None:
            self.components["asset_id"] = asset_id
        if baby_asset_id is not None:
            self.components["baby_asset_id"] = baby_asset_id

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

class CowSounds:
    def __init__(
            self,
            ambient_sound: Optional[Union['SoundEventRef', Any]] = None,
            hurt_sound: Optional[Union['SoundEventRef', Any]] = None,
            death_sound: Optional[Union['SoundEventRef', Any]] = None,
            step_sound: Optional[Union['SoundEventRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if ambient_sound is not None:
            self.components["ambient_sound"] = ambient_sound
        if hurt_sound is not None:
            self.components["hurt_sound"] = hurt_sound
        if death_sound is not None:
            self.components["death_sound"] = death_sound
        if step_sound is not None:
            self.components["step_sound"] = step_sound

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

class CowVariant(SpawnPrioritySelectors):
    def __init__(
            self,
            model: Optional[Union[str, Any]] = None,
            asset_id: Optional[Union[str, Any]] = None,
            baby_asset_id: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if model is not None:
            self.components["model"] = model
        if asset_id is not None:
            self.components["asset_id"] = asset_id
        if baby_asset_id is not None:
            self.components["baby_asset_id"] = baby_asset_id

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

class FrogVariant(SpawnPrioritySelectors):
    def __init__(
            self,
            asset_id: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if asset_id is not None:
            self.components["asset_id"] = asset_id

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

class Instrument:
    def __init__(
            self,
            sound_event: Optional[Union['SoundEventRef', Any]] = None,
            range: Optional[Union[float, Any]] = None,
            use_duration: Optional[Union[Union[float, float], Any]] = None,
            durability_damage: Optional[Union[int, Any]] = None,
            description: Optional[Union['Text', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if sound_event is not None:
            self.components["sound_event"] = sound_event
        if range is not None:
            self.components["range"] = range
        if use_duration is not None:
            self.components["use_duration"] = use_duration
        if durability_damage is not None:
            self.components["durability_damage"] = durability_damage
        if description is not None:
            self.components["description"] = description

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

class JukeboxSong:
    def __init__(
            self,
            description: Optional[Union['Text', Any]] = None,
            comparator_output: Optional[Union[int, Any]] = None,
            length_in_seconds: Optional[Union[float, Any]] = None,
            sound_event: Optional[Union['SoundEventRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if description is not None:
            self.components["description"] = description
        if comparator_output is not None:
            self.components["comparator_output"] = comparator_output
        if length_in_seconds is not None:
            self.components["length_in_seconds"] = length_in_seconds
        if sound_event is not None:
            self.components["sound_event"] = sound_event

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

class PaintingVariant:
    def __init__(
            self,
            asset_id: Optional[Union[str, Any]] = None,
            width: Optional[Union[int, Any]] = None,
            height: Optional[Union[int, Any]] = None,
            title: Optional[Union['Text', Any]] = None,
            author: Optional[Union['Text', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if asset_id is not None:
            self.components["asset_id"] = asset_id
        if width is not None:
            self.components["width"] = width
        if height is not None:
            self.components["height"] = height
        if title is not None:
            self.components["title"] = title
        if author is not None:
            self.components["author"] = author

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

class PigVariant(SpawnPrioritySelectors):
    def __init__(
            self,
            model: Optional[Union[str, Any]] = None,
            asset_id: Optional[Union[str, Any]] = None,
            baby_asset_id: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if model is not None:
            self.components["model"] = model
        if asset_id is not None:
            self.components["asset_id"] = asset_id
        if baby_asset_id is not None:
            self.components["baby_asset_id"] = baby_asset_id

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

class WolfVariant:
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

class WolfVariantAssetInfo:
    def __init__(
            self,
            wild: Optional[Union[str, Any]] = None,
            tame: Optional[Union[str, Any]] = None,
            angry: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if wild is not None:
            self.components["wild"] = wild
        if tame is not None:
            self.components["tame"] = tame
        if angry is not None:
            self.components["angry"] = angry

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

class ZombieNautilusVariant(SpawnPrioritySelectors):
    def __init__(
            self,
            model: Optional[Union[str, Any]] = None,
            asset_id: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if model is not None:
            self.components["model"] = model
        if asset_id is not None:
            self.components["asset_id"] = asset_id

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

class VillagerTrade:
    def __init__(
            self,
            wants: Optional[Union['TradeCost', Any]] = None,
            additional_wants: Optional[Union['TradeCost', Any]] = None,
            gives: Optional[Union['ItemStackTemplate', Any]] = None,
            given_item_modifiers: Optional[Union[list['NonReferenceItemModifier'], Any]] = None,
            max_uses: Optional[Union['NumberProvider', Any]] = None,
            reputation_discount: Optional[Union['NumberProvider', Any]] = None,
            xp: Optional[Union['NumberProvider', Any]] = None,
            merchant_predicate: Optional[Union['NonReferencePredicate', Any]] = None,
            double_trade_price_enchantments: Optional[Union[Union[str, list[str]], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if wants is not None:
            self.components["wants"] = wants
        if additional_wants is not None:
            self.components["additional_wants"] = additional_wants
        if gives is not None:
            self.components["gives"] = gives
        if given_item_modifiers is not None:
            self.components["given_item_modifiers"] = given_item_modifiers
        if max_uses is not None:
            self.components["max_uses"] = max_uses
        if reputation_discount is not None:
            self.components["reputation_discount"] = reputation_discount
        if xp is not None:
            self.components["xp"] = xp
        if merchant_predicate is not None:
            self.components["merchant_predicate"] = merchant_predicate
        if double_trade_price_enchantments is not None:
            self.components["double_trade_price_enchantments"] = double_trade_price_enchantments

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

class Biome:
    def __init__(
            self,
            attributes: Optional[Union['PositionalEnvironmentAttributeMap', Any]] = None,
            category: Optional[Union[str, Any]] = None,
            depth: Optional[Union[float, Any]] = None,
            scale: Optional[Union[float, Any]] = None,
            temperature: Optional[Union[float, Any]] = None,
            downfall: Optional[Union[float, Any]] = None,
            precipitation: Optional[Union[str, Any]] = None,
            has_precipitation: Optional[Union[bool, Any]] = None,
            temperature_modifier: Optional[Union[str, Any]] = None,
            player_spawn_friendly: Optional[Union[bool, Any]] = None,
            creature_spawn_probability: Optional[Union[float, Any]] = None,
            effects: Optional[Union['BiomeEffects', Any]] = None,
            surface_builder: Optional[Union['ConfiguredSurfaceBuilderRef', Any]] = None,
            starts: Optional[Union[list['StructureRef'], Any]] = None,
            spawners: Optional[Union[dict, Any]] = None,
            spawn_costs: Optional[Union[dict, Any]] = None,
            carvers: Optional[Union[Union[dict, Union[list['CarverRef'], str, str]], Any]] = None,
            features: Optional[Union[Union[list[list['ConfiguredFeatureRef']], list[Union[list['PlacedFeatureRef'], str]]], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if attributes is not None:
            self.components["attributes"] = attributes
        if category is not None:
            self.components["category"] = category
        if depth is not None:
            self.components["depth"] = depth
        if scale is not None:
            self.components["scale"] = scale
        if temperature is not None:
            self.components["temperature"] = temperature
        if downfall is not None:
            self.components["downfall"] = downfall
        if precipitation is not None:
            self.components["precipitation"] = precipitation
        if has_precipitation is not None:
            self.components["has_precipitation"] = has_precipitation
        if temperature_modifier is not None:
            self.components["temperature_modifier"] = temperature_modifier
        if player_spawn_friendly is not None:
            self.components["player_spawn_friendly"] = player_spawn_friendly
        if creature_spawn_probability is not None:
            self.components["creature_spawn_probability"] = creature_spawn_probability
        if effects is not None:
            self.components["effects"] = effects
        if surface_builder is not None:
            self.components["surface_builder"] = surface_builder
        if starts is not None:
            self.components["starts"] = starts
        if spawners is not None:
            self.components["spawners"] = spawners
        if spawn_costs is not None:
            self.components["spawn_costs"] = spawn_costs
        if carvers is not None:
            self.components["carvers"] = carvers
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

class BiomeEffects:
    def __init__(
            self,
            sky_color: Optional[Union[int, Any]] = None,
            fog_color: Optional[Union[int, Any]] = None,
            water_color: Optional[Union[Union[int, 'StringRGB'], Any]] = None,
            water_fog_color: Optional[Union[int, Any]] = None,
            grass_color: Optional[Union[Union[int, 'StringRGB'], Any]] = None,
            foliage_color: Optional[Union[Union[int, 'StringRGB'], Any]] = None,
            dry_foliage_color: Optional[Union[Union[int, 'StringRGB'], Any]] = None,
            grass_color_modifier: Optional[Union[str, Any]] = None,
            ambient_sound: Optional[Union['SoundEventRef', Any]] = None,
            mood_sound: Optional[Union[{'sound': 'SoundEventRef', 'tick_delay': int, 'block_search_extent': int, 'offset': float}, Any]] = None,
            additions_sound: Optional[Union[{'sound': 'SoundEventRef', 'tick_chance': float}, Any]] = None,
            music: Optional[Union[Union['BiomeMusic', 'WeightedList'], Any]] = None,
            music_volume: Optional[Union[float, Any]] = None,
            particle: Optional[Union[{'options': 'Particle', 'probability': float}, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if sky_color is not None:
            self.components["sky_color"] = sky_color
        if fog_color is not None:
            self.components["fog_color"] = fog_color
        if water_color is not None:
            self.components["water_color"] = water_color
        if water_fog_color is not None:
            self.components["water_fog_color"] = water_fog_color
        if grass_color is not None:
            self.components["grass_color"] = grass_color
        if foliage_color is not None:
            self.components["foliage_color"] = foliage_color
        if dry_foliage_color is not None:
            self.components["dry_foliage_color"] = dry_foliage_color
        if grass_color_modifier is not None:
            self.components["grass_color_modifier"] = grass_color_modifier
        if ambient_sound is not None:
            self.components["ambient_sound"] = ambient_sound
        if mood_sound is not None:
            self.components["mood_sound"] = mood_sound
        if additions_sound is not None:
            self.components["additions_sound"] = additions_sound
        if music is not None:
            self.components["music"] = music
        if music_volume is not None:
            self.components["music_volume"] = music_volume
        if particle is not None:
            self.components["particle"] = particle

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

class BiomeMusic:
    def __init__(
            self,
            sound: Optional[Union['SoundEventRef', Any]] = None,
            min_delay: Optional[Union[int, Any]] = None,
            max_delay: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if sound is not None:
            self.components["sound"] = sound
        if min_delay is not None:
            self.components["min_delay"] = min_delay
        if max_delay is not None:
            self.components["max_delay"] = max_delay

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

class MobSpawnCost:
    def __init__(
            self,
            energy_budget: Optional[Union[double, Any]] = None,
            charge: Optional[Union[double, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if energy_budget is not None:
            self.components["energy_budget"] = energy_budget
        if charge is not None:
            self.components["charge"] = charge

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

class SpawnerData:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            weight: Optional[Union[int, Any]] = None,
            minCount: Optional[Union[int, Any]] = None,
            maxCount: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type
        if weight is not None:
            self.components["weight"] = weight
        if minCount is not None:
            self.components["minCount"] = minCount
        if maxCount is not None:
            self.components["maxCount"] = maxCount

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

CarverRef = Union[Union[str, str, 'ConfiguredCarver'], Any]

class ConfiguredCarver:
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

class Dimension:
    def __init__(
            self,
            type: Optional[Union['DimensionTypeRef', Any]] = None,
            generator: Optional[Union['ChunkGenerator', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type
        if generator is not None:
            self.components["generator"] = generator

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

class DimensionType:
    def __init__(
            self,
            attributes: Optional[Union['GlobalEnvironmentAttributeMap', Any]] = None,
            default_clock: Optional[Union[str, Any]] = None,
            timelines: Optional[Union[Union[str, list[str]], Any]] = None,
            ultrawarm: Optional[Union[bool, Any]] = None,
            natural: Optional[Union[bool, Any]] = None,
            piglin_safe: Optional[Union[bool, Any]] = None,
            respawn_anchor_works: Optional[Union[bool, Any]] = None,
            bed_works: Optional[Union[bool, Any]] = None,
            has_raids: Optional[Union[bool, Any]] = None,
            has_skylight: Optional[Union[bool, Any]] = None,
            has_ceiling: Optional[Union[bool, Any]] = None,
            has_ender_dragon_fight: Optional[Union[bool, Any]] = None,
            shrunk: Optional[Union[bool, Any]] = None,
            coordinate_scale: Optional[Union[double, Any]] = None,
            ambient_light: Optional[Union[float, Any]] = None,
            fixed_time: Optional[Union[int, Any]] = None,
            has_fixed_time: Optional[Union[bool, Any]] = None,
            logical_height: Optional[Union[Union[int, int], Any]] = None,
            effects: Optional[Union[str, Any]] = None,
            skybox: Optional[Union[str, Any]] = None,
            cardinal_light: Optional[Union[str, Any]] = None,
            infiniburn: Optional[Union[Union[str, str, str, list[str]], Any]] = None,
            min_y: Optional[Union[int, Any]] = None,
            height: Optional[Union[int, Any]] = None,
            monster_spawn_light_level: Optional[Union['IntProvider', Any]] = None,
            monster_spawn_block_light_limit: Optional[Union[int, Any]] = None,
            cloud_height: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if attributes is not None:
            self.components["attributes"] = attributes
        if default_clock is not None:
            self.components["default_clock"] = default_clock
        if timelines is not None:
            self.components["timelines"] = timelines
        if ultrawarm is not None:
            self.components["ultrawarm"] = ultrawarm
        if natural is not None:
            self.components["natural"] = natural
        if piglin_safe is not None:
            self.components["piglin_safe"] = piglin_safe
        if respawn_anchor_works is not None:
            self.components["respawn_anchor_works"] = respawn_anchor_works
        if bed_works is not None:
            self.components["bed_works"] = bed_works
        if has_raids is not None:
            self.components["has_raids"] = has_raids
        if has_skylight is not None:
            self.components["has_skylight"] = has_skylight
        if has_ceiling is not None:
            self.components["has_ceiling"] = has_ceiling
        if has_ender_dragon_fight is not None:
            self.components["has_ender_dragon_fight"] = has_ender_dragon_fight
        if shrunk is not None:
            self.components["shrunk"] = shrunk
        if coordinate_scale is not None:
            self.components["coordinate_scale"] = coordinate_scale
        if ambient_light is not None:
            self.components["ambient_light"] = ambient_light
        if fixed_time is not None:
            self.components["fixed_time"] = fixed_time
        if has_fixed_time is not None:
            self.components["has_fixed_time"] = has_fixed_time
        if logical_height is not None:
            self.components["logical_height"] = logical_height
        if effects is not None:
            self.components["effects"] = effects
        if skybox is not None:
            self.components["skybox"] = skybox
        if cardinal_light is not None:
            self.components["cardinal_light"] = cardinal_light
        if infiniburn is not None:
            self.components["infiniburn"] = infiniburn
        if min_y is not None:
            self.components["min_y"] = min_y
        if height is not None:
            self.components["height"] = height
        if monster_spawn_light_level is not None:
            self.components["monster_spawn_light_level"] = monster_spawn_light_level
        if monster_spawn_block_light_limit is not None:
            self.components["monster_spawn_block_light_limit"] = monster_spawn_block_light_limit
        if cloud_height is not None:
            self.components["cloud_height"] = cloud_height

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

DimensionTypeRef = Union[Union[str, {'name': str}], Any]

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

class MultiNoiseBiomeSourceParameterList:
    def __init__(
            self,
            preset: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if preset is not None:
            self.components["preset"] = preset

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

class NoiseParameters:
    def __init__(
            self,
            firstOctave: Optional[Union[int, Any]] = None,
            amplitudes: Optional[Union[list[double], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if firstOctave is not None:
            self.components["firstOctave"] = firstOctave
        if amplitudes is not None:
            self.components["amplitudes"] = amplitudes

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

class ChunkGenerator:
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

PlacedFeatureRef = Union[Union[str, 'PlacedFeature'], Any]

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

class MaterialCondition:
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

class SpawnOverride:
    def __init__(
            self,
            bounding_box: Optional[Union[str, Any]] = None,
            spawns: Optional[Union[list['SpawnerData'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if bounding_box is not None:
            self.components["bounding_box"] = bounding_box
        if spawns is not None:
            self.components["spawns"] = spawns

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

class Structure:
    def __init__(
            self,
            type: Optional[Union[Union[str, str], Any]] = None,
            biomes: Optional[Union[Union[list[str], str], Any]] = None,
            step: Optional[Union[str, Any]] = None,
            adapt_noise: Optional[Union[bool, Any]] = None,
            terrain_adaptation: Optional[Union[str, Any]] = None,
            spawn_overrides: Optional[Union[dict, Any]] = None,
            config: Optional[Union[Any, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type
        if biomes is not None:
            self.components["biomes"] = biomes
        if step is not None:
            self.components["step"] = step
        if adapt_noise is not None:
            self.components["adapt_noise"] = adapt_noise
        if terrain_adaptation is not None:
            self.components["terrain_adaptation"] = terrain_adaptation
        if spawn_overrides is not None:
            self.components["spawn_overrides"] = spawn_overrides
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

StructureRef = Union[Union[str, str, 'Structure'], Any]

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

class ExclusionZone:
    def __init__(
            self,
            other_set: Optional[Union['StructureSetRef', Any]] = None,
            chunk_count: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if other_set is not None:
            self.components["other_set"] = other_set
        if chunk_count is not None:
            self.components["chunk_count"] = chunk_count

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

class StructurePlacement:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            salt: Optional[Union[int, Any]] = None,
            frequency_reduction_method: Optional[Union[str, Any]] = None,
            frequency: Optional[Union[float, Any]] = None,
            exclusion_zone: Optional[Union['ExclusionZone', Any]] = None,
            locate_offset: Optional[Union[list[int], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type
        if salt is not None:
            self.components["salt"] = salt
        if frequency_reduction_method is not None:
            self.components["frequency_reduction_method"] = frequency_reduction_method
        if frequency is not None:
            self.components["frequency"] = frequency
        if exclusion_zone is not None:
            self.components["exclusion_zone"] = exclusion_zone
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

class StructureSet:
    def __init__(
            self,
            structures: Optional[Union[list['StructureSetElement'], Any]] = None,
            placement: Optional[Union['StructurePlacement', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if structures is not None:
            self.components["structures"] = structures
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

class StructureSetElement:
    def __init__(
            self,
            structure: Optional[Union[Union[str, str], Any]] = None,
            weight: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if structure is not None:
            self.components["structure"] = structure
        if weight is not None:
            self.components["weight"] = weight

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

StructureSetRef = Union[Union[str, 'StructureSet'], Any]

class ConfiguredSurfaceBuilder:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            config: Optional[Union[{'top_material': 'BlockState', 'under_material': 'BlockState', 'underwater_material': 'BlockState'}, Any]] = None,
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

ConfiguredSurfaceBuilderRef = Union[Union[str, 'ConfiguredSurfaceBuilder'], Any]

class Element:
    def __init__(
            self,
            element_type: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if element_type is not None:
            self.components["element_type"] = element_type

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

class TemplatePool:
    def __init__(
            self,
            fallback: Optional[Union[str, Any]] = None,
            elements: Optional[Union[list['WeightedElement'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if fallback is not None:
            self.components["fallback"] = fallback
        if elements is not None:
            self.components["elements"] = elements

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

class WeightedElement:
    def __init__(
            self,
            weight: Optional[Union[Union[int, int], Any]] = None,
            element: Optional[Union['Element', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if weight is not None:
            self.components["weight"] = weight
        if element is not None:
            self.components["element"] = element

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

class FlatGeneratorPreset:
    def __init__(
            self,
            display: Optional[Union[Union[str, str], Any]] = None,
            settings: Optional[Union['FlatGeneratorSettings', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if display is not None:
            self.components["display"] = display
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

class WorldPreset:
    def __init__(
            self,
            dimensions: Optional[Union[dict, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if dimensions is not None:
            self.components["dimensions"] = dimensions

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

Profile = Union[Union[{'name': str, 'id': Any, 'properties': Union[list['ProfileProperty'], 'ProfilePropertyMap']}, {'name': str, 'id': Any, 'properties': Union[list['ProfileProperty'], list['ProfileProperty'], 'ProfilePropertyMap'], 'texture': str, 'cape': str, 'elytra': str, 'model': str}, str], Any]

class ProfileProperty:
    def __init__(
            self,
            name: Optional[Union[Union[str, str], Any]] = None,
            value: Optional[Union[Union[str, str], Any]] = None,
            signature: Optional[Union[Union[str, str], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if name is not None:
            self.components["name"] = name
        if value is not None:
            self.components["value"] = value
        if signature is not None:
            self.components["signature"] = signature

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

class ProfilePropertyMap:
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

RGBA = Union[Union[int, list[float]], Any]

StringRGB = Union[Union[int, list[float], str], Any]

class Particle:
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

class ClickEvent:
    def __init__(
            self,
            action: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if action is not None:
            self.components["action"] = action

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

class HoverEvent:
    def __init__(
            self,
            action: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if action is not None:
            self.components["action"] = action

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

class ObjectTextConfig:
    def __init__(
            self,
            fallback: Optional[Union['Text', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if fallback is not None:
            self.components["fallback"] = fallback

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

Text = Union[Union[str, 'TextObject', list['Text']], Any]

class TextStyle:
    def __init__(
            self,
            color: Optional[Union[Union[str, str], Any]] = None,
            shadow_color: Optional[Union['RGBA', Any]] = None,
            font: Optional[Union[str, Any]] = None,
            bold: Optional[Union[bool, Any]] = None,
            italic: Optional[Union[bool, Any]] = None,
            underlined: Optional[Union[bool, Any]] = None,
            strikethrough: Optional[Union[bool, Any]] = None,
            obfuscated: Optional[Union[bool, Any]] = None,
            insertion: Optional[Union[str, Any]] = None,
            clickEvent: Optional[Union['ClickEvent', Any]] = None,
            click_event: Optional[Union['ClickEvent', Any]] = None,
            hoverEvent: Optional[Union['HoverEvent', Any]] = None,
            hover_event: Optional[Union['HoverEvent', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if color is not None:
            self.components["color"] = color
        if shadow_color is not None:
            self.components["shadow_color"] = shadow_color
        if font is not None:
            self.components["font"] = font
        if bold is not None:
            self.components["bold"] = bold
        if italic is not None:
            self.components["italic"] = italic
        if underlined is not None:
            self.components["underlined"] = underlined
        if strikethrough is not None:
            self.components["strikethrough"] = strikethrough
        if obfuscated is not None:
            self.components["obfuscated"] = obfuscated
        if insertion is not None:
            self.components["insertion"] = insertion
        if clickEvent is not None:
            self.components["clickEvent"] = clickEvent
        if click_event is not None:
            self.components["click_event"] = click_event
        if hoverEvent is not None:
            self.components["hoverEvent"] = hoverEvent
        if hover_event is not None:
            self.components["hover_event"] = hover_event

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

class TextBase(TextStyle):
    def __init__(
            self,
            extra: Optional[Union[list['Text'], Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if extra is not None:
            self.components["extra"] = extra

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

class TextNbtBase(TextBase):
    def __init__(
            self,
            interpret: Optional[Union[bool, Any]] = None,
            plain: Optional[Union[bool, Any]] = None,
            separator: Optional[Union['Text', Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if interpret is not None:
            self.components["interpret"] = interpret
        if plain is not None:
            self.components["plain"] = plain
        if separator is not None:
            self.components["separator"] = separator

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

TextObject = Union[Union[{'text': str, 'type': Any}, {'translate': str, 'fallback': str, 'with': list['Text'], 'type': Any}, {'score': {'objective': str, 'name': str}, 'type': Any}, {'selector': str, 'separator': 'Text', 'type': Any}, {'keybind': str, 'type': Any}, {'block': str, 'nbt': str, 'source': Any, 'type': Any}, {'entity': str, 'nbt': str, 'source': Any, 'type': Any}, {'storage': str, 'nbt': str, 'source': Any, 'type': Any}, {'atlas': str, 'sprite': str, 'object': Any, 'type': Any}, {'player': 'Profile', 'hat': bool, 'object': Any, 'type': Any}], Any]

SpawnPotential = Union[Union[{'Entity': 'AnyEntity', 'Weight': Union[int, byte]}, 'WeightedEntry'], Any]

class AnyEntity:
    def __init__(
            self,
            id: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if id is not None:
            self.components["id"] = id

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

ItemStackTemplate = Union[Union['ItemStack', str], Any]

class TradeCost:
    def __init__(
            self,
            count: Optional[Union['NumberProvider', Any]] = None,
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

