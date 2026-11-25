import zipfile
from pathlib import Path

# Files bundled into code.zip for the web (Pyodide) build
FILES = ['minesweeper.py', 'flag.png']


def create_code_zip():
    with zipfile.ZipFile('code.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
        for name in FILES:
            path = Path(name)
            if not path.is_file():
                raise FileNotFoundError(f"Missing required file: {name}")
            zf.write(path, name)

    print("Files included in code.zip:")
    for name in FILES:
        print(f"  - {name}")


if __name__ == '__main__':
    create_code_zip()
