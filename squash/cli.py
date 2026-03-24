import sys
import os
import argparse
import mimetypes
import fnmatch
from pathlib import Path

# Default patterns for folders that usually contain garbage for LLMs
DEFAULT_IGNORE_DIRS = [
    '.git',
    '__pycache__',
    'node_modules',
    '.venv',
    'venv',
    'env',
    '.idea',
    '.vscode',
    'build',
    'dist',
    '*.egg-info',
]

# Default file extensions to completely skip (images, archives, binaries, etc.)
DEFAULT_IGNORE_EXTS = {
    '.pdf',
    '.zip',
    '.tar',
    '.gz',
    '.rar',
    '.7z',
    '.exe',
    '.dll',
    '.so',
    '.dylib',
    '.bin',
    '.png',
    '.jpg',
    '.jpeg',
    '.gif',
    '.svg',
    '.ico',
    '.webp',
    '.mp3',
    '.mp4',
    '.wav',
    '.avi',
    '.mov',
    '.pyc',
    '.pyd',
    '.class',
    '.o',
    '.obj',
}


def main():
    # 1. Set up the argument parser for the CLI
    parser = argparse.ArgumentParser(
        description='Squashes all files in a folder into a single text file.'
    )
    parser.add_argument(
        'folder', type=str, help='Path to the folder (relative or absolute)'
    )

    parser.add_argument(
        '-i',
        '--ignore',
        nargs='*',
        default=[],
        help='Additional subfolder patterns to ignore (e.g., -i my_folder *.bak)',
    )

    parser.add_argument(
        '-e',
        '--ext',
        nargs='*',
        default=[],
        help='Additional file extensions to completely ignore (e.g., -e .csv .json)',
    )

    args = parser.parse_args()

    # Combine default ignores with user-provided ones
    ignore_dir_patterns = set(DEFAULT_IGNORE_DIRS + args.ignore)

    # Clean up and combine extensions (ensure they start with a dot and are lowercase)
    user_exts = {ext if ext.startswith('.') else f'.{ext}' for ext in args.ext}
    ignore_extensions = {ext.lower() for ext in DEFAULT_IGNORE_EXTS.union(user_exts)}

    # 2. Resolve paths
    target_dir = Path(args.folder).resolve()

    if not target_dir.is_dir():
        print(f"Error: The directory '{target_dir}' does not exist or is not a folder.")
        sys.exit(1)

    # 3. Define output path
    parent_dir = target_dir.parent
    output_filename = f'{target_dir.name}.txt'
    output_path = parent_dir / output_filename

    print(f"Squashing '{target_dir.name}' into '{output_path}' ...")
    print(f'Ignoring folder patterns: {", ".join(ignore_dir_patterns)}')
    print(
        f'Ignoring file extensions: {", ".join(user_exts) if user_exts else "Defaults only"}'
    )

    try:
        # Open output file for writing
        with open(output_path, 'w', encoding='utf-8') as outfile:
            # 4. Iterate through directory tree using os.walk for fast pruning
            for root, dirs, files in os.walk(target_dir):
                # IN-PLACE PRUNING for directories
                dirs[:] = [
                    d
                    for d in dirs
                    if not any(
                        fnmatch.fnmatch(d, pattern) for pattern in ignore_dir_patterns
                    )
                ]

                for file in files:
                    filepath = Path(root) / file

                    # 5. Check if we should skip this file extension entirely
                    if filepath.suffix.lower() in ignore_extensions:
                        continue

                    # Gather metadata
                    filename = filepath.name

                    # Guess filetype
                    filetype, _ = mimetypes.guess_type(filepath)
                    if not filetype:
                        filetype = 'unknown'

                    # Format location: folder_name/relative_path
                    rel_path = filepath.relative_to(target_dir)
                    location = f'{target_dir.name}/{rel_path.as_posix()}'

                    # 6. Read file content (fallback protection against unexpected binary files without known extensions)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as infile:
                            content = infile.read()
                    except UnicodeDecodeError:
                        content = '<Binary file or invalid encoding. Content skipped.>'
                    except Exception as e:
                        content = f'<Error reading file: {e}>'

                    # 7. Write header and content
                    outfile.write('=' * 60 + '\n')
                    outfile.write(f'Filename: {filename}\n')
                    outfile.write(f'Filetype: {filetype}\n')
                    outfile.write(f'Location: {location}\n')
                    outfile.write('=' * 60 + '\n\n')
                    outfile.write(content)
                    outfile.write('\n\n')

        print('Done! 🎉')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
