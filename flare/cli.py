import argparse
import ast
import json
import os
import shutil
import sys
import threading
import time
import traceback
from pathlib import Path

import mcemu
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from . import context
from .preprocessor import FlareTransformer, CallGraphAnalyzer, preprocess_minecraft_commands

build_lock = threading.RLock()


def init_project(path: str):
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    json_path = p / "flare.json"

    if json_path.exists():
        print(f"Project already initialized at {p.absolute()}")
        return

    print("Initializing Flare project...")
    try:
        namespace = input("Namespace [flare]: ").strip() or "flare"
        pack_format = input("Pack format [15]: ").strip() or "15"
        description = input("Description [A Flare datapack]: ").strip() or "A Flare datapack"
    except (KeyboardInterrupt, EOFError):
        print("\nInitialization cancelled.")
        return

    config = {"namespace": namespace, "pack_format": int(pack_format), "description": description, "build_dir": "dist"}

    with open(json_path, "w") as f:
        json.dump(config, f, indent=4)
    print(f"Created {json_path.absolute()}")


def _build_datapack_inner(file_path: str, cli_overrides: dict = None):
    p = Path(file_path).parent
    json_path = p / "flare.json"

    if json_path.exists():
        with open(json_path, "r") as f:
            config = json.load(f)
    else:
        config = {"namespace": "flare", "pack_format": 15, "description": "A Flare datapack", "build_dir": "dist",
                  "validation_level": "strict", "minecraft_version": "1.20.4"}

    if cli_overrides:
        config.update(cli_overrides)

    namespace = config.get("namespace", "flare")
    build_dir = Path(config.get("build_dir", "dist"))
    if not build_dir.is_absolute():
        build_dir = p / build_dir

    context.validation_level = config.get("validation_level", "strict")
    context.minecraft_version = config.get("minecraft_version", "1.20.4")
    context.nbt_schema_missing = config.get("nbt_schema_missing", "error")

    context.reset_context()
    context._current_namespace = namespace

    print(f"Compiling {file_path}...")

    old_modules = set(sys.modules.keys())

    try:
        abs_path = os.path.abspath(file_path)
        sys.path.insert(0, os.path.dirname(abs_path))

        with open(abs_path, "r") as f:
            source = f.read()

        source = preprocess_minecraft_commands(source)

        tree = ast.parse(source, abs_path)

        analyzer = CallGraphAnalyzer()
        analyzer.visit(tree)
        context._recursive_functions = analyzer.get_recursive_functions()

        transformer = FlareTransformer()
        tree = transformer.visit(tree)
        ast.fix_missing_locations(tree)

        global_env = {"__name__": "__main__", "__file__": abs_path}
        exec(
            "from flare import _flare_assign, _flare_aug_assign, _flare_if, _flare_while, _flare_for, _flare_with, runcommand, _flare_return, _flare_break, _flare_continue, _flare_in, _flare_notin\n"
            "from flare import context as ctx\n"
            "from flare.command_parser import interpolate_command\n"
            "from flare import _flare_print as print, selector, _as, at, positioned, aligned, facing, anchored, rotated, dimension, applyon, on, summon, store\n"
            "from flare import nbt, score, fixed, tagged, ref, getscore, storage, array, byte, boolean, short, long, double\n"
            "from flare import nbtbyte, nbtbool, nbtshort, nbtint, nbtlong, nbtfloat, nbtdouble, nbtstr, nbtlist, nbtdict, nbtbytearray, nbtintarray, nbtlongarray\n"
            "from flare import round_, floor, ceil\n"
            "from flare.math import *\n"
            "from flare import dbg, export, namespace, tick", global_env)

        exec(compile(tree, abs_path, "exec"), global_env)
        sys.path.pop(0)
    except Exception as e:
        print(f"Build failed: {e}")
        traceback.print_exc()
        return False, {os.path.abspath(file_path)}, None

    new_modules = set(sys.modules.keys()) - old_modules
    watch_files = {os.path.abspath(file_path)}
    if os.path.exists(p / "flare.json"):
        watch_files.add(os.path.abspath(p / "flare.json"))

    for mod_name in new_modules:
        mod = sys.modules.get(mod_name)
        if mod and getattr(mod, "__file__", None):
            mod_file = os.path.abspath(mod.__file__)
            if (mod_file.endswith(".fl") or mod_file.endswith(
                    ".py")) and "site-packages" not in mod_file and "lib/python" not in mod_file:
                watch_files.add(mod_file)

    if build_dir.exists():
        shutil.rmtree(build_dir)

    build_dir.mkdir(parents=True, exist_ok=True)

    with open(build_dir / "pack.mcmeta", "w") as f:
        json.dump({"pack": {"pack_format": config.get("pack_format", 15),
                            "description": config.get("description", "A Flare datapack")}}, f, indent=4)

    tags = {"tick": [], "load": []}

    load_key = f"{context._current_namespace}:load"
    if "main" in context.files:
        if load_key not in context.files:
            context.files[load_key] = []
        context.files[load_key].extend(context.files.pop("main"))

    for filename, lines in context.files.items():
        if not lines and filename != "main":
            continue

        if filename.endswith(":tick"):
            tags["tick"].append(filename)
        elif filename.endswith(":load"):
            tags["load"].append(filename)

        if ":" in filename:
            ns, name = filename.split(":", 1)
            file_p = build_dir / "data" / ns / "functions" / f"{name}.mcfunction"
            is_top_level = "generated_" not in name and "while_" not in name and name not in ("main", "load")
        else:
            file_p = build_dir / "data" / context._current_namespace / "functions" / f"{filename}.mcfunction"
            is_top_level = "generated_" not in filename and "while_" not in filename and filename not in ("main",
                                                                                                          "load")

        if is_top_level and lines and lines[-1] in ("return 1", "return 0"):
            lines.pop()

        file_p.parent.mkdir(parents=True, exist_ok=True)
        with open(file_p, "w") as f:
            for line in lines:
                f.write(f"{line}\n")

    tag_dir = build_dir / "data" / "minecraft" / "tags" / "functions"
    for tag_name, tag_funcs in tags.items():
        if tag_funcs:
            tag_dir.mkdir(parents=True, exist_ok=True)
            tag_path = tag_dir / f"{tag_name}.json"
            with open(tag_path, "w") as f:
                json.dump({"values": tag_funcs}, f, indent=4)

    print(f"Successfully built datapack to {build_dir.absolute()}")
    return True, watch_files, build_dir


def build_datapack(file_path: str, cli_overrides: dict = None):
    with build_lock:
        return _build_datapack_inner(file_path, cli_overrides)


class WatcherHandler(FileSystemEventHandler):
    def __init__(self, cli_args, watch_files):
        self.cli_args = cli_args
        self.watch_files = watch_files
        self.rebuild_pending = False

    def on_modified(self, event):
        if not event.is_directory and event.src_path in self.watch_files:
            self.rebuild_pending = True


def get_tags(build_dir: Path, tag_type: str, tag_name: str) -> list[str]:
    tag_path = build_dir / "data" / "minecraft" / "tags" / tag_type / f"{tag_name}.json"
    if tag_path.exists():
        try:
            with open(tag_path, "r") as f:
                data = json.load(f)
                return data.get("values", [])
        except Exception:
            pass
    return []


def run_emulator(build_dir: Path):
    print("\n--- Starting mcemu ---")
    emu = mcemu.Emulator()
    emu.load_datapack(str(build_dir.absolute()))

    return emu


def main():
    parser = argparse.ArgumentParser(description="Flare CLI Datapack Compiler")
    parser.add_argument("target", nargs="?", default=".",
                        help="File to build or directory to init. Use 'init' to initialize in current directory.")
    parser.add_argument("--watch", action="store_true", help="Watch for file changes and rebuild")
    parser.add_argument("--run", nargs="?", const="-1", default=None,
                        help="Run the compiled datapack in mcemu. Optionally specify a timeout in seconds.")
    parser.add_argument("--nbt-schema-missing", choices=["error", "warning", "ignore"], default="error",
                        help="Action when indexing an NBT path that does not exist in the attached schema.")

    args, unknown_args = parser.parse_known_args()

    cli_overrides = {}
    if hasattr(args, 'nbt_schema_missing'):
        cli_overrides["nbt_schema_missing"] = args.nbt_schema_missing
    i = 0
    while i < len(unknown_args):
        arg = unknown_args[i]
        if arg.startswith("--"):
            key = arg[2:].replace("-", "_")
            if i + 1 < len(unknown_args) and not unknown_args[i + 1].startswith("--"):
                cli_overrides[key] = unknown_args[i + 1]
                i += 2
            else:
                cli_overrides[key] = True
                i += 1
        else:
            i += 1

    is_init = args.target == "init"
    if is_init:
        init_project(".")
        if not args.watch and not args.run:
            return

    if os.path.isdir(args.target):
        file_path = os.path.join(args.target, "main.fl")
        if not os.path.exists(file_path) and os.path.exists(os.path.join(args.target, "main.py")):
            file_path = os.path.join(args.target, "main.py")
    else:
        if args.target.endswith(".fl") or args.target.endswith(".py"):
            file_path = args.target
        else:
            file_path = f"{args.target}.fl"
            if not os.path.exists(file_path) and os.path.exists(f"{args.target}.py"):
                file_path = f"{args.target}.py"

    if not os.path.exists(file_path) and not is_init:
        print(f"Error: Target file {file_path} not found.")
        return

    success, watch_files, build_dir = build_datapack(file_path, cli_overrides)

    emu_thread = None
    running = True

    def run_loop(emu, timeout):
        try:
            start_time = time.time()
            while running:
                if timeout is not None and timeout >= 0:
                    if time.time() - start_time >= timeout:
                        break
                if emu:
                    emu.tick()
                time.sleep(0.05)
        except KeyboardInterrupt:
            pass

    if success and args.run is not None:
        try:
            timeout = float(args.run) if args.run != "-1" else None
        except ValueError:
            timeout = None
        emu = run_emulator(build_dir)
        if emu:
            emu_thread = threading.Thread(target=run_loop, args=(emu, timeout))
            emu_thread.daemon = True
            emu_thread.start()

    if args.watch:
        print(f"Watching for changes in {len(watch_files)} files...")
        handler = WatcherHandler(args, watch_files)
        observer = Observer()

        watch_dirs = set(os.path.dirname(f) for f in watch_files)
        for d in watch_dirs:
            observer.schedule(handler, d, recursive=False)

        observer.start()

        try:
            while True:
                time.sleep(0.5)
                if handler.rebuild_pending:
                    print("\nChange detected. Rebuilding...")
                    handler.rebuild_pending = False

                    if emu_thread:
                        running = False
                        emu_thread.join()

                    success, new_watch_files, build_dir = build_datapack(file_path, cli_overrides)

                    if success and new_watch_files != watch_files:
                        observer.unschedule_all()
                        watch_files = new_watch_files
                        handler.watch_files = watch_files
                        watch_dirs = set(os.path.dirname(f) for f in watch_files)
                        for d in watch_dirs:
                            observer.schedule(handler, d, recursive=False)

                    if success and args.run is not None:
                        running = True
                        try:
                            timeout = float(args.run) if args.run != "-1" else None
                        except ValueError:
                            timeout = None
                        emu = run_emulator(build_dir)
                        if emu:
                            emu_thread = threading.Thread(target=run_loop, args=(emu, timeout))
                            emu_thread.daemon = True
                            emu_thread.start()

        except KeyboardInterrupt:
            observer.stop()
            running = False
            print("\nStopped watching.")
        observer.join()
    else:
        if emu_thread:
            try:
                while emu_thread.is_alive():
                    time.sleep(0.1)
            except KeyboardInterrupt:
                running = False
                print("\nStopped emulator.")


if __name__ == "__main__":
    main()
