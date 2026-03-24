import sys
import os
import argparse
import mimetypes
import fnmatch
from pathlib import Path

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
    parser = argparse.ArgumentParser(
        description='Squashes all files in a directory into a single text file.'
    )
    parser.add_argument('folder', type=str, help='Path to the target directory')
    parser.add_argument(
        '-i',
        '--ignore',
        nargs='*',
        default=[],
        help='Additional subfolder patterns to ignore',
    )
    parser.add_argument(
        '-e',
        '--ext',
        nargs='*',
        default=[],
        help='Additional file extensions to completely ignore',
    )
    parser.add_argument('-o', '--output', type=str, help='Custom output file path')

    args = parser.parse_args()

    ignore_dir_patterns = set(DEFAULT_IGNORE_DIRS + args.ignore)
    user_exts = {ext if ext.startswith('.') else f'.{ext}' for ext in args.ext}
    ignore_extensions = {ext.lower() for ext in DEFAULT_IGNORE_EXTS.union(user_exts)}

    target_dir = Path(args.folder).resolve()

    if not target_dir.is_dir():
        print(f"Error: The directory '{target_dir}' does not exist.")
        sys.exit(1)

    if args.output:
        output_path = Path(args.output).resolve()
        # Ensure the parent directories of the custom output path exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        output_path = target_dir.parent / f'{target_dir.name}.txt'

    print(f"Squashing '{target_dir.name}' into '{output_path}' ...")

    try:
        with open(output_path, 'w', encoding='utf-8') as outfile:
            for root, dirs, files in os.walk(target_dir):
                # In-place pruning: Modify the 'dirs' list to prevent os.walk from traversing ignored directories
                dirs[:] = [
                    d
                    for d in dirs
                    if not any(
                        fnmatch.fnmatch(d, pattern) for pattern in ignore_dir_patterns
                    )
                ]

                for file in files:
                    filepath = Path(root) / file

                    if filepath.suffix.lower() in ignore_extensions:
                        continue

                    filename = filepath.name
                    filetype, _ = mimetypes.guess_type(filepath)
                    filetype = filetype or 'unknown'

                    rel_path = filepath.relative_to(target_dir)
                    location = f'{target_dir.name}/{rel_path.as_posix()}'

                    try:
                        with open(filepath, 'r', encoding='utf-8') as infile:
                            content = infile.read()
                    except UnicodeDecodeError:
                        content = '<Binary file or invalid encoding. Content skipped.>'
                    except Exception as e:
                        content = f'<Error reading file: {e}>'

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
