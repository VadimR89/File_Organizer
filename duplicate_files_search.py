import os
import sys
from collections import defaultdict
from pathlib import Path


def find_duplicate_files(folder_path):
    file_dict = defaultdict(list)

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_dict[filename].append(file_path)

    duplicate_files = {name: paths for name, paths in file_dict.items() if len(paths) > 1}

    return duplicate_files


if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")
    arg = Path(path)
    duplicates = find_duplicate_files(path)

    if not duplicates:
        print("No duplicate files found.")
    else:
        print("Duplicate files:")
        for name, paths in duplicates.items():
            print(f"Filename: {name}")
            for path in paths:
                print(f"  Path: {path}")
