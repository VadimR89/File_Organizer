import os
import shutil
import sys
from pathlib import Path


def extract_archives_recursive(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                extract_folder = os.path.splitext(file_path)[0]  # Створюємо папку для розпакованих файлів
                shutil.unpack_archive(file_path, extract_folder)
                print(f"Extracted {file_path} to {extract_folder}")
            except shutil.ReadError:
                pass
            except Exception as e:
                print(f"Failed to extract {file_path}: {e}")


if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)

    extract_archives_recursive(path)
    print("Archives extracted.")