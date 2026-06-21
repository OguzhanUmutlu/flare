# Playground

Try Flare right in your browser - no installation needed! The playground loads Pyodide and installs `flaremc` automatically. This may take a moment on first visit.

<Playground />

<script type="module">
// Ensure the Playground component mounts after Vue hydration
</script>

---

::: tip Note
The playground runs the **real** Flare compiler (via Pyodide / WebAssembly) in your browser. Not all features are available in the browser environment (e.g. `--run` with the emulator), but code compilation and `.mcfunction` generation work fully.
:::

## Example Snippets

Click the **Examples** buttons inside the playground above to quickly load pre-written snippets demonstrating key features.
