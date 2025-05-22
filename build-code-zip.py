import zipfile
from pathlib import Path
from itertools import chain


def create_code_zip():
    current_dir = Path('.')

    # Create a manifest of files being included
    included_files = []

    with zipfile.ZipFile('code.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
        # Combine game.py and map.json rglob generators
        for file_path in chain(current_dir.rglob('minesweeper.py'), current_dir.rglob('flag.png')):
            if file_path.is_file():
                zf.write(file_path, file_path.relative_to(current_dir.parent))
                included_files.append(str(file_path))

    print("Files included in code.zip:")
    for file in included_files:
        print(f"  - {file}")


if __name__ == '__main__':
    create_code_zip()
