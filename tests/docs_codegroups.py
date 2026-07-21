import os
import re
import shutil
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)

DOCS_DIR = os.path.join(ROOT_DIR, "docs", "guide")
DOCS_TEST_DIR = os.path.join(SCRIPT_DIR, "docstest")
FLARE_BIN = os.path.join(ROOT_DIR, ".venv", "bin", "flare")


def process_markdown_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    def compile_and_generate_group(code, original_text):
        test_code = "from flare import *\nnamespace('pack')\n" + code

        os.makedirs(DOCS_TEST_DIR, exist_ok=True)
        main_py = os.path.join(DOCS_TEST_DIR, "main.py")
        with open(main_py, "w", encoding="utf-8") as f:
            f.write(test_code)

        dist_dir = os.path.join(DOCS_TEST_DIR, "dist")
        if os.path.exists(dist_dir):
            shutil.rmtree(dist_dir)

        try:
            res = subprocess.run([FLARE_BIN, "main.py"], cwd=DOCS_TEST_DIR, capture_output=True, text=True, timeout=5)
        except subprocess.TimeoutExpired:
            print("  -> Timed out while compiling a snippet. Skipping.")
            return original_text

        if res.returncode != 0:
            error_output = res.stderr if res.stderr else res.stdout
            match = re.search(r'File ".*?main\.py", line (\d+)', error_output)
            if match:
                line_num = int(match.group(1)) - 2
                error_msg = error_output.strip().split("\n")[-1]
                print(f"  -> Error at line {line_num}: {error_msg}")
            else:
                error_msg = error_output.strip().split("\n")[-1]
                print(f"  -> Error: {error_msg}")
            return original_text

        pack_funcs_dir = os.path.join(dist_dir, "data", "pack", "functions")
        if not os.path.exists(pack_funcs_dir):
            return original_text

        mcfunctions = []
        for root, dirs, files in os.walk(pack_funcs_dir):
            for file in sorted(files):
                if file.endswith(".mcfunction"):
                    path = os.path.join(root, file)
                    rel_path = os.path.relpath(path, pack_funcs_dir)
                    with open(path, "r", encoding="utf-8") as f:
                        mcf_content = f.read().strip()
                        if mcf_content:
                            mcfunctions.append((rel_path.replace("\\", "/"), mcf_content))

        if len(mcfunctions) == 0 or len(mcfunctions) >= 5:
            return original_text



        group = "::: code-group\n\n```python [Flare]\n" + code.strip() + "\n```\n\n"
        for name, mcf_content in mcfunctions:
            group += f"```mcfunction [{name}]\n{mcf_content}\n```\n\n"
        group += ":::"

        return group

    parts = re.split(r'(::: code-group.*?:::)', content, flags=re.DOTALL)

    new_parts = []
    for part in parts:
        if part.startswith("::: code-group"):
            match = re.search(r'^::: code-group\s*```python(?: \[.*?\])?\n(.*?)```', part, flags=re.DOTALL)
            if match:
                code = match.group(1)
                new_group = compile_and_generate_group(code, original_text=part)
                new_parts.append(new_group)
            else:
                new_parts.append(part)
        else:
            new_part = re.sub(r'```python\n(.*?)```', lambda m: compile_and_generate_group(m.group(1), m.group(0)),
                              part, flags=re.DOTALL)
            new_parts.append(new_part)

    new_content = "".join(new_parts)

    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)


print("Starting Docs Code Group Replacer...")
for root, dirs, files in sorted(os.walk(DOCS_DIR)):
    for file in sorted(files):
        if file.endswith(".md"):
            process_markdown_file(os.path.join(root, file))

print("All done!")
