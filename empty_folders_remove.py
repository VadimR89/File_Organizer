import os
import sys
from pathlib import Path


def remove_empty_folders_recursive(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                os.rmdir(dir_path)
                print(f"Removed empty folder: {dir_path}")
            except OSError:
                pass


if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")
    arg = Path(path)
    remove_empty_folders_recursive(path)
    print("Empty folders removed.")

