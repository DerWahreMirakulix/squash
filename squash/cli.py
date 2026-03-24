import sys
import argparse
import mimetypes

from pathlib import Path


def main():
    # 1. Set up the argument parser for the CLI
    parser = argparse.ArgumentParser(
        description='Squashes all files in a folder into a single text file.'
    )
    parser.add_argument(
        'folder', type=str, help='Path to the folder (relative or absolute)'
    )
    args = parser.parse_args()

    # 2. Resolve paths (converts relative paths to absolute paths)
    target_dir = Path(args.folder).resolve()

    if not target_dir.is_dir():
        print(f"Error: The directory '{target_dir}' does not exist or is not a folder.")
        sys.exit(1)

    # 3. Define output path (in the parent directory, named after the target folder)
    parent_dir = target_dir.parent
    output_filename = f'{target_dir.name}.txt'
    output_path = parent_dir / output_filename

    print(f"Squashing '{target_dir.name}' into '{output_path}' ...")

    try:
        # Open output file for writing
        with open(output_path, 'w', encoding='utf-8') as outfile:
            # 4. Iterate through all files recursively
            for filepath in target_dir.rglob('*'):
                if filepath.is_file():
                    # Gather metadata
                    filename = filepath.name

                    # Guess filetype (e.g., 'text/plain', 'image/png')
                    filetype, _ = mimetypes.guess_type(filepath)
                    if not filetype:
                        filetype = 'unknown'

                    # Format location: folder_name/relative_path
                    rel_path = filepath.relative_to(target_dir)
                    # .as_posix() ensures forward slashes (/) are used, even on Windows
                    location = f'{target_dir.name}/{rel_path.as_posix()}'

                    # 5. Read file content (with protection against binary files)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as infile:
                            content = infile.read()
                    except UnicodeDecodeError:
                        content = '<Binary file or invalid encoding. Content skipped.>'
                    except Exception as e:
                        content = f'<Error reading file: {e}>'

                    # 6. Write header and content to the output file
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
