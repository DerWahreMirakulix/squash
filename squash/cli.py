import sys
import os
import argparse
import mimetypes
import fnmatch
from pathlib import Path

# Default patterns for directories and specific files to ignore
DEFAULT_IGNORE_PATTERNS = [
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
    '.DS_Store',
    'Thumbs.db',
    '.gitignore',
    'todo',
    '*.squash.txt',
]

# Default file extensions to skip (binary/large files)
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


def is_ignored(name, suffix, ignore_patterns, ignore_extensions):
    """Check if a file or directory should be ignored based on name or extension."""
    if suffix.lower() in ignore_extensions:
        return True
    if any(fnmatch.fnmatch(name, p) for p in ignore_patterns):
        return True
    return False


def build_tree(dir_path, ignore_patterns, ignore_extensions, prefix=''):
    """Recursively builds a string representation of the directory tree."""
    tree_lines = []

    # Get all items, sort them (directories first, then files)
    try:
        items = sorted(
            list(dir_path.iterdir()), key=lambda x: (x.is_file(), x.name.lower())
        )
    except PermissionError:
        return [f'{prefix} [Permission Denied]']

    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        connector = '└── ' if is_last else '├── '

        ignored_label = ''
        # Check if this specific item is ignored
        if is_ignored(item.name, item.suffix, ignore_patterns, ignore_extensions):
            ignored_label = ' [IGNORED]'

        tree_lines.append(f'{prefix}{connector}{item.name}{ignored_label}')

        if item.is_dir():
            # If the directory itself is ignored, we don't necessarily need to list sub-items
            # but for the tree structure, we stop recursion here if ignored.
            if not ignored_label:
                extension = '    ' if is_last else '│   '
                tree_lines.extend(
                    build_tree(
                        item, ignore_patterns, ignore_extensions, prefix + extension
                    )
                )

    return tree_lines


def main():
    parser = argparse.ArgumentParser(
        description='Squashes directory content into one file with a tree overview.'
    )
    parser.add_argument(
        'folder', type=str, nargs='?', help='Path to the target directory'
    )
    parser.add_argument(
        '-i', '--ignore', nargs='*', default=[], help='Additional ignore patterns'
    )
    parser.add_argument(
        '-e', '--ext', nargs='*', default=[], help='Additional ignore extensions'
    )
    parser.add_argument(
        '-a',
        '--allow',
        nargs='*',
        default=[],
        help='Override: allow specific default patterns',
    )
    parser.add_argument(
        '-ae',
        '--allow-ext',
        nargs='*',
        default=[],
        help='Override: allow specific default extensions',
    )
    parser.add_argument(
        '--no-defaults', action='store_true', help='Disable all default ignore rules'
    )
    parser.add_argument(
        '--show-ignored', action='store_true', help='Show default ignore lists and exit'
    )
    parser.add_argument('-o', '--outdir', type=str, help='Output directory')

    args = parser.parse_args()

    if args.show_ignored:
        print(
            '\n=== Default Ignore Patterns ===\n '
            + '\n '.join(sorted(DEFAULT_IGNORE_PATTERNS))
        )
        print(
            '\n=== Default Ignore Extensions ===\n '
            + '\n '.join(sorted(DEFAULT_IGNORE_EXTS))
            + '\n'
        )
        sys.exit(0)

    if not args.folder:
        parser.error('the following arguments are required: folder')

    # Setup Ignore Sets
    if args.no_defaults:
        ignore_patterns = set(args.ignore)
        ignore_extensions = {
            e.lower() if e.startswith('.') else f'.{e.lower()}' for e in args.ext
        }
    else:
        ignore_patterns = set(DEFAULT_IGNORE_PATTERNS + args.ignore)
        user_exts = {
            e.lower() if e.startswith('.') else f'.{e.lower()}' for e in args.ext
        }
        ignore_extensions = {e.lower() for e in DEFAULT_IGNORE_EXTS.union(user_exts)}

    # Process Overrides
    for p in args.allow:
        if p in ignore_patterns:
            ignore_patterns.remove(p)
    for e in args.allow_ext:
        norm_e = e.lower() if e.startswith('.') else f'.{e.lower()}'
        if norm_e in ignore_extensions:
            ignore_extensions.remove(norm_e)

    target_dir = Path(args.folder).resolve()
    if not target_dir.is_dir():
        print(f"Error: Target '{target_dir}' not found.")
        sys.exit(1)

    output_dir = Path(args.outdir).resolve() if args.outdir else target_dir.parent
    if not output_dir.is_dir():
        print(f"Error: Output directory '{output_dir}' not found.")
        sys.exit(1)

    output_path = output_dir / f'{target_dir.name}.squash.txt'

    print(f"Squashing '{target_dir.name}' into '{output_path}'...")

    try:
        with open(output_path, 'w', encoding='utf-8') as outfile:
            # --- PHASE 1: Write Tree Header ---
            outfile.write('=' * 60 + '\n')
            outfile.write('PROJECT STRUCTURE OVERVIEW\n')
            outfile.write(f'Target: {target_dir.name}\n')
            outfile.write('=' * 60 + '\n\n')
            tree = build_tree(target_dir, ignore_patterns, ignore_extensions)
            outfile.write(target_dir.name + '\n')
            outfile.write('\n'.join(tree) + '\n\n')

            # --- PHASE 2: Squash Files ---
            for root, dirs, files in os.walk(target_dir):
                # Prune ignored directories
                dirs[:] = [
                    d for d in dirs if not is_ignored(d, '', ignore_patterns, set())
                ]

                for file in files:
                    filepath = Path(root) / file

                    # Safety and Ignore Checks
                    if is_ignored(
                        file, filepath.suffix, ignore_patterns, ignore_extensions
                    ):
                        continue
                    if filepath.resolve() == output_path.resolve():
                        continue

                    filetype, _ = mimetypes.guess_type(filepath)
                    rel_path = filepath.relative_to(target_dir)

                    outfile.write('=' * 60 + '\n')
                    outfile.write(f'Filename: {file}\n')
                    outfile.write(f'Filetype: {filetype or "unknown"}\n')
                    outfile.write(
                        f'Location: {target_dir.name}/{rel_path.as_posix()}\n'
                    )
                    outfile.write('=' * 60 + '\n\n')

                    try:
                        with open(filepath, 'r', encoding='utf-8') as infile:
                            outfile.write(infile.read())
                    except UnicodeDecodeError:
                        outfile.write(
                            '<Binary file or invalid encoding. Content skipped.>'
                        )
                    except Exception as e:
                        outfile.write(f'<Error reading file: {e}>')

                    outfile.write('\n\n')

        print('Done! 🎉')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
