# Squash 🍋

A fast Command Line Interface (CLI) tool that takes a directory and "squashes" all its files recursively into a single `.squash.txt` file.

It automatically adds a clean header to every file, making it perfect for feeding entire codebases or project directories into Large Language Models (LLMs) for context.

## Features

- **Recursive:** Captures all files in all subdirectories.
- **Project Structure Overview:** Generates a visual directory tree at the top of the file, clearly marking ignored items with `[IGNORED]`.
- **Smart Pruning:** Automatically ignores heavy folders (like `.git`, `node_modules`) and skips binary/media files.
- **Pattern Matching:** Use wildcard patterns (e.g., `temp_*`, `*.log`) to ignore specific files or directories.
- **Auto-Naming:** Generates the output file based on the target folder name with a unique `.squash.txt` suffix.
- **Override Defaults:** Easily "un-ignore" default patterns or disable all defaults entirely.
- **Context-Ready:** Prepends every file with clear metadata (Filename, Filetype, and Relative Location).

## Installation

Navigate to the folder containing the `pyproject.toml` file and install the package globally using `pip`:

```bash
pip install -e .
```

_(The `-e` flag installs it in editable mode, allowing you to update the code without reinstalling)._

## Usage

Point the `squash` command at any directory:

```bash
squash <path-to-your-folder>
```

By default, the tool creates `folder_name.squash.txt` in the **parent directory** of your target folder.

### Inspecting & Overriding Defaults

Squash comes with a built-in list of ignored folders and extensions.

```bash
# See what is currently ignored by default
squash --show-ignored

# Disable all built-in ignore lists and only use your own
squash ./src --no-defaults -i secret_folder

# Include specific default-ignored items (e.g., .git folder and images)
squash ./src -a .git -ae .png .jpg
```

### Advanced Filtering

```bash
# Save the result into a specific directory
squash ./src -o ./my_exports

# Ignore additional specific files or patterns
squash ./src -i config.json test_*

# Ignore additional file extensions
squash ./src -e .csv .json
```

> **Note:** If you provide an output directory via `-o`, it must already exist. If the directory is missing, the tool will exit with an error to prevent accidental file placement.

## Output Format

Inside the generated `.squash.txt` file, you will first see a complete overview followed by the file contents:

```text
============================================================
PROJECT STRUCTURE OVERVIEW
Target: my-app
============================================================

my-app
├── .git [IGNORED]
├── src
│   ├── main.py
│   └── utils.py
├── node_modules [IGNORED]
└── package.json

============================================================
Filename: main.py
Filetype: text/x-python
Location: my-app/src/main.py
============================================================

def hello():
    print("Hello World")


============================================================
Filename: package.json
Filetype: application/json
Location: my-app/package.json
============================================================

{
  "name": "my-app",
  "version": "1.0.0"
}
```
