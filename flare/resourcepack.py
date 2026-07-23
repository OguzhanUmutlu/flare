from __future__ import annotations

import io
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple, Union

from PIL import Image, ImageColor, ImageEnhance, ImageFilter, ImageChops, ImageOps

from . import context as ctx

ColorType = Union[str, Tuple[int, int, int], Tuple[int, int, int, int]]

_temp_counter: int = 0


def _next_temp_name() -> str:
    global _temp_counter
    _temp_counter += 1
    return f"#temp_texture_{_temp_counter}"


def parse_color(color: ColorType) -> Tuple[int, int, int, int]:
    if isinstance(color, tuple):
        if len(color) == 3:
            return color[0], color[1], color[2], 255
        return color
    elif isinstance(color, str):
        return ImageColor.getcolor(color, "RGBA")
    raise ValueError(f"Invalid color specification: {color}")


class FlareTexture:
    """Represents a Minecraft resource pack texture with rich image editing and layering capabilities."""

    def __init__(self, name: Optional[str] = None, image: Optional[Union[str, bytes, Image.Image, FlareTexture]] = None,
            *, width: int = 16, height: int = 16, color: Optional[ColorType] = None, mcmeta: Optional[dict] = None,
            temp: bool = False, ):
        self.is_temp = temp or name is None
        if name is None:
            name = _next_temp_name()
        elif ":" not in name and not self.is_temp:
            name = f"{ctx._current_namespace}:{name}"

        self.name: str = name
        self.mcmeta: Optional[dict] = deepcopy(mcmeta) if mcmeta is not None else None

        if isinstance(image, FlareTexture):
            self.image = image.image.copy()
            if self.mcmeta is None and image.mcmeta:
                self.mcmeta = deepcopy(image.mcmeta)
        elif isinstance(image, Image.Image):
            self.image = image.convert("RGBA")
        elif isinstance(image, bytes):
            self.image = Image.open(io.BytesIO(image)).convert("RGBA")
        elif isinstance(image, (str, Path)) and (
                Path(image).exists() or "/" in str(image) or "\\" in str(image) or str(image).endswith(
            (".png", ".jpg", ".jpeg", ".webp", ".tga"))):
            self.image = Image.open(image).convert("RGBA")
        elif image is not None and color is None:
            rgba = parse_color(image)  # type: ignore
            self.image = Image.new("RGBA", (width, height), rgba)
        elif color is not None:
            rgba = parse_color(color)
            self.image = Image.new("RGBA", (width, height), rgba)
        else:
            self.image = Image.new("RGBA", (width, height), (0, 0, 0, 0))

        if not self.is_temp:
            self.save()

    def save(self, name: Optional[str] = None) -> FlareTexture:
        if name is not None:
            if ":" not in name:
                name = f"{ctx._current_namespace}:{name}"
            self.name = name
        elif ":" not in self.name:
            self.name = f"{ctx._current_namespace}:{self.name}"

        self.is_temp = False
        ctx.resourcepack_textures[self.name] = self
        return self

    def copy(self) -> FlareTexture:
        return FlareTexture(name=None, image=self.image.copy(), mcmeta=self.mcmeta, temp=True)

    @property
    def size(self) -> Tuple[int, int]:
        return self.image.size

    @property
    def width(self) -> int:
        return self.image.width

    @property
    def height(self) -> int:
        return self.image.height

    def fill(self, color: ColorType) -> FlareTexture:
        rgba = parse_color(color)
        self.image = Image.new("RGBA", self.image.size, rgba)
        return self

    def set_pixel(self, x: int, y: int, color: ColorType) -> FlareTexture:
        rgba = parse_color(color)
        self.image.putpixel((x, y), rgba)
        return self

    def get_pixel(self, x: int, y: int) -> Tuple[int, int, int, int]:
        return self.image.getpixel((x, y))  # type: ignore

    def resize(self, width_or_size: Union[int, Tuple[int, int]], height: Optional[int] = None) -> FlareTexture:
        if isinstance(width_or_size, tuple):
            new_size = width_or_size
        else:
            new_size = (width_or_size, height if height is not None else width_or_size)
        self.image = self.image.resize(new_size, Image.NEAREST)
        return self

    def scale(self, factor: float) -> FlareTexture:
        w = max(1, int(round(self.image.width * factor)))
        h = max(1, int(round(self.image.height * factor)))
        self.image = self.image.resize((w, h), Image.NEAREST)
        return self

    def crop(self, box_or_left: Union[Tuple[int, int, int, int], int], top: Optional[int] = None,
            right_or_width: Optional[int] = None, bottom_or_height: Optional[int] = None, ) -> FlareTexture:
        if isinstance(box_or_left, tuple):
            box = box_or_left
        elif top is not None and right_or_width is not None and bottom_or_height is not None:
            if right_or_width <= box_or_left or bottom_or_height <= top:
                box = (box_or_left, top, box_or_left + right_or_width, top + bottom_or_height)
            else:
                box = (box_or_left, top, right_or_width, bottom_or_height)
        else:
            raise ValueError("Invalid crop parameters.")
        self.image = self.image.crop(box)
        return self

    def rotate(self, angle: int, expand: bool = False) -> FlareTexture:
        self.image = self.image.rotate(angle, expand=expand)
        return self

    def flip_horizontal(self) -> FlareTexture:
        self.image = ImageOps.mirror(self.image)
        return self

    def flip_vertical(self) -> FlareTexture:
        self.image = ImageOps.flip(self.image)
        return self

    def opacity(self, factor: float) -> FlareTexture:
        r, g, b, a = self.image.split()
        a = a.point(lambda p: max(0, min(255, int(p * factor))))
        self.image = Image.merge("RGBA", (r, g, b, a))
        return self

    def alpha(self, factor: float) -> FlareTexture:
        return self.opacity(factor)

    def brightness(self, factor: float) -> FlareTexture:
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(factor)
        return self

    def contrast(self, factor: float) -> FlareTexture:
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(factor)
        return self

    def saturation(self, factor: float) -> FlareTexture:
        enhancer = ImageEnhance.Color(self.image)
        self.image = enhancer.enhance(factor)
        return self

    def recolor(self, color_map_or_func: Union[
        Dict[ColorType, ColorType], Callable[[int, int, int, int], Tuple[int, int, int, int]]], ) -> FlareTexture:
        pixels = self.image.load()
        w, h = self.image.size
        if callable(color_map_or_func):
            for x in range(w):
                for y in range(h):
                    r, g, b, a = pixels[x, y]
                    pixels[x, y] = color_map_or_func(r, g, b, a)
        elif isinstance(color_map_or_func, dict):
            parsed_map = {parse_color(k): parse_color(v) for k, v in color_map_or_func.items()}
            for x in range(w):
                for y in range(h):
                    current = pixels[x, y]
                    if current in parsed_map:
                        pixels[x, y] = parsed_map[current]
        return self

    def tint(self, color: ColorType, factor: float = 0.5) -> FlareTexture:
        target_r, target_g, target_b, _ = parse_color(color)
        pixels = self.image.load()
        w, h = self.image.size
        for x in range(w):
            for y in range(h):
                r, g, b, a = pixels[x, y]
                if a > 0:
                    new_r = int(r * (1 - factor) + target_r * factor)
                    new_g = int(g * (1 - factor) + target_g * factor)
                    new_b = int(b * (1 - factor) + target_b * factor)
                    pixels[x, y] = (new_r, new_g, new_b, a)
        return self

    def outline(self, color: ColorType = "black", width: int = 1) -> FlareTexture:
        rgba = parse_color(color)
        alpha = self.image.split()[3]
        filter_size = max(3, width * 2 + 1)
        expanded_alpha = alpha.filter(ImageFilter.MaxFilter(filter_size))
        outline_mask = ImageChops.difference(expanded_alpha, alpha)

        outline_img = Image.new("RGBA", self.image.size, rgba)
        self.image.paste(outline_img, (0, 0), mask=outline_mask)
        return self

    def overlay(self, other: Union[FlareTexture, Image.Image, str, Path],
            position: Tuple[int, int] = (0, 0)) -> FlareTexture:
        if isinstance(other, FlareTexture):
            other_img = other.image
        elif isinstance(other, Image.Image):
            other_img = other.convert("RGBA")
        elif isinstance(other, (str, Path)):
            other_img = Image.open(other).convert("RGBA")
        else:
            raise TypeError(f"Cannot overlay unsupported type: {type(other)}")

        self.image.paste(other_img, position, mask=other_img)
        return self

    def layer(self, *layers: Any) -> FlareTexture:
        for item in layers:
            pos = (0, 0)
            target_layer = item
            if isinstance(item, tuple):
                if len(item) == 2:
                    target_layer, pos = item[0], item[1]
                elif len(item) == 3:
                    target_layer, pos = item[0], (item[1], item[2])
            self.overlay(target_layer, position=pos)
        return self

    def animate(self, frametime: int = 1, interpolate: bool = False, frames: Optional[list] = None) -> FlareTexture:
        anim_dict: dict = {"frametime": frametime, "interpolate": interpolate}
        if frames is not None:
            anim_dict["frames"] = frames
        if self.mcmeta is None:
            self.mcmeta = {}
        self.mcmeta["animation"] = anim_dict
        return self

    def to_beet(self):
        try:
            from beet import Texture

            return Texture(self.image, mcmeta=self.mcmeta)
        except ImportError:
            raise RuntimeError("Beet package is required to convert FlareTexture to beet.Texture.")


def temp_texture(image: Optional[Union[str, bytes, Image.Image, FlareTexture]] = None, *, width: int = 16,
        height: int = 16, color: Optional[ColorType] = None, mcmeta: Optional[dict] = None, ) -> FlareTexture:
    """Creates a temporary, non-sourced texture (not saved to resourcepack unless explicitly saved or layered)."""
    return FlareTexture(name=None, image=image, width=width, height=height, color=color, mcmeta=mcmeta, temp=True)


def texture(name_or_image: Optional[Union[str, bytes, Image.Image, FlareTexture, ColorType]] = None,
        image: Optional[Union[str, bytes, Image.Image, FlareTexture]] = None, *, width: int = 16, height: int = 16,
        color: Optional[ColorType] = None, mcmeta: Optional[dict] = None,
        temp: Optional[bool] = None, ) -> FlareTexture:
    """Creates or fetches a texture seamlessly.

    - If no resourcepack name is given (or an image, color, dimensions, or temp=True is specified without a texture path), returns a temporary non-sourced texture.
    - If a resourcepack texture path is provided (e.g. 'item/custom_sword'), returns a sourced texture registered in the resource pack.
    """
    if temp is True:
        if isinstance(name_or_image, str) and ("/" in name_or_image or ":" in name_or_image) and not (
                Path(name_or_image).exists() or name_or_image.endswith((".png", ".jpg", ".jpeg", ".webp", ".tga"))):
            return FlareTexture(name_or_image, image=image, width=width, height=height, color=color, mcmeta=mcmeta,
                                temp=True)
        img_val = image if image is not None else name_or_image
        return temp_texture(image=img_val, width=width, height=height, color=color, mcmeta=mcmeta)

    if temp is False:
        name_str = str(name_or_image) if name_or_image is not None else None
        return FlareTexture(name_str, image=image, width=width, height=height, color=color, mcmeta=mcmeta, temp=False)

    if name_or_image is None:
        if image is not None:
            return temp_texture(image=image, width=width, height=height, color=color, mcmeta=mcmeta)
        return temp_texture(width=width, height=height, color=color, mcmeta=mcmeta)

    if isinstance(name_or_image, (Image.Image, bytes, FlareTexture)):
        return temp_texture(image=name_or_image, width=width, height=height, color=color, mcmeta=mcmeta)

    if isinstance(name_or_image, tuple):
        return temp_texture(width=width, height=height, color=name_or_image, mcmeta=mcmeta)

    if isinstance(name_or_image, str):
        if Path(name_or_image).exists() or name_or_image.endswith((".png", ".jpg", ".jpeg", ".webp", ".tga")):
            return temp_texture(image=name_or_image, width=width, height=height, color=color, mcmeta=mcmeta)

        if color is None and image is None and "/" not in name_or_image and ":" not in name_or_image:
            try:
                ImageColor.getcolor(name_or_image, "RGBA")
                return temp_texture(width=width, height=height, color=name_or_image, mcmeta=mcmeta)
            except Exception:
                pass

        name_key = name_or_image
        if ":" not in name_key:
            name_key = f"{ctx._current_namespace}:{name_key}"

        if image is None and color is None and mcmeta is None:
            if name_key in ctx.resourcepack_textures:
                return ctx.resourcepack_textures[name_key]

        return FlareTexture(name_or_image, image=image, width=width, height=height, color=color, mcmeta=mcmeta,
                            temp=False)

    return temp_texture(image=name_or_image, width=width, height=height, color=color, mcmeta=mcmeta)


def add_texture(name: str, image: Optional[Union[str, bytes, Image.Image, FlareTexture]] = None,
        **kwargs, ) -> FlareTexture:
    return FlareTexture(name, image=image, **kwargs)


def edit_texture(name: str, func: Callable[[FlareTexture], Any]) -> FlareTexture:
    tex = texture(name)
    res = func(tex)
    if isinstance(res, FlareTexture):
        res.save()
        return res
    tex.save()
    return tex


def get_texture(name: str) -> Optional[FlareTexture]:
    if ":" not in name:
        name = f"{ctx._current_namespace}:{name}"
    return ctx.resourcepack_textures.get(name)


__all__ = ["FlareTexture", "texture", "temp_texture", "add_texture", "edit_texture", "get_texture", ]
