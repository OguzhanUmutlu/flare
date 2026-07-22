import argparse
import hashlib
import importlib.abc
import importlib.machinery
import importlib.util
import json
import marshal
import os
import shutil
import sys
import threading
import time
import traceback
from pathlib import Path

import mcemu

try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer

    HAS_WATCHDOG = True
except ImportError:
    FileSystemEventHandler = object
    Observer = None
    HAS_WATCHDOG = False

from . import context
from .preprocessor import (setup_global_env,
                           transform_source, process_and_exec)
from .utils import resolve_build_targets, resolve_uri
from .setup_autoreload import setup_autoreload

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
        description = (input("Description [A Flare datapack]: ").strip() or "A Flare datapack")
        from flare.utils import minecraft_version_to_pack_format
        pack_format_val = pack_format
        ver = minecraft_version_to_pack_format(pack_format)
        if ver is not None:
            pack_format_val = ver
        else:
            try:
                pack_format_val = float(pack_format)
                if pack_format_val.is_integer():
                    pack_format_val = int(pack_format_val)
            except ValueError:
                pack_format_val = 15

    except (KeyboardInterrupt, EOFError):
        print("\nInitialization cancelled.")
        return

    config = {"namespace": namespace, "pack_format": pack_format_val, "description": description,
              "build_dir": ["dist"], }

    with open(json_path, "w") as f:
        json.dump(config, f, indent=4)
    print(f"Created {json_path.absolute()}")


def _build_datapack_inner(file_path: str, cli_overrides: dict | None = None):
    from flare.utils import minecraft_version_to_pack_format

    p = Path(file_path).parent
    json_path = p / "flare.json"

    if json_path.exists():
        with open(json_path, "r") as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError as e:
                print(f"\033[91mError: Invalid flare.json file.\033[0m")
                print(f"\033[91m{e.msg} at line {e.lineno}, column {e.colno}\033[0m")
                sys.exit(1)
    else:
        config = {"namespace": "flare", "pack_format": 15, "description": "A Flare datapack", "build_dir": ["dist"],
                  "validation_level": "strict", "system_command_validation": "none"}

    if cli_overrides:
        config.update(cli_overrides)

    pack_format = config.get("pack_format", 15)
    if isinstance(pack_format, str):
        ver = minecraft_version_to_pack_format(pack_format)
        if ver is not None:
            pack_format = ver
        else:
            try:
                pack_format = float(pack_format)
                if pack_format.is_integer(): pack_format = int(pack_format)
            except ValueError:
                pack_format = 15
        config["pack_format"] = pack_format

    namespace = config.get("namespace", "flare")

    build_dirs_raw = config.get("build_dir", ["dist"])
    if isinstance(build_dirs_raw, str):
        build_dirs_raw = [build_dirs_raw]
    else:
        build_dirs_raw = list(build_dirs_raw)

    if "out_dir" in config:
        if isinstance(config["out_dir"], list):
            build_dirs_raw = config["out_dir"]
        else:
            build_dirs_raw = [config["out_dir"]]

    resolved_build_dirs = resolve_build_targets(build_dirs_raw, p, namespace)

    if not resolved_build_dirs:
        print("\033[91mNo valid output directories found. Defaulting to 'dist'.\033[0m")
        resolved_build_dirs = [p / "dist"]

    build_dir = None
    for d in resolved_build_dirs:
        try:
            if d.is_relative_to(p) and str(d) != str(p):
                build_dir = d
                break
        except AttributeError:
            if str(p) in str(d):
                build_dir = d
                break

    if build_dir is None:
        if resolved_build_dirs:
            build_dir = resolved_build_dirs[0]
        else:
            build_dir = p / "dist"

    from flare.utils import pack_format_to_minecraft_version
    context.validation_level = config.get("validation_level", "strict")
    context.system_command_validation = config.get("system_command_validation", "none")
    context.minecraft_version = pack_format_to_minecraft_version(pack_format)
    context.nbt_schema_missing = config.get("nbt_schema_missing", "error")
    context.config = config

    context.reset_context()
    context._current_namespace = namespace

    print(f"\033[94mCompiling {file_path}...\033[0m")

    old_modules = set(sys.modules.keys())

    try:
        abs_path = os.path.abspath(file_path)
        project_dir = os.path.dirname(abs_path)
        parent_dir = os.path.dirname(project_dir)
        sys.path.insert(0, parent_dir)
        sys.path.insert(0, project_dir)

        with open(abs_path, "r", encoding="utf-8") as f:
            source = f.read()

        pkg_name = os.path.basename(project_dir)
        global_env = {"__name__": "__main__", "__file__": abs_path, "__package__": pkg_name}

        if pkg_name in sys.modules and hasattr(sys.modules[pkg_name], "__path__"):
            if project_dir not in sys.modules[pkg_name].__path__:
                sys.modules[pkg_name].__path__.append(project_dir)

        pre_start = time.time()
        setup_global_env(global_env)
        pre_end = time.time()

        comp_start = time.time()
        code_obj, tree = transform_source(source, abs_path)

        class FlareLoader(importlib.abc.Loader):
            def __init__(self, filename):
                self.filename = filename

            def create_module(self, spec):
                return None

            def exec_module(self, module):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    mod_source = f.read()
                process_and_exec(mod_source, module.__dict__, self.filename)

        class FlareMetaFinder(importlib.abc.MetaPathFinder):
            def find_spec(self, fullname, path, target=None):
                spec = importlib.machinery.PathFinder.find_spec(fullname, path, target)
                if spec and spec.origin and spec.origin.endswith('.py'):
                    if spec.origin.startswith(project_dir) or spec.origin.startswith(parent_dir):
                        spec.loader = FlareLoader(spec.origin)

                if spec is None:
                    search_paths = path if path is not None else sys.path
                    module_name = fullname.split('.')[-1]
                    for p in search_paths:
                        if not isinstance(p, str):
                            continue
                        fl_path = os.path.join(p, module_name + '.fl')
                        if os.path.exists(fl_path):
                            loader = FlareLoader(fl_path)
                            spec = importlib.util.spec_from_file_location(fullname, fl_path, loader=loader)
                            break

                return spec

        meta_finder = FlareMetaFinder()
        sys.meta_path.insert(0, meta_finder)

        try:
            exec(code_obj, global_env)
            context.evaluate_pending_exports()
        finally:
            sys.meta_path.remove(meta_finder)

        comp_end = time.time()
        sys.path.pop(0)
        sys.path.pop(0)
    except Exception as e:
        print(f"\033[91mBuild failed: {e}\033[0m")
        tb_str = traceback.format_exc()
        print(f"\033[91m{tb_str}\033[0m")
        return False, {os.path.abspath(file_path)}, None

    new_modules = set(sys.modules.keys()) - old_modules
    watch_files = {os.path.abspath(file_path)}
    if os.path.exists(p / "flare.json"):
        watch_files.add(os.path.abspath(p / "flare.json"))

    for mod_name in new_modules:
        mod = sys.modules.get(mod_name)
        if mod and getattr(mod, "__file__", None):
            mod_file = os.path.abspath(str(mod.__file__))
            if ((mod_file.endswith(".fl") or mod_file.endswith(
                    ".py")) and "site-packages" not in mod_file and "lib/python" not in mod_file):
                watch_files.add(mod_file)

    _created_dirs = set()
    io_start = time.time()

    use_cache = not config.get("no_cache", False)
    build_dir_str = str(build_dir)

    def _ensure_parent(file_path_str):
        parent = os.path.dirname(file_path_str)
        if parent not in _created_dirs:
            os.makedirs(parent, exist_ok=True)
            _created_dirs.add(parent)

    unique_targets = []
    seen_targets = set()
    for d in [build_dir] + resolved_build_dirs:
        abs_d = str(d.absolute())
        if abs_d not in seen_targets:
            seen_targets.add(abs_d)
            unique_targets.append(abs_d)

    target_caches = {}
    for t in unique_targets:
        cache_path = os.path.join(t, ".flare_iocache.dat")
        cache = {}
        if use_cache and os.path.exists(cache_path):
            try:
                with open(cache_path, "rb") as f:
                    cache = marshal.load(f)
            except Exception:
                pass
        target_caches[t] = {"path": cache_path, "old": cache, "new": {}, "written": 0, "time": 0.0, }

    if not use_cache:
        for target_dir_str in unique_targets:
            try:
                shutil.rmtree(os.path.join(target_dir_str, "data"))
            except OSError:
                pass
            try:
                os.unlink(os.path.join(target_dir_str, "pack.mcmeta"))
            except OSError:
                pass

    def write_if_changed(file_path_str, content):
        content_hash = hashlib.md5(content.encode()).hexdigest()
        rel_path = os.path.relpath(file_path_str, build_dir_str)

        for t in unique_targets:
            t0 = time.perf_counter()
            c = target_caches[t]
            c["new"][rel_path] = content_hash
            tgt_path = os.path.abspath(os.path.join(t, rel_path))

            if c["old"].get(rel_path) == content_hash and os.path.exists(tgt_path):
                c["time"] += time.perf_counter() - t0
                continue

            _ensure_parent(tgt_path)
            try:
                with open(tgt_path, "w") as f:
                    f.write(content)
                c["written"] += 1
            except Exception:
                pass
            c["time"] += time.perf_counter() - t0

    os.makedirs(build_dir_str, exist_ok=True)

    write_if_changed(os.path.join(build_dir_str, "pack.mcmeta"), json.dumps({
        "pack": {"pack_format": config.get("pack_format", 15),
                 "description": config.get("description", "A Flare datapack"), }}, indent=4, ), )

    tags = {"tick": [], "load": []}

    load_key = f"{context._current_namespace}:__init__"

    func_dir_name = "function" if config.get("pack_format", 15) >= 45 else "functions"
    ns_str = str(context._current_namespace)

    for filename, lines in context.files.items():
        if not lines and filename != load_key:
            continue

        if filename.endswith(":tick"):
            tags["tick"].append(filename)
        elif filename.endswith(":load") or filename.endswith(":__init__") or filename.endswith(":__constants__"):
            tags["load"].append(filename)

        if ":" in filename:
            ns, name = filename.split(":", 1)
            file_p = os.path.join(build_dir_str, "data", ns, func_dir_name, f"{name}.mcfunction")
            is_top_level = (
                    "generated_" not in name and "while_" not in name and "with_" not in name and name not in ("load",
                                                                                                               "__init__",
                                                                                                               "__constants__"))
        else:
            file_p = os.path.join(build_dir_str, "data", ns_str, func_dir_name, f"{filename}.mcfunction")
            is_top_level = (
                    "generated_" not in filename and "while_" not in filename and "with_" not in filename and filename not in (
                "load", "__init__", "__constants__"))

        if is_top_level and lines and lines[-1] in ("return 1", "return 0"):
            lines.pop()

        write_if_changed(file_p, "\n".join(lines) + "\n")

    for filename, json_content in context.json_files.items():
        if ":" in filename:
            ns, path = filename.split(":", 1)
        else:
            ns, path = ns_str, filename

        file_p = os.path.join(build_dir_str, "data", ns, path)
        write_if_changed(file_p, json.dumps(json_content, indent=4))

    for tick_f in context.tick_funcs:
        if tick_f not in tags["tick"]:
            tags["tick"].append(tick_f)
    for load_f in context.load_funcs:
        if load_f not in tags["load"]:
            tags["load"].append(load_f)

    tag_dir_name = "function" if config.get("pack_format", 15) >= 45 else "functions"
    tag_dir_str = os.path.join(build_dir_str, "data", "minecraft", "tags", tag_dir_name)
    for tag_name, tag_funcs in tags.items():
        if tag_funcs:
            if tag_name == "load":
                tag_funcs.sort(
                    key=lambda x: (0 if x.endswith(":__constants__") else 2 if x.endswith(":__init__") else 1, x))
            write_if_changed(os.path.join(tag_dir_str, f"{tag_name}.json"),
                             json.dumps({"values": tag_funcs}, indent=4), )

    for t in unique_targets:
        t0 = time.perf_counter()
        c = target_caches[t]
        prev_files = set(c["old"].get("__files__", []))
        current_files = set(c["new"].keys())
        stale_files = prev_files - current_files

        stale_dirs = set()
        for rel_path in stale_files:
            tgt_path = os.path.abspath(os.path.join(t, rel_path))
            try:
                os.unlink(tgt_path)
                p = os.path.dirname(tgt_path)
                while p != t and p.startswith(t):
                    stale_dirs.add(p)
                    p = os.path.dirname(p)
            except OSError:
                pass

        for d in sorted(stale_dirs, key=len, reverse=True):
            try:
                os.rmdir(d)
            except OSError:
                pass

        c["new"]["__files__"] = list(current_files)
        os.makedirs(os.path.dirname(c["path"]), exist_ok=True)
        with open(c["path"], "wb") as f:
            marshal.dump(c["new"], f)
        c["time"] += time.perf_counter() - t0

    home_dir = str(Path.home())
    simplify_path = lambda p: (("~" + p[len(home_dir):]) if p.startswith(home_dir) else p)

    io_time_sum = sum(c["time"] for c in target_caches.values())
    total_time_ms = ((pre_end - pre_start) + (comp_end - comp_start) + io_time_sum) * 1000
    print(f"\033[92mSuccessfully built datapack!\033[0m \033[90m({total_time_ms:.2f}ms)\033[0m")
    print(f"\033[90m  Preprocessed in {(pre_end - pre_start) * 1000:.2f}ms")
    print(f"  Compiled in {(comp_end - comp_start) * 1000:.2f}ms")
    for i, t in enumerate(unique_targets):
        c = target_caches[t]
        total_files = max(0, len(c["new"]) - 1)
        written = c["written"]
        cached = total_files - written
        color = "" if i == 0 else "\033[90m"
        reset = "\033[0m"
        print(
            f"{color}  Wrote {written} files in {c['time'] * 1000:.2f}ms ({cached} cached, {total_files} total) ({simplify_path(t)}){reset}")

    if config.get("autoreload"):
        try:
            autoreload_val = config["autoreload"]
            if autoreload_val is True or str(autoreload_val).lower() == "true":
                autoreload_val = "world://_last"
            elif not ("://" in autoreload_val or "/" in autoreload_val or "\\" in autoreload_val):
                autoreload_val = f"world://{autoreload_val}"
            datapacks_dir = resolve_uri(autoreload_val, p)
            pack_format = config.get("pack_format", 15)
            setup_autoreload(datapacks_dir, pack_format)
            print(f"\033[90m  Triggered autoreload in {simplify_path(str(datapacks_dir.absolute()))}\033[0m")
        except Exception as e:
            print(f"\033[93m  Failed to setup autoreload: {e}\033[0m")
    else:
        for target_dir in resolved_build_dirs:
            parent = target_dir.parent
            if parent.name == "datapacks":
                autoreload_dir = parent / "_flare_autoreload"
                if autoreload_dir.exists():
                    try:
                        shutil.rmtree(autoreload_dir)
                    except OSError:
                        pass

    return True, watch_files, build_dir


def build_datapack(file_path: str, cli_overrides: dict | None = None):
    with build_lock:
        try:
            return _build_datapack_inner(file_path, cli_overrides)
        except Exception as e:
            print(f"\033[91mBuild failed: {e}\033[0m")
            tb_str = traceback.format_exc()
            print(f"\033[91m{tb_str}\033[0m")
            return False, {os.path.abspath(file_path)}, None


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
        except:  # noqa
            pass
    return []


def run_emulator(build_dir: Path):
    print("\n--- Starting mcemu ---")
    emu = mcemu.Emulator()
    emu.load_datapack(str(build_dir.absolute()))

    return emu


class EmulatorRunner:
    def __init__(self, build_dir: Path, timeout_val: str | float | None):
        self.build_dir = build_dir
        self.running = True
        self.emu_thread = None
        try:
            self.timeout = (float(timeout_val) if timeout_val != "-1" and timeout_val is not None else None)
        except ValueError:
            self.timeout = None

    def start(self):
        emu = run_emulator(self.build_dir)
        if not emu:
            return False

        def run_loop():
            try:
                start_time = time.time()
                while self.running:
                    if self.timeout is not None and self.timeout >= 0:
                        if time.time() - start_time >= self.timeout:
                            break
                    emu.tick()
                    time.sleep(0.05)
            except KeyboardInterrupt:
                pass

        self.emu_thread = threading.Thread(target=run_loop)
        self.emu_thread.daemon = True
        self.emu_thread.start()
        return True

    def stop(self):
        self.running = False
        if self.emu_thread:
            self.emu_thread.join()

    def wait(self):
        if self.emu_thread:
            try:
                while self.emu_thread.is_alive():
                    time.sleep(0.1)
            except KeyboardInterrupt:
                self.running = False
                print("\nStopped emulator.")


def main():
    parser = argparse.ArgumentParser(description="Flare CLI Datapack Compiler")
    parser.add_argument("target", nargs="?", default=".",
                        help="File to build or directory to init. Use 'init' to initialize in current directory.", )
    parser.add_argument("--watch", action="store_true", help="Watch for file changes and rebuild")
    parser.add_argument("--run", nargs="?", const="-1", default=None,
                        help="Run the compiled datapack in mcemu. Optionally specify a timeout in seconds.", )
    parser.add_argument("--nbt-schema-missing", choices=["error", "warning", "ignore"], default="error",
                        help="Action when indexing an NBT path that does not exist in the attached schema.", )
    parser.add_argument("--namespace", type=str, default=None, help="Override the namespace for the datapack.", )
    parser.add_argument("--pack-format", type=str, default=None, help="Override the pack_format for the datapack.", )
    parser.add_argument("--description", type=str, default=None, help="Override the description for the datapack.", )
    parser.add_argument("--out-dir", type=str, default=None,
                        help="Override the output directory for the compiled datapack.", )
    parser.add_argument("--validation", type=str, help="Set the validation level of the compiled datapack.", )
    parser.add_argument("--system-command-validation", type=str,
                        help="Set the validation level for internal system commands.", )
    parser.add_argument("--no-cache", action="store_true", default=False,
                        help="Disable I/O cache, forcing all files to be rewritten.", )
    parser.add_argument("--autoreload", nargs="?", const=True, default=None,
                        help="Specify a world URI (e.g. world://my_world) to setup autoreload. Requires --watch.", )

    args, unknown_args = parser.parse_known_args()

    if args.target in ("watch", "run", "autoreload"):
        unknown_args.insert(0, args.target)
        args.target = "."

    new_unknown = []
    i = 0
    while i < len(unknown_args):
        arg = unknown_args[i]
        if arg == "watch":
            args.watch = True
        elif arg == "run":
            args.run = "-1"
            if i + 1 < len(unknown_args):
                next_arg = unknown_args[i + 1]
                if not next_arg.startswith("-") and next_arg not in ("watch", "autoreload", "run"):
                    try:
                        float(next_arg)
                        args.run = next_arg
                        i += 1
                    except ValueError:
                        if args.target == "." and (
                                next_arg.endswith(".py") or next_arg.endswith(".fl") or os.path.exists(next_arg)):
                            args.target = next_arg
                            i += 1
        elif arg == "autoreload":
            args.autoreload = True
            if i + 1 < len(unknown_args):
                next_arg = unknown_args[i + 1]
                if not next_arg.startswith("-") and next_arg not in ("watch", "autoreload", "run"):
                    if args.target == "." and (
                            next_arg.endswith(".py") or next_arg.endswith(".fl") or os.path.exists(next_arg)):
                        args.target = next_arg
                    else:
                        args.autoreload = next_arg
                    i += 1
        else:
            if args.target == "." and (arg.endswith(".py") or arg.endswith(".fl") or os.path.exists(arg)):
                args.target = arg
            else:
                new_unknown.append(arg)
        i += 1
    unknown_args = new_unknown

    cli_overrides = {}
    if hasattr(args, "nbt_schema_missing") and args.nbt_schema_missing is not None:
        cli_overrides["nbt_schema_missing"] = args.nbt_schema_missing
    if hasattr(args, "namespace") and args.namespace is not None:
        cli_overrides["namespace"] = args.namespace
    if hasattr(args, "pack_format") and args.pack_format is not None:
        cli_overrides["pack_format"] = args.pack_format
    if hasattr(args, "description") and args.description is not None:
        cli_overrides["description"] = args.description
    if hasattr(args, "out_dir") and args.out_dir is not None:
        cli_overrides["out_dir"] = args.out_dir

    if getattr(args, "no_cache", False):
        cli_overrides["no_cache"] = True
    if hasattr(args, "autoreload") and args.autoreload is not None:
        cli_overrides["autoreload"] = args.autoreload
    if hasattr(args, "validation") and args.validation is not None:
        cli_overrides["validation_level"] = args.validation
        if args.validation not in ("none", "warning", "strict"):
            print(
                f"\033[91mInvalid validation level: {args.validation}. Must be one of 'none', 'warning', or 'strict'.\033[0m")
            sys.exit(1)
    if hasattr(args, "system_command_validation") and args.system_command_validation is not None:
        cli_overrides["system_command_validation"] = args.system_command_validation
        if args.system_command_validation not in ("none", "warning", "strict"):
            print(
                f"\033[91mInvalid system command validation level: {args.system_command_validation}. Must be one of 'none', 'warning', or 'strict'.\033[0m")
            sys.exit(1)
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
        file_path = None
        json_path = os.path.join(args.target, "flare.json")
        if os.path.exists(json_path):
            try:
                with open(json_path, "r") as f:
                    config = json.load(f)
                    if "input" in config:
                        file_path = os.path.join(args.target, config["input"])
            except Exception:
                pass

        if not file_path:
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
        print(f"\033[91mError: Target file {file_path} not found.\033[0m")
        return
    if args.watch:
        os.system("cls" if os.name == "nt" else "clear")

    success, watch_files, build_dir = build_datapack(file_path, cli_overrides)

    runner = None
    if success and args.run is not None:
        runner = EmulatorRunner(build_dir, args.run)
        runner.start()

    if args.watch:
        if not HAS_WATCHDOG:
            print("\033[91mError: The 'watchdog' module is required for the --watch flag.\033[0m")
            print("\033[93mInstall it with: pip install flaremc[cli]\033[0m")
            return

        print(f"\033[93mWatching for changes in {len(watch_files)} files...\033[0m")
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
                    os.system("cls" if os.name == "nt" else "clear")

                    print("\nChange detected. Rebuilding...")
                    handler.rebuild_pending = False

                    if runner:
                        runner.stop()

                    success, new_watch_files, build_dir = build_datapack(file_path, cli_overrides)

                    if success and new_watch_files != watch_files:
                        observer.unschedule_all()
                        watch_files = new_watch_files
                        handler.watch_files = watch_files
                        watch_dirs = set(os.path.dirname(f) for f in watch_files)
                        for d in watch_dirs:
                            observer.schedule(handler, d, recursive=False)

                    if success and args.run is not None:
                        runner = EmulatorRunner(build_dir, args.run)
                        runner.start()

        except KeyboardInterrupt:
            observer.stop()
            if runner:
                runner.stop()
            print("\n\033[91mStopped watching.\033[0m")
        observer.join()
    else:
        if runner:
            runner.wait()


if __name__ == "__main__":
    main()
