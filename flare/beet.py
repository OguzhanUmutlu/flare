from __future__ import annotations

import json
from pathlib import Path
from typing import Literal, Optional

from beet import Context, configurable
from beet.core.utils import FileSystemPath
from beet.toolchain.config import load_config, locate_config
from pydantic import BaseModel

from .cli import build_datapack, EmulatorRunner


class FlareOptions(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        extra = "allow"

    path: Optional[FileSystemPath] = None
    namespace: Optional[str] = None
    pack_format: Optional[int] = None
    description: Optional[str] = None
    validation: Optional[Literal["none", "warning", "strict"]] = None
    system_command_validation: Optional[Literal["none", "warning", "strict"]] = None
    minecraft_version: Optional[str] = None
    nbt_schema_missing: Optional[Literal["error", "warning", "ignore"]] = None


def beet_default(ctx: Context) -> None:
    ctx.require(flare)


@configurable(validator=FlareOptions)
def flare(ctx: Context, opts: FlareOptions) -> None:
    if opts.path:
        entry = (ctx.directory / opts.path).resolve()
    else:
        entry = _find_entry(ctx)

    if not entry.exists():
        raise FileNotFoundError(
            f"Flare entry-point not found: {entry}\n"
            "Add a load path to data_pack.load, or set 'path' under meta.flare."
        )

    cli_overrides: dict = {}
    if ctx.project_name:
        cli_overrides["namespace"] = ctx.project_name

    root_flare_json = ctx.directory / "flare.json"
    if root_flare_json.exists() and root_flare_json != (entry.parent / "flare.json"):
        with open(root_flare_json) as fh:
            cli_overrides.update(json.load(fh))

    if opts.namespace is not None:
        cli_overrides["namespace"] = opts.namespace
    if opts.pack_format is not None:
        cli_overrides["pack_format"] = opts.pack_format
    if opts.description is not None:
        cli_overrides["description"] = opts.description
    if opts.validation is not None:
        cli_overrides["validation_level"] = opts.validation
    if opts.system_command_validation is not None:
        cli_overrides["system_command_validation"] = opts.system_command_validation
    if opts.minecraft_version is not None:
        cli_overrides["minecraft_version"] = opts.minecraft_version
    if opts.nbt_schema_missing is not None:
        cli_overrides["nbt_schema_missing"] = opts.nbt_schema_missing

    extra_opts = {}
    for key, value in opts.dict(exclude_unset=True).items():
        if key not in ("path", "namespace", "pack_format", "description", "validation", "system_command_validation",
                       "minecraft_version",
                       "nbt_schema_missing"):
            extra_opts[key] = value

    for key, value in extra_opts.items():
        if key != "run":
            cli_overrides[key] = value

    output_dir: Path = ctx.cache["flare"].directory / "dist"
    cli_overrides["out_dir"] = str(output_dir)

    success, _watch_files, build_dir = build_datapack(str(entry), cli_overrides)

    if not success or build_dir is None:
        raise RuntimeError(f"Flare compilation failed for entry-point: {entry}")

    ctx.data.load(build_dir)

    if "run" in extra_opts:
        run_val = extra_opts["run"]
        runner = EmulatorRunner(build_dir, run_val)
        if runner.start():
            runner.wait()


def _find_entry(ctx: Context) -> Path:
    candidates: list[Path] = []

    default_names = ["main.fl", "main.py"]
    flare_json_path = ctx.directory / "flare.json"
    if flare_json_path.exists():
        try:
            with open(flare_json_path) as f:
                data = json.load(f)
                if "input" in data:
                    default_names.insert(0, data["input"])
        except Exception:
            pass

    try:
        config = load_config(locate_config(ctx.directory, parents=True))
        for item in config.data_pack.load.entries():
            if isinstance(item, dict):
                continue
            item_path = str(item)
            if Path(item_path).is_absolute():
                load_dir = Path(item_path)
            else:
                load_dir = ctx.directory / item_path

            if load_dir.is_dir():
                candidates.append(load_dir)
    except Exception:
        pass

    candidates.append(ctx.directory)

    for directory in candidates:
        for name in default_names:
            candidate = directory / name
            if candidate.exists():
                return candidate

    return ctx.directory / default_names[0]
