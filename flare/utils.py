import json
import os
import sys
from pathlib import Path
from typing import List

CACHE_FILE = Path.home() / ".flare" / "world_cache.json"

def minecraft_version_to_pack_format(version: str) -> float | int | None:
    if str(version).isdigit():
        return None
        
    try:
        parts = [int(p) for p in version.split(".") if p.isdigit()]
        if not parts:
            return None

        if parts[0] == 1:
            if len(parts) < 2:
                return 15
            minor = parts[1]
            patch = parts[2] if len(parts) > 2 else 0

            if minor <= 12:
                return 3
            elif minor <= 14:
                return 4
            elif minor == 15 or (minor == 16 and patch <= 1):
                return 5
            elif minor == 16:
                return 6
            elif minor == 17:
                return 7
            elif minor == 18:
                return 8 if patch <= 1 else 9
            elif minor == 19:
                return 10 if patch <= 3 else 12
            elif minor == 20:
                if patch <= 1: return 15
                if patch == 2: return 18
                if patch <= 4: return 26
                return 41
            elif minor == 21:
                if patch <= 1: return 48
                if patch <= 3: return 57
                if patch == 4: return 61
                if patch == 5: return 71
                if patch == 6: return 80
                if patch <= 8: return 81
                if patch <= 10: return 88.0
                return 94.1
        elif parts[0] >= 26:
            if parts[0] == 26:
                if len(parts) < 2: return 101.1
                minor = parts[1]
                if minor <= 1: return 101.1
                return 107.1
    except Exception:
        pass
    
    return None

def pack_format_to_minecraft_version(pack_format: float | int) -> str:
    try:
        pf = float(pack_format)
        if pf <= 4: return "1.14.4"
        if pf == 5: return "1.16.1"
        if pf == 6: return "1.16.5"
        if pf == 7: return "1.17.1"
        if pf == 8: return "1.18.1"
        if pf == 9: return "1.18.2"
        if pf <= 12: return "1.19.4"
        if pf <= 15: return "1.20.1"
        if pf <= 18: return "1.20.2"
        if pf <= 26: return "1.20.4"
        if pf <= 41: return "1.20.6"
        if pf <= 48: return "1.21.1"
        if pf <= 57: return "1.21.3"
        if pf <= 61: return "1.21.4"
        if pf <= 71: return "1.21.5"
        if pf <= 80: return "1.21.6"
        if pf <= 81: return "1.21.8"
        if pf <= 88.0: return "1.21.10"
        if pf <= 94.1: return "1.21.11"
        if pf <= 101.1: return "26.1.2"
        return "26.2"
    except Exception:
        return "1.20.4"

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
