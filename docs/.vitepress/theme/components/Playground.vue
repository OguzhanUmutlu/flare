<template>
    <div class="pg-wrapper">
        <div class="pg-status-bar">
            <span class="pg-logo">Flare Playground 🔥</span>
            <div class="pg-status-right">
                <span v-if="compileTime !== null" class="pg-compile-time">compiled in {{ compileTime }}ms</span>
                <span class="pg-ver">{{ statusText }}</span>
            </div>
        </div>

        <div v-if="loading" class="pg-loading">
            <div class="pg-spinner"></div>
            <p>{{ loadingMessage }}</p>
        </div>

        <div v-show="!loading" class="pg-content">
            <div class="pg-toolbar">
                <div class="pg-examples-row">
                    <span class="pg-ex-label">Examples:</span>
                    <button v-for="ex in examples" :key="ex.label" class="pg-ex-btn" @click="loadExample(ex)">{{ ex.label }}</button>
                </div>
                <div class="pg-controls">
                    <label class="pg-ns-label">namespace: <input id="pg-namespace" v-model="namespace" class="pg-ns-input" placeholder="my_pack" /></label>
                    <button class="pg-btn pg-compile-btn" @click="compile" :disabled="compiling || running">{{ compiling ? 'Compiling…' : 'Compile' }}</button>
                    <button class="pg-btn pg-run-btn-btn" @click="compileAndRun" :disabled="compiling || running">{{ running ? 'Running…' : 'Run' }}</button>
                </div>
            </div>

            <div ref="monacoEl" class="pg-monaco"></div>

            <div v-if="runOutput || runError" class="pg-emu-section">
                <div class="pg-section-hd">
                    <span>🎮 Emulator Output</span>
                    <button class="pg-copy-btn" @click="clearRun">✕ Clear</button>
                </div>
                <div v-if="runError" class="pg-error-box" style="margin:0;border-radius:0;border:none;border-bottom:1px solid #f87171;">
                    <div class="pg-error-hd">⚠ Runtime Error</div>
                    <pre class="pg-error-body">{{ runError }}</pre>
                </div>
                <pre v-else class="pg-emu-output">{{ runOutput }}</pre>
            </div>

            <div v-if="errorMsg" class="pg-error-box">
                <div class="pg-error-hd">⚠ Compile Error</div>
                <pre class="pg-error-body">{{ errorMsg }}</pre>
            </div>

            <div v-if="files.length" class="pg-files-section">
                <div class="pg-section-hd">
                    <span>📦 Compiled Output</span>
                    <span class="pg-badge">{{ files.length }} file{{ files.length !== 1 ? 's' : '' }}</span>
                </div>
                <div v-for="file in files" :key="file.name" class="pg-file">
                    <div class="pg-file-hd">
                        <span class="pg-file-icon">📄</span>
                        <span class="pg-file-name">{{ file.name }}</span>
                        <button class="pg-copy-btn" @click="copyFile(file.name, file.content)">{{ file.copied ? '✓ Copied' : 'Copy' }}</button>
                    </div>
                    <pre class="pg-file-body">{{ file.content }}</pre>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const loading = ref(true);
const compiling = ref(false);
const running = ref(false);
const loadingMessage = ref("Loading Pyodide runtime…");
const statusText = ref("Loading…");
const namespace = ref("my_pack");
const files = ref([]);
const errorMsg = ref("");
const runOutput = ref("");
const runError = ref("");
const compileTime = ref(null);
const monacoEl = ref(null);

let monacoEditor = null;
let pyodideInstance = null;
let autoCompileTimer = null;

const defaultCode = `from flare import namespace, score

namespace("my_pack")

# Scores compile to scoreboard operations
health = score(20)
damage = score(15)
health -= damage

if health < 10:
    print("Warning: Low Health!")`;

const examples = [
    { label: "Hello World", ns: "hello", code: `from flare import namespace\nnamespace("hello")\n\nprint("Hello, Minecraft World!")` },
    { label: "Scores", ns: "math_pack", code: `from flare import namespace, score\nnamespace("math_pack")\n\nx = score(100)\ny = score(50)\nz = x + y\nprint("Sum:", z)` },
    { label: "NBT", ns: "nbt_pack", code: `from flare import namespace, nbtint\nnamespace("nbt_pack")\n\nlevel = storage.nbt_pack.data.Level[int]\nlevel = 5\nlevel += 1\nprint("Level:", level)` },
    { label: "Execute", ns: "exec_pack", code: `from flare import namespace, score\nnamespace("exec_pack")\n\nhp = score(10)\nwith hp.store():\n    say Storing HP` },
    { label: "Function", ns: "fn_pack", code: `from flare import namespace, export, score\nnamespace("fn_pack")\n\n@export\ndef add(a: score, b: score) -> score:\n    return a + b\n\nx = score(5)\ny = score(3)\nresult = add(x, y)\nprint("Result:", result)` }
];

function getCode() { return monacoEditor ? monacoEditor.getValue() : defaultCode; }
function setCode(val) { if (monacoEditor) monacoEditor.setValue(val); }

function loadExample(ex) {
    namespace.value = ex.ns;
    setCode(ex.code);
    compile();
}

function autoCompile() {
    clearTimeout(autoCompileTimer);
    autoCompileTimer = setTimeout(() => { if (pyodideInstance) compile(); }, 900);
}

const COMPILE_PY = `
import json, sys, ast
from io import StringIO

def run_flare(ns, src):
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        from flare import context
        from flare.preprocessor import preprocess_minecraft_commands, CallGraphAnalyzer, FlareTransformer

        context.reset_context()
        context._current_namespace = ns

        src = preprocess_minecraft_commands(src)
        tree = ast.parse(src, "<playground>")

        analyzer = CallGraphAnalyzer()
        analyzer.visit(tree)
        context._recursive_functions = analyzer.get_recursive_functions()

        transformer = FlareTransformer()
        tree = transformer.visit(tree)
        ast.fix_missing_locations(tree)

        global_env = {"__name__": "__main__", "__file__": "<playground>"}
        exec(
            "from flare import _flare_assign, _flare_aug_assign, _flare_if, _flare_while, _flare_for, _flare_with, runcommand, _flare_return, _flare_break, _flare_continue, _flare_in, _flare_notin\\n"
            "from flare import context as ctx\\n"
            "from flare.command_parser import interpolate_command\\n"
            "from flare import _flare_print as print, selector, _as, at, positioned, aligned, facing, anchored, rotated, dimension, applyon, on, summon, store\\n"
            "from flare import nbt, score, fixed, tagged, ref, getscore, storage, array, byte, boolean, short, long, double\\n"
            "from flare import nbtbyte, nbtbool, nbtshort, nbtint, nbtlong, nbtfloat, nbtdouble, nbtstr, nbtlist, nbtcompound, nbtbytearray, nbtintarray, nbtlongarray\\n"
            "from flare import round_, floor, ceil\\n"
            "from flare.math import *\\n"
            "from flare import dbg, export, namespace, tick", global_env)

        exec(compile(tree, "<playground>", "exec"), global_env)

        load_key = f"{ns}:load"
        if "main" in context.files:
            if load_key not in context.files:
                context.files[load_key] = []
            context.files[load_key].extend(context.files.pop("main"))

        output_files = {}
        tags = {"tick": [], "load": []}
        
        # 1. Generate pack.mcmeta
        output_files["pack.mcmeta"] = json.dumps({
            "pack": {
                "pack_format": 15,
                "description": "Flare Playground Datapack"
            }
        }, indent=4)

        # 2. Process functions and strip top-level returns
        for filename, lines in context.files.items():
            if not lines and filename != "main":
                continue
                
            if filename.endswith(":tick"):
                tags["tick"].append(filename)
            elif filename.endswith(":load"):
                tags["load"].append(filename)

            if ":" in filename:
                rel_ns, name = filename.split(":", 1)
                path = f"data/{rel_ns}/functions/{name}.mcfunction"
                is_top_level = "generated_" not in name and "while_" not in name and name not in ("main", "load")
            else:
                path = f"data/{ns}/functions/{filename}.mcfunction"
                is_top_level = "generated_" not in filename and "while_" not in filename and filename not in ("main", "load")

            if is_top_level and lines and lines[-1] in ("return 1", "return 0"):
                lines.pop()

            output_files[path] = "\\n".join(lines)

        # 3. Generate Minecraft tags (load.json / tick.json)
        for tag_name, tag_funcs in tags.items():
            if tag_funcs:
                if tag_name == "load":
                    tag_funcs.sort(key=lambda x: (x == load_key, x))
                tag_path = f"data/minecraft/tags/functions/{tag_name}.json"
                output_files[tag_path] = json.dumps({"values": tag_funcs}, indent=4)

        sys.stdout = old_stdout
        return json.dumps({"ok": True, "files": output_files})
    except Exception as e:
        import traceback
        sys.stdout = old_stdout
        return json.dumps({"ok": False, "error": traceback.format_exc()})
`;

async function compile() {
    if (!pyodideInstance) return;
    compiling.value = true;
    errorMsg.value = "";
    files.value = [];
    const src = getCode();
    const t0 = performance.now();
    try {
        const result = await pyodideInstance.runPythonAsync(
            COMPILE_PY + `\nrun_flare(${JSON.stringify(namespace.value)}, ${JSON.stringify(src)})`
        );
        const data = JSON.parse(result);
        if (data.ok) {
            files.value = Object.entries(data.files || {}).map(([name, content]) => ({ name, content: (content || "").trim(), copied: false }));
            if (!files.value.length) errorMsg.value = "Compilation succeeded but produced no output files.";
        } else {
            errorMsg.value = (data.error || "Unknown error").replace(/\x1b\[[0-9;]*m/g, "");
        }
    } catch (err) { errorMsg.value = err.message || String(err); }
    compileTime.value = Math.round(performance.now() - t0);
    compiling.value = false;
}

async function runDatapack(compiledFiles) {
  if (!pyodideInstance || !compiledFiles?.length) return;
  running.value = true;
  runOutput.value = "";
  runError.value = "";
  const filesJson = JSON.stringify(Object.fromEntries(compiledFiles.map(f => [f.name, f.content])));
  try {
    const result = await pyodideInstance.runPythonAsync(`
import json, sys, os, shutil
from io import StringIO

def run_emulator(files_json):
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        files = json.loads(files_json)
        base = "/tmp/flare_emu"
        if os.path.exists(base): shutil.rmtree(base)
        os.makedirs(base, exist_ok=True)

        for rel_path, content in files.items():
            full_path = os.path.join(base, rel_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            open(full_path, "w").write(content)

        try:
            from mcemu import Emulator
            emu = Emulator()
            # LOAD DIRECTLY FROM BASE, NOT A SUBDIRECTORY
            emu.load_datapack(base)
        finally:
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout

        return json.dumps({"ok": True, "output": output})
    except Exception:
        import traceback
        sys.stdout = old_stdout
        return json.dumps({"ok": False, "error": traceback.format_exc()})

run_emulator(${JSON.stringify(filesJson)})
`);
    const data = JSON.parse(result);
    if (data.ok) runOutput.value = (data.output || "(no output)").replace(/\x1b\[[0-9;]*m/g, "");
    else runError.value = (data.error || "Unknown error").replace(/\x1b\[[0-9;]*m/g, "");
  } catch (err) { runError.value = err.message || String(err); }
  running.value = false;
}

async function compileAndRun() {
    await compile();
    if (!errorMsg.value && files.value.length > 0) await runDatapack(files.value);
}

function clearRun() { runOutput.value = ""; runError.value = ""; }

async function copyFile(name, content) {
    await navigator.clipboard.writeText(content);
    const f = files.value.find(f => f.name === name);
    if (f) { f.copied = true; setTimeout(() => { f.copied = false; }, 2000); }
}

function loadMonaco() {
    return new Promise((resolve) => {
        if (window.monaco) { resolve(); return; }
        const s = document.createElement('script');
        s.src = 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs/loader.js';
        s.onload = () => {
            window.require.config({ paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs' } });
            window.require(['vs/editor/editor.main'], () => resolve());
        };
        document.head.appendChild(s);
    });
}

function isDark() { return document.documentElement.classList.contains('dark'); }

onMounted(async () => {
    if (typeof window === "undefined") return;
    try {
        const monacoReady = loadMonaco();

        loadingMessage.value = "Loading Pyodide runtime… (this may take a moment)";
        const { loadPyodide } = await import("https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.mjs");
        pyodideInstance = await loadPyodide();

        // 1. Fetch latest versions from PyPI concurrently
        loadingMessage.value = "Fetching latest package versions…";
        let flaremcTarget = "flaremc";
        let mcemuTarget = "mcemu";
        let flaremcDisplay = "latest";
        let mcemuDisplay = "latest";

        try {
            const cacheBuster = `?t=${Date.now()}`;
            const [flareRes, mcemuRes] = await Promise.all([
                fetch(`https://pypi.org/pypi/flaremc/json${cacheBuster}`),
                fetch(`https://pypi.org/pypi/mcemu/json${cacheBuster}`)
            ]);

            if (flareRes.ok) {
                const data = await flareRes.json();
                flaremcDisplay = data.info.version;
                flaremcTarget = `flaremc==${flaremcDisplay}`;
            }
            if (mcemuRes.ok) {
                const data = await mcemuRes.json();
                mcemuDisplay = data.info.version;
                mcemuTarget = `mcemu==${mcemuDisplay}`;
            }
        } catch (e) {
            console.warn("Could not fetch latest versions from PyPI, using defaults.", e);
        }

        // 2. Install specific versions
        loadingMessage.value = `Installing packages (flaremc v${flaremcDisplay}, mcemu v${mcemuDisplay})…`;
        await pyodideInstance.loadPackage("micropip");
        const micropip = pyodideInstance.pyimport("micropip");
        await micropip.install([flaremcTarget, mcemuTarget]);

        statusText.value = `flaremc v${flaremcDisplay} | mcemu v${mcemuDisplay}`;
        loading.value = false;

        await monacoReady;
        if (monacoEl.value && window.monaco) {
            monacoEditor = window.monaco.editor.create(monacoEl.value, {
                value: defaultCode,
                language: 'python',
                theme: isDark() ? 'vs-dark' : 'vs',
                fontSize: 13,
                fontFamily: "'Fira Code', Consolas, monospace",
                minimap: { enabled: false },
                lineNumbers: 'on',
                scrollBeyondLastLine: false,
                automaticLayout: true,
                tabSize: 4,
                insertSpaces: true,
                padding: { top: 12, bottom: 12 },
            });
            monacoEditor.onDidChangeModelContent(() => autoCompile());

            new MutationObserver(() => {
                window.monaco.editor.setTheme(isDark() ? 'vs-dark' : 'vs');
            }).observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
        }

        await compile();
    } catch (err) {
        if (err.message && err.message.includes("Can't find a pure Python 3 wheel")) {
            loadingMessage.value = "Cache issue detected. Clearing cache and reloading...";
            if (window.caches) {
                caches.keys().then(keys => {
                    Promise.all(keys.map(key => caches.delete(key))).then(() => {
                        window.location.reload();
                    });
                });
                return;
            }
        }
        statusText.value = "Failed to load";
        loadingMessage.value = `Error: ${err.message}. Try refreshing the page.`;
    }
});
</script>

<style scoped>
.pg-wrapper {
    border: 1px solid var(--vp-c-divider);
    border-radius: 12px;
    overflow: hidden;
    background: var(--vp-c-bg-soft);
    margin: 24px 0;
    font-family: 'Inter', sans-serif;
    position: relative;
    min-height: 540px;
}

.pg-status-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 18px;
    background: #18181b; 
    border-bottom: 2px solid #ea580c; 
    color: #f4f4f5; 
    font-size: 13px;
    font-weight: 600;
}
.pg-logo {
    display: flex;
    align-items: center;
    gap: 6px;
    letter-spacing: 0.02em;
}
.pg-status-right {
    display: flex;
    align-items: center;
    gap: 12px;
}
.pg-ver { 
    opacity: 0.8; 
    font-size: 11.5px; 
    font-family: 'Fira Code', monospace;
}
.pg-compile-time {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(251, 146, 60, 0.35); 
    color: #fb923c; 
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 600;
    font-family: 'Fira Code', monospace;
}

.pg-loading {
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,0.65);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: white;
    z-index: 10;
    gap: 16px;
}
.pg-spinner {
    width: 44px; height: 44px;
    border: 4px solid rgba(255,255,255,0.2);
    border-top-color: #ff8c00;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.pg-loading p { font-size: 14px; opacity: 0.85; max-width: 300px; text-align: center; }

.pg-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 14px;
    background: var(--vp-c-bg-elv);
    border-bottom: 1px solid var(--vp-c-divider);
    gap: 12px;
    flex-wrap: nowrap;
}

.pg-examples-row {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
    flex: 1;
    min-width: 0;
}
.pg-ex-label {
    font-size: 11px;
    color: var(--vp-c-text-3);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    white-space: nowrap;
}
.pg-ex-btn {
    background: var(--vp-c-bg);
    border: 1px solid var(--vp-c-divider);
    border-radius: 5px;
    padding: 3px 10px;
    font-size: 11.5px;
    cursor: pointer;
    color: var(--vp-c-text-2);
    transition: all 0.15s;
    white-space: nowrap;
}
.pg-ex-btn:hover { border-color: var(--vp-c-brand); color: var(--vp-c-brand); }

.pg-controls {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
    white-space: nowrap;
}
.pg-ns-label { font-size: 12px; color: var(--vp-c-text-2); }
.pg-ns-input {
    background: var(--vp-c-bg);
    border: 1px solid var(--vp-c-divider);
    border-radius: 6px;
    padding: 3px 8px;
    color: var(--vp-c-text-1);
    font-size: 12px;
    width: 90px;
    outline: none;
    transition: border-color 0.2s;
}
.pg-ns-input:focus { border-color: var(--vp-c-brand); }

.pg-btn {
    border: none;
    border-radius: 6px;
    padding: 5px 14px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: opacity 0.2s, transform 0.1s;
    color: white;
}
.pg-btn:hover:not(:disabled) { opacity: 0.88; transform: translateY(-1px); }
.pg-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.pg-compile-btn { background: linear-gradient(135deg, #ff6b35, #ff8c00); }
.pg-run-btn-btn { background: linear-gradient(135deg, #16a34a, #15803d); }

.pg-monaco {
    height: 380px;
    border-bottom: 1px solid var(--vp-c-divider);
}

.pg-section-hd {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 14px;
    background: var(--vp-c-bg-elv);
    border-bottom: 1px solid var(--vp-c-divider);
    font-size: 12px;
    font-weight: 600;
    color: var(--vp-c-text-2);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.pg-badge {
    font-size: 11px;
    color: var(--vp-c-brand);
    background: var(--vp-c-brand-soft);
    padding: 2px 8px;
    border-radius: 10px;
    text-transform: none;
    letter-spacing: 0;
}

.pg-files-section { border-top: 1px solid var(--vp-c-divider); }

.pg-file {
    border-bottom: 1px solid var(--vp-c-divider);
}
.pg-file-hd {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 7px 14px;
    background: var(--vp-c-bg-elv);
    border-bottom: 1px solid var(--vp-c-divider);
}
.pg-file-icon { font-size: 13px; }
.pg-file-name {
    flex: 1;
    font-family: 'Fira Code', monospace;
    font-size: 12px;
    color: var(--vp-c-brand);
    font-weight: 600;
    word-break: break-all;
}
.pg-file-body {
    margin: 0;
    padding: 12px 16px;
    font-family: 'Fira Code', monospace;
    font-size: 12px;
    line-height: 1.65;
    color: var(--vp-c-text-1);
    background: var(--vp-c-bg);
    white-space: pre;
    overflow-x: auto;
    max-height: 260px;
    overflow-y: auto;
}

.pg-copy-btn {
    background: transparent;
    border: 1px solid var(--vp-c-divider);
    border-radius: 5px;
    padding: 2px 9px;
    font-size: 11px;
    cursor: pointer;
    color: var(--vp-c-text-2);
    transition: all 0.15s;
    flex-shrink: 0;
    text-transform: none;
    letter-spacing: 0;
    font-weight: normal;
}
.pg-copy-btn:hover { border-color: var(--vp-c-brand); color: var(--vp-c-brand); }

.pg-error-box {
    margin: 12px;
    border-radius: 8px;
    border: 1px solid #f87171;
    overflow: hidden;
}
.pg-error-hd {
    background: #fca5a5;
    color: #7f1d1d;
    padding: 8px 14px;
    font-size: 12px;
    font-weight: 700;
}
.dark .pg-error-hd { background: #7f1d1d; color: #fca5a5; }
.pg-error-body {
    margin: 0;
    padding: 12px 14px;
    font-family: 'Fira Code', monospace;
    font-size: 12px;
    line-height: 1.6;
    color: var(--vp-c-text-1);
    white-space: pre-wrap;
    word-break: break-all;
    background: var(--vp-c-bg);
}

.pg-emu-section { border-bottom: 1px solid var(--vp-c-divider); }
.pg-emu-output {
    margin: 0;
    padding: 14px 16px;
    font-family: 'Fira Code', monospace;
    font-size: 12.5px;
    line-height: 1.7;
    color: var(--vp-c-text-1);
    white-space: pre-wrap;
    word-break: break-word;
    background: var(--vp-c-bg);
    min-height: 60px;
    max-height: 240px;
    overflow-y: auto;
}
</style>
