import os
import sys
from collections import defaultdict
from pathlib import Path


def rename_duplicate_files(folder_path):
    file_dict = defaultdict(list)

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_dict[filename].append(file_path)

    while True:
        duplicate_files = {name: paths for name, paths in file_dict.items() if len(paths) > 1}
        if not duplicate_files:
            break

        for name, paths in duplicate_files.items():
            base_name, extension = os.path.splitext(name)
            index = 1
            new_paths = []

            for path in paths:
                new_name = f"{base_name}_{index}{extension}"
                new_path = os.path.join(os.path.dirname(path), new_name)

                while os.path.exists(new_path):
                    index += 1
                    new_name = f"{base_name}_{index}{extension}"
                    new_path = os.path.join(os.path.dirname(path), new_name)

                new_paths.append(new_path)
                index += 1

            for old_path, new_path in zip(paths, new_paths):
                os.rename(old_path, new_path)
                print(f"Renamed {old_path} to {new_path}")

        file_dict.clear()

        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                file_dict[filename].append(file_path)


if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")
    arg = Path(path)
    rename_duplicate_files(path)
