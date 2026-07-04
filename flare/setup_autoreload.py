import json
import shutil
import threading
import time
from pathlib import Path


def setup_autoreload(datapacks_dir: Path, pack_format: int = 15):
    pack_dir = datapacks_dir / "_flare_autoreload"
    
    mcmeta_path = pack_dir / "pack.mcmeta"
    if mcmeta_path.exists():
        try:
            with open(mcmeta_path, "r") as f:
                data = json.load(f)
                if data.get("pack", {}).get("pack_format") != pack_format:
                    shutil.rmtree(pack_dir)
        except Exception:
            pass
            
    pack_dir.mkdir(parents=True, exist_ok=True)

    if not mcmeta_path.exists():
        with open(mcmeta_path, "w") as f:
            json.dump({"pack": {"pack_format": pack_format, "description": "Flare Autoreload"}}, f)

    dir_name = "function" if pack_format >= 45 else "functions"

    tags_dir = pack_dir / "data" / "minecraft" / "tags" / dir_name
    tags_dir.mkdir(parents=True, exist_ok=True)
    with open(tags_dir / "load.json", "w") as f:
        json.dump({"values": ["_flare_autoreload:load"]}, f)

    funcs_dir = pack_dir / "data" / "_flare_autoreload" / dir_name
    funcs_dir.mkdir(parents=True, exist_ok=True)

    with open(funcs_dir / "load.mcfunction", "w") as f:
        f.write("scoreboard objectives add __flare_temp__ dummy\n")
        f.write("scoreboard players set _flare_autoreload __flare_temp__ 0\n")
        f.write("scoreboard players set _flare_autoreload1 __flare_temp__ 0\n")
        f.write("schedule function _flare_autoreload:check_loop 10t replace\n")

    with open(funcs_dir / "check_loop.mcfunction", "w") as f:
        f.write("scoreboard players operation !_flare_autoreload1 __flare_temp__ = !_flare_autoreload __flare_temp__\n")
        f.write("execute store result score !_flare_autoreload __flare_temp__ run datapack list available\n")
        f.write('execute if score !_flare_autoreload __flare_temp__ > !_flare_autoreload1 __flare_temp__ run tellraw @a {"text":"Flare autoreload triggered!", "color": "green"}\n')
        f.write("execute if score !_flare_autoreload __flare_temp__ > !_flare_autoreload1 __flare_temp__ run reload\n")
        f.write("schedule function _flare_autoreload:check_loop 10t replace\n")

    def trigger():
        trigger_dir = datapacks_dir / "_flare_trigger"
        trigger_dir.mkdir(parents=True, exist_ok=True)
        with open(trigger_dir / "pack.mcmeta", "w") as f:
            json.dump({"pack": {"pack_format": pack_format, "description": "Trigger"}}, f)
        time.sleep(1)
        shutil.rmtree(trigger_dir, ignore_errors=True)

    t = threading.Thread(target=trigger, daemon=True)
    t.start()
