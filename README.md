# Squash 🍋

A fast Command Line Interface (CLI) tool that takes a directory and "squashes" all its files recursively into a single `.txt` file.

It automatically adds a clean header to every file, making it perfect for feeding entire codebases or project directories into Large Language Models (LLMs) for context.

## Features

- **Recursive:** Captures all files in all subdirectories.
- **Smart Pruning:** Automatically ignores heavy, irrelevant folders (like `.git` or `node_modules`) and skips binary/media files to prevent garbage text.
- **Highly Customizable:** Exclude specific folder patterns or file extensions on the fly, and define custom output locations.
- **Cross-Platform:** Works flawlessly on Windows, Linux, and macOS.
- **Context-Ready:** Prepends every file with clear metadata (Filename, Filetype, and Relative Location).

## Installation

Navigate to the folder containing the `pyproject.toml` file and install the package globally using `pip`:

```bash
pip install -e .
```

_(The `-e` flag installs it in editable mode, allowing you to update the code without reinstalling)._

## Usage

Once installed, point the `squash` command at any directory:

```bash
squash <path-to-your-folder>
```

By default, the tool creates a `.txt` file in the _parent_ directory of your target folder, named exactly like the target folder (e.g., squashing `./src` creates `./src.txt`).

### Advanced Usage

You can customize the output location and add your own filtering rules using the available flags:

```bash
# Define a custom output file path
squash ./src -o /home/user/Desktop/context.txt

# Ignore specific subfolders (e.g., 'tests' and any folder ending with '_bak')
squash ./src -i tests *_bak

# Ignore specific file extensions (e.g., CSV and JSON files)
squash ./src -e .csv .json

# Combine everything
squash ./src -o ./exports/project.txt -i legacy_code -e .md .log
```

## Output Format

Inside the generated text file, the squashed files are clearly separated and structured like this:

```text
============================================================
Filename: main.py
Filetype: text/x-python
Location: src/main.py
============================================================

def hello():
    print("Hello World")


============================================================
Filename: index.html
Filetype: text/html
Location: src/public/index.html
============================================================

<!DOCTYPE html>
<html>
<body>
    <h1>Hi</h1>
</body>
</html>
```
