# Squash 🍋

A simple, fast Command Line Interface (CLI) tool that takes a directory and "squashes" all its files recursively into a single `.txt` file.

It automatically adds a clean header to every file, making it perfect for feeding entire codebases or project directories into Large Language Models (LLMs) for context.

## Features

- **Recursive:** Captures all files in all subdirectories.
- **Smart:** Automatically detects and skips binary files to prevent garbage text.
- **Cross-Platform:** Works flawlessly on Windows, Linux, and macOS.
- **Context-Ready:** Prepends every file with clear metadata (Filename, Filetype, and Relative Location).

## Installation

1. Open your terminal and navigate to the folder containing the `pyproject.toml` file.
2. Install the package globally using `pip`:

```bash
pip install -e .
```

_(The `-e` flag installs it in editable mode, so you can tweak the code later without having to reinstall it)._

## Usage

Once installed, the `squash` command is available system-wide. Simply point it at any directory (relative or absolute):

```bash
squash <path-to-your-folder>
```

**Examples:**

```bash
# Squash a folder in the current directory
squash ./frontend

# Squash a folder using an absolute path (Windows)
squash C:\Users\Projects\MyCode
```

## Output Format

The tool will create a `.txt` file in the _parent_ directory of your target folder, named exactly like the target folder (e.g., `MyCode.txt`).

Inside, the squashed files are clearly separated and structured like this:

```text
============================================================
Filename: main.py
Filetype: text/x-python
Location: MyCode/src/main.py
============================================================

def hello():
    print("Hello World")


============================================================
Filename: index.html
Filetype: text/html
Location: MyCode/public/index.html
============================================================

<!DOCTYPE html>
<html>
<body>
    <h1>Hi</h1>
</body>
</html>
```
