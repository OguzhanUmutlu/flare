import json
import urllib.request
from pathlib import Path


_memory_cache = {}

def get_schema(minecraft_version: str) -> dict:
    if minecraft_version in _memory_cache:
        return _memory_cache[minecraft_version]

    cache_dir = Path.home() / ".flare" / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"commands_{minecraft_version}.json"

    if cache_path.exists():
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                _memory_cache[minecraft_version] = data
                return data
        except json.JSONDecodeError:
            pass

    url = f"https://raw.githubusercontent.com/misode/mcmeta/{minecraft_version}-summary/commands/data.min.json"
    print(f"Downloading command schema for Minecraft {minecraft_version}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Flare/1.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(data, f)
            _memory_cache[minecraft_version] = data
            return data
    except Exception as e:
        raise RuntimeError(
            f"Failed to fetch command schema for {minecraft_version} from {url}. Ensure the version is correct.") from e
