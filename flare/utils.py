import json
import os
import sys
from pathlib import Path
from typing import List

CACHE_FILE = Path.home() / ".flare" / "world_cache.json"


def get_minecraft_dir() -> Path:
    if sys.platform == "win32":
        return Path(os.environ.get("APPDATA", "")) / ".minecraft"
    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "minecraft"
    else:
        return Path.home() / ".minecraft"


def _get_last_edited_world(minecraft_dir: Path) -> Path | None:
    saves_dir = minecraft_dir / "saves"
    if not saves_dir.exists():
        return None

    latest_time = 0
    latest_world = None

    for world_dir in saves_dir.iterdir():
        if not world_dir.is_dir():
            continue

        level_dat = world_dir / "level.dat"
        if not level_dat.exists():
            continue

        mtime = os.path.getmtime(level_dat)
        if mtime > latest_time:
            latest_time = mtime
            latest_world = world_dir

    return latest_world


def _prompt_user_for_world(world_name: str) -> bool:
    print(f"\033[93mFound last edited world: \"{world_name}\"\033[0m")
    while True:
        response = input("Are you sure you want to add the datapack to this world? (y/n): ").strip().lower()
        if response in ("y", "yes"):
            return True
        elif response in ("n", "no"):
            return False


def resolve_uri(uri: str, project_dir: str | Path, namespace: str = None) -> Path:
    uri = str(uri)
    project_dir = str(Path(project_dir).resolve())
    minecraft_dir = get_minecraft_dir()

    if uri.startswith("minecraft://"):
        return Path(uri.replace("minecraft://", str(minecraft_dir) + os.sep))

    if uri.startswith("world://"):
        world_param = uri[len("world://"):]

        if world_param == "_last":
            last_world = _get_last_edited_world(minecraft_dir)
            if last_world is None:
                raise ValueError("Could not find any Minecraft worlds with a level.dat file.")

            world_name = last_world.name

            cache = {}
            if CACHE_FILE.exists():
                try:
                    with open(CACHE_FILE, "r") as f:
                        cache = json.load(f)
                except Exception:
                    pass

            cached_world = cache.get(project_dir)

            if cached_world != world_name:
                if not _prompt_user_for_world(world_name):
                    print("Build aborted by user.")
                    sys.exit(1)

                cache[project_dir] = world_name
                CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
                try:
                    with open(CACHE_FILE, "w") as f:
                        json.dump(cache, f, indent=4)
                except Exception as e:
                    print(f"\033[93mWarning: Failed to save world cache: {e}\033[0m")

            target_world = last_world
        else:
            target_world = minecraft_dir / "saves" / world_param

        if "datapacks" in target_world.parts:
            return target_world

        datapacks_dir = target_world / "datapacks"
        if namespace:
            return datapacks_dir / namespace
        return datapacks_dir

    p = Path(uri)
    if not p.is_absolute():
        p = Path(project_dir) / uri

    if (p / "level.dat").exists() and "datapacks" not in p.parts:
        p = p / "datapacks"
        if namespace:
            p = p / namespace

    return p


def resolve_build_targets(build_dirs: str | List[str], project_dir: str | Path, namespace: str = None) -> List[Path]:
    if isinstance(build_dirs, str):
        build_dirs = [build_dirs]

    resolved = []
    for d in build_dirs:
        try:
            p = resolve_uri(d, project_dir, namespace)
            resolved.append(p)
        except Exception as e:
            print(f"\033[91mFailed to resolve build target '{d}': {e}\033[0m")

    return resolved
