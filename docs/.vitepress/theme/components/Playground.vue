<template>
    <div class="playground-wrapper">
        <!-- Status bar -->
        <div class="pg-status-bar">
            <span class="pg-logo">🔥 Flare Playground</span>
            <span class="pg-version" id="pg-version">{{ statusText }}</span>
        </div>

        <!-- Loading overlay -->
        <div v-if="loading" class="pg-loading">
            <div class="pg-spinner"></div>
            <p>{{ loadingMessage }}</p>
        </div>

        <!-- Main editor area -->
        <div class="pg-main" v-show="!loading">
            <!-- Left panel: Editor -->
            <div class="pg-panel pg-editor-panel">
                <div class="pg-panel-header">
                    <span class="pg-panel-title">📝 Flare Code</span>
                    <div class="pg-editor-controls">
                        <label>namespace: <input id="pg-namespace" v-model="namespace" class="pg-mini-input" placeholder="my_pack" /></label>
                        <button class="pg-run-btn" @click="compile" :disabled="compiling || running">
                            <span v-if="compiling">⏳ Compiling…</span>
                            <span v-else>▶ Compile</span>
                        </button>
                        <button class="pg-run-btn pg-emu-btn" @click="compileAndRun" :disabled="compiling || running">
                            <span v-if="running">⏳ Running…</span>
                            <span v-else>▶ Run</span>
                        </button>
                    </div>
                </div>
                <textarea
                    id="pg-code"
                    v-model="code"
                    class="pg-textarea"
                    spellcheck="false"
                    placeholder="# Write your Flare code here!&#10;from flare import score&#10;&#10;x = score(10)&#10;print('Hello from Flare!')"
                    @keydown.tab.prevent="insertTab"
                    @input="autoCompile"
                ></textarea>
                <div class="pg-examples">
                    <span class="pg-examples-label">Examples:</span>
                    <button v-for="ex in examples" :key="ex.label" class="pg-example-btn" @click="loadExample(ex)">{{ ex.label }}</button>
                </div>
            </div>

            <!-- Right panel: Output -->
            <div class="pg-panel pg-output-panel">
                <div class="pg-panel-header">
                    <span class="pg-panel-title">📦 Compiled Output</span>
                    <span class="pg-file-count" v-if="files.length">{{ files.length }} file{{ files.length !== 1 ? 's' : '' }}</span>
                </div>

                <div class="pg-output-area">
                    <!-- Error display -->
                    <div v-if="errorMsg" class="pg-error">
                        <div class="pg-error-header">⚠ Compile Error</div>
                        <pre class="pg-error-text">{{ errorMsg }}</pre>
                    </div>

                    <!-- No output yet -->
                    <div v-else-if="files.length === 0" class="pg-placeholder">
                        <div class="pg-placeholder-icon">🔥</div>
                        <p>Write some Flare code and hit <strong>Compile</strong> to see the generated mcfunction files here.</p>
                    </div>

                    <!-- Files output -->
                    <div v-else>
                        <div v-for="file in files" :key="file.name" class="pg-file">
                            <div class="pg-file-header">
                                <span class="pg-file-icon">📄</span>
                                <span class="pg-file-name">{{ file.name }}</span>
                                <button class="pg-copy-btn" @click="copyFile(file.name, file.content)">{{ file.copied ? '✓ Copied' : 'Copy' }}</button>
                            </div>
                            <pre class="pg-file-content">{{ file.content }}</pre>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Bottom panel: Emulator output -->
        <div class="pg-emu-panel" v-show="!loading && (runOutput || runError)">
            <div class="pg-panel-header">
                <span class="pg-panel-title">🎮 Emulator Output</span>
                <button class="pg-copy-btn" @click="clearRun">✕ Clear</button>
            </div>
            <div v-if="runError" class="pg-error" style="margin: 12px;">
                <div class="pg-error-header">⚠ Runtime Error</div>
                <pre class="pg-error-text">{{ runError }}</pre>
            </div>
            <pre v-else class="pg-emu-output">{{ runOutput }}</pre>
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
const code = ref(`from flare import namespace, score

namespace("my_pack")

# Scores compile to scoreboard operations
health = score(20)
damage = score(5)
health -= damage

if health < 10:
    print("Warning: Low Health!")`);

const files = ref([]);
const errorMsg = ref("");
const runOutput = ref("");
const runError = ref("");

let pyodideInstance = null;
let autoCompileTimer = null;

const examples = [
    {
        label: "Hello World",
        ns: "hello",
        code: `from flare import namespace
namespace("hello")

print("Hello, Minecraft World!")`
    },
    {
        label: "Scores",
        ns: "math_pack",
        code: `from flare import namespace, score
namespace("math_pack")

x = score(100)
y = score(50)
z = x + y
print("Sum:", z)`
    },
    {
        label: "NBT",
        ns: "nbt_pack",
        code: `from flare import namespace, nbtint
namespace("nbt_pack")

level = nbtint(5, addr="storage nbt_pack:data Level")
level += 1
print("Level:", level)`
    },
    {
        label: "Execute",
        ns: "exec_pack",
        code: `from flare import namespace, score
namespace("exec_pack")

hp = score(10)
with hp.store():
    say Storing HP`
    },
    {
        label: "Function",
        ns: "fn_pack",
        code: `from flare import namespace, export, score
namespace("fn_pack")

@export
def add(a: score, b: score) -> score:
    return a + b

x = score(5)
y = score(3)
result = add(x, y)
print("Result:", result)`
    }
];

function loadExample(ex) {
    namespace.value = ex.ns;
    code.value = ex.code;
    compile();
}

function insertTab(e) {
    const el = e.target;
    const start = el.selectionStart;
    const end = el.selectionEnd;
    const val = el.value;
    el.value = val.substring(0, start) + "    " + val.substring(end);
    el.selectionStart = el.selectionEnd = start + 4;
    code.value = el.value;
}

function autoCompile() {
    clearTimeout(autoCompileTimer);
    autoCompileTimer = setTimeout(() => {
        if (pyodideInstance) compile();
    }, 800);
}

async function compile() {
    if (!pyodideInstance) return;
    compiling.value = true;
    errorMsg.value = "";
    files.value = [];

    try {
        const result = await pyodideInstance.runPythonAsync(`
import json, sys
from io import StringIO

def run_flare(ns, src):
    try:
        import flare as _flare_module
        # Reset flare state
        if hasattr(_flare_module, '_reset'):
            _flare_module._reset()

        # Redirect stdout
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        import flare
        from flare.compiler import Compiler

        compiler = Compiler(namespace=ns)
        compiler.compile_string(src)
        output_files = compiler.get_files()

        sys.stdout = old_stdout
        return json.dumps({"ok": True, "files": output_files})
    except Exception as e:
        sys.stdout = old_stdout if 'old_stdout' in dir() else sys.stdout
        return json.dumps({"ok": False, "error": str(e)})

run_flare(${JSON.stringify(namespace.value)}, ${JSON.stringify(code.value)})
`);

        const data = JSON.parse(result);
        if (data.ok) {
            files.value = Object.entries(data.files || {}).map(([name, content]) => ({
                name,
                content: (content || "").trim(),
                copied: false
            }));
            if (files.value.length === 0) {
                errorMsg.value = "Compilation succeeded but produced no output files.";
            }
        } else {
            // Strip ANSI escape codes
            errorMsg.value = (data.error || "Unknown error").replace(/\x1b\[[0-9;]*m/g, "");
        }
    } catch (err) {
        errorMsg.value = err.message || String(err);
    }

    compiling.value = false;
}

async function runDatapack(compiledFiles) {
    if (!pyodideInstance || !compiledFiles || compiledFiles.length === 0) return;
    running.value = true;
    runOutput.value = "";
    runError.value = "";

    const filesJson = JSON.stringify(
        Object.fromEntries(compiledFiles.map(f => [f.name, f.content]))
    );

    try {
        const result = await pyodideInstance.runPythonAsync(`
import json, sys, os
from io import StringIO

def run_emulator(files_json):
    try:
        files = json.loads(files_json)

        base = "/tmp/flare_emu"
        import shutil
        if os.path.exists(base):
            shutil.rmtree(base)
        os.makedirs(base, exist_ok=True)

        for rel_path, content in files.items():
            full_path = os.path.join(base, rel_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w") as f:
                f.write(content)

        old_stdout = sys.stdout
        sys.stdout = buf = StringIO()

        try:
            from mcemu import Emulator
            emu = Emulator()
            pack_dirs = [d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))]
            pack_path = os.path.join(base, pack_dirs[0]) if pack_dirs else base
            emu.load_datapack(pack_path)
        finally:
            sys.stdout = old_stdout

        output = buf.getvalue()
        return json.dumps({"ok": True, "output": output})
    except Exception as e:
        import traceback
        sys.stdout = old_stdout if 'old_stdout' in dir() else sys.stdout
        return json.dumps({"ok": False, "error": traceback.format_exc()})

run_emulator(${JSON.stringify(filesJson)})
`);

        const data = JSON.parse(result);
        if (data.ok) {
            runOutput.value = (data.output || "(no output)").replace(/\x1b\[[0-9;]*m/g, "");
        } else {
            runError.value = (data.error || "Unknown error").replace(/\x1b\[[0-9;]*m/g, "");
        }
    } catch (err) {
        runError.value = err.message || String(err);
    }

    running.value = false;
}

async function compileAndRun() {
    await compile();
    if (!errorMsg.value && files.value.length > 0) {
        await runDatapack(files.value);
    }
}

function clearRun() {
    runOutput.value = "";
    runError.value = "";
}

async function copyFile(name, content) {
    await navigator.clipboard.writeText(content);
    const f = files.value.find(f => f.name === name);
    if (f) {
        f.copied = true;
        setTimeout(() => { f.copied = false; }, 2000);
    }
}

onMounted(async () => {
    if (typeof window === "undefined") return;

    try {
        loadingMessage.value = "Loading Pyodide runtime… (this may take a moment)";
        const { loadPyodide } = await import("https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.mjs");
        pyodideInstance = await loadPyodide();

        loadingMessage.value = "Installing flaremc package…";
        await pyodideInstance.loadPackage("micropip");
        const micropip = pyodideInstance.pyimport("micropip");

        // Stub out watchdog (used only for --watch CLI mode, unavailable in Pyodide)
        await pyodideInstance.runPythonAsync(`
import sys, types

def _make_stub(name):
    mod = types.ModuleType(name)
    sys.modules[name] = mod
    return mod

for _pkg in ["watchdog", "watchdog.observers", "watchdog.events"]:
    _make_stub(_pkg)
`);

        await micropip.install("flaremc", { headers: { pragma: "no-cache", "cache-control": "no-cache" } });

        // Get version
        const ver = pyodideInstance.runPython(`
try:
    from flare import __version__
    __version__
except:
    "latest"
`);
        statusText.value = `flaremc v${ver}`;
        loading.value = false;

        // Auto-compile the default example
        await compile();
    } catch (err) {
        statusText.value = "Failed to load";
        loadingMessage.value = `Error: ${err.message}. Try refreshing the page.`;
    }
});
</script>

<style scoped>
.playground-wrapper {
    position: relative;
    border: 1px solid var(--vp-c-divider);
    border-radius: 12px;
    overflow: hidden;
    background: var(--vp-c-bg-soft);
    min-height: 540px;
    margin: 24px 0;
    font-family: 'Inter', sans-serif;
}

/* Status bar */
.pg-status-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 18px;
    background: linear-gradient(90deg, #ff6b35 0%, #ff8c00 100%);
    color: white;
    font-size: 13px;
    font-weight: 600;
}

.pg-logo { font-size: 14px; letter-spacing: 0.02em; }
.pg-version { opacity: 0.9; font-size: 12px; }

/* Loading */
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
    width: 44px;
    height: 44px;
    border: 4px solid rgba(255,255,255,0.2);
    border-top-color: #ff8c00;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.pg-loading p {
    font-size: 14px;
    opacity: 0.85;
    max-width: 280px;
    text-align: center;
}

/* Main layout */
.pg-main {
    display: grid;
    grid-template-columns: 1fr 1fr;
    height: 520px;
}

@media (max-width: 768px) {
    .pg-main { grid-template-columns: 1fr; height: auto; }
}

/* Panel */
.pg-panel {
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.pg-editor-panel {
    border-right: 1px solid var(--vp-c-divider);
}

.pg-panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 14px;
    background: var(--vp-c-bg-elv);
    border-bottom: 1px solid var(--vp-c-divider);
    gap: 8px;
    flex-shrink: 0;
}

.pg-panel-title {
    font-size: 12px;
    font-weight: 600;
    color: var(--vp-c-text-2);
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.pg-file-count {
    font-size: 11px;
    color: var(--vp-c-brand);
    background: var(--vp-c-brand-soft);
    padding: 2px 8px;
    border-radius: 10px;
}

/* Editor controls */
.pg-editor-controls {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 12px;
    color: var(--vp-c-text-2);
}

.pg-mini-input {
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

.pg-mini-input:focus {
    border-color: var(--vp-c-brand);
}

.pg-run-btn {
    background: linear-gradient(135deg, #ff6b35, #ff8c00);
    color: white;
    border: none;
    border-radius: 6px;
    padding: 5px 14px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: opacity 0.2s, transform 0.1s;
}

.pg-run-btn:hover:not(:disabled) {
    opacity: 0.88;
    transform: translateY(-1px);
}

.pg-run-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Code textarea */
.pg-textarea {
    flex: 1;
    background: var(--vp-c-bg);
    color: var(--vp-c-text-1);
    border: none;
    outline: none;
    resize: none;
    padding: 14px 16px;
    font-family: 'Fira Code', 'Consolas', monospace;
    font-size: 13px;
    line-height: 1.7;
    tab-size: 4;
}

/* Examples bar */
.pg-examples {
    padding: 8px 14px;
    background: var(--vp-c-bg-elv);
    border-top: 1px solid var(--vp-c-divider);
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
    flex-shrink: 0;
}

.pg-examples-label {
    font-size: 11px;
    color: var(--vp-c-text-3);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-right: 4px;
}

.pg-example-btn {
    background: var(--vp-c-bg);
    border: 1px solid var(--vp-c-divider);
    border-radius: 5px;
    padding: 3px 10px;
    font-size: 11.5px;
    cursor: pointer;
    color: var(--vp-c-text-2);
    transition: all 0.15s;
}

.pg-example-btn:hover {
    border-color: var(--vp-c-brand);
    color: var(--vp-c-brand);
}

/* Output panel */
.pg-output-area {
    flex: 1;
    overflow-y: auto;
    padding: 0;
}

/* Error */
.pg-error {
    margin: 14px;
    border-radius: 8px;
    border: 1px solid #f87171;
    overflow: hidden;
}

.pg-error-header {
    background: #fca5a5;
    color: #7f1d1d;
    padding: 8px 14px;
    font-size: 12px;
    font-weight: 700;
}

.dark .pg-error-header {
    background: #7f1d1d;
    color: #fca5a5;
}

.pg-error-text {
    margin: 0;
    padding: 12px 14px;
    font-family: 'Fira Code', monospace;
    font-size: 12px;
    line-height: 1.6;
    color: var(--vp-c-text-1);
    white-space: pre-wrap;
    word-break: break-all;
}

/* Placeholder */
.pg-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding: 40px 24px;
    text-align: center;
    color: var(--vp-c-text-3);
}

.pg-placeholder-icon {
    font-size: 48px;
    margin-bottom: 16px;
    opacity: 0.5;
}

.pg-placeholder p {
    font-size: 13.5px;
    max-width: 260px;
    line-height: 1.65;
}

/* File output */
.pg-file {
    margin: 12px;
    border-radius: 8px;
    border: 1px solid var(--vp-c-divider);
    overflow: hidden;
}

.pg-file-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
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
}

.pg-copy-btn:hover {
    border-color: var(--vp-c-brand);
    color: var(--vp-c-brand);
}

.pg-file-content {
    margin: 0;
    padding: 12px 14px;
    font-family: 'Fira Code', monospace;
    font-size: 12px;
    line-height: 1.65;
    color: var(--vp-c-text-1);
    overflow-x: auto;
    background: var(--vp-c-bg);
    white-space: pre;
    max-height: 300px;
    overflow-y: auto;
}

/* Run button (green variant) */
.pg-emu-btn {
    background: linear-gradient(135deg, #16a34a, #15803d);
}

/* Emulator output panel */
.pg-emu-panel {
    border-top: 1px solid var(--vp-c-divider);
}

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
