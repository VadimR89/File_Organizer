import os
import re
import sys
from pathlib import Path

UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p",
               "r", "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")
SPECIAL_CHARACTERS = set('!@#$%^&*()_+{}[]|\:;"<>,.?/~`')

TRANS = {}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()


def normalize(name):
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r"\W+", "_", new_name)
    return f"{new_name}.{'.'.join(extension)}"


def rename_files_recursively(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            old_path = os.path.join(root, filename)

            if any(c.isalpha() and (c.lower() in UKRAINIAN_SYMBOLS) for c in filename):
                normalized_name = normalize(filename)
                base_name, ext = os.path.splitext(normalized_name)
                new_name = base_name
                index = 1
                while os.path.exists(os.path.join(root, new_name + ext)):
                    new_name = f"{base_name}_{index}"
                    index += 1
                new_name += ext

            else:
                new_name = filename

            if any(char in SPECIAL_CHARACTERS for char in filename):
                normalized_name = normalize(filename)
                base_name, ext = os.path.splitext(normalized_name)
                new_name = base_name
                index = 1
                while os.path.exists(os.path.join(root, new_name + ext)):
                    new_name = f"{base_name}_{index}"
                    index += 1
                new_name += ext
            else:
                new_name = filename

            new_path = os.path.join(root, new_name)
            os.rename(old_path, new_path)
            print(f"Normalized {filename} to {new_name}")


if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")
    arg = Path(path)
    rename_files_recursively(path)
