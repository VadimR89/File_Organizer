import os
import shutil
import sys
import re
from collections import defaultdict
from pathlib import Path

jpeg_files = list()
png_files = list()
jpg_files = list()
svg_files = list()
txt_files = list()
docx_files = list()
doc_files = list()
xlsx_files = list()
xls_files = list()
pdf_files = list()
pptx_files = list()
avi_files = list()
mp4_files = list()
mov_files = list()
mkv_files = list()
gz_files = list()
tar_files = list()
zip_files = list()
folders = list()
others = list()
unknown = set()
extensions = set()

registered_extensions = {
    "JPEG": jpeg_files,
    "PNG": png_files,
    "JPG": jpg_files,
    "SVG": svg_files,
    "TXT": txt_files,
    "DOCX": docx_files,
    "DOC": doc_files,
    "XLSX": xlsx_files,
    "XLS": xls_files,
    "PDF": pdf_files,
    "PPTX": pptx_files,
    "ZIP": zip_files,
    "GZ": gz_files,
    "TAR": tar_files,
    "AVI": avi_files,
    "MP4": mp4_files,
    "MOV": mov_files,
    "MKV": mkv_files
}
join_extensions = {
    "JPEG": "JPEG",
    "PNG": "PNG",
    "JPG": "JPG",
    "SVG": "SVG",
    "TXT": "TXT",
    "DOCX": "DOCX",
    "DOC": "DOC",
    "XLSX": "XLSX",
    "XLS": "XLS",
    "PDF": "PDF",
    "PPTX": "PPTX",
    "ZIP": "ZIP",
    "GZ": "GZ",
    "TAR": "TAR",
    "AVI": "AVI",
    "MOV": "MOV",
    "MKV": "MKV",
    "MP4": "MP4"
}

UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p",
               "r", "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")
SPECIAL_CHARACTERS = set('!@#$%^&*()+{}[]|\:;"<>,.?/~`')
TRANS = {}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()


def main():
    scan(arg)
    scan_result()
    extract_archives_recursive(arg)
    rename_files_recursively(arg)
    find_duplicate_files(arg)
    rename_duplicate_files(arg)
    scan_and_move(arg, path, is_last_call=True)
    remove_empty_folders_recursive(arg)


def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()


def normalize(name):
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r"\W+", "_", new_name)
    return f"{new_name}.{'.'.join(extension)}"


def create_folder_if_not_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def move_file_to_folder(source_path, target_folder):
    target_path = os.path.join(target_folder, source_path.name)
    os.rename(source_path, target_path)


def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            scan(item)  # Рекурсивно викликаємо функцію для вкладених папок
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder / item.name
        if not extension:
            others.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)


def scan_result():
    if jpeg_files:
        for filename in jpeg_files:
            print(f"JPEG: {filename}")
        print()

    if jpg_files:
        for filename in jpg_files:
            print(f"JPG: {filename}")
        print()
    if png_files:
        for filename in png_files:
            print(f"PNG: {filename}")
        print()
    if svg_files:
        for filename in svg_files:
            print(f"SVG: {filename}")
        print()
    if txt_files:
        for filename in txt_files:
            print(f"TXT: {filename}")
        print()
    if docx_files:
        for filename in docx_files:
            print(f"DOCX: {filename}")
        print()
    if doc_files:
        for filename in doc_files:
            print(f"DOC: {filename}")
        print()
    if xlsx_files:
        for filename in xlsx_files:
            print(f"XLSX: {filename}")
        print()
    if xls_files:
        for filename in xls_files:
            print(f"XLS: {filename}")
        print()
    if pdf_files:
        for filename in pdf_files:
            print(f"PDF: {filename}")
        print()
    if pptx_files:
        for filename in pptx_files:
            print(f"PPTX: {filename}")
        print()
    if avi_files:
        for filename in avi_files:
            print(f"AVI: {filename}")
        print()
    if mp4_files:
        for filename in mp4_files:
            print(f"MP4: {filename}")
        print()
    if mov_files:
        for filename in mov_files:
            print(f"MOV: {filename}")
        print()
    if mkv_files:
        for filename in mkv_files:
            print(f"MKV: {filename}")
        print()
    if tar_files:
        for filename in tar_files:
            print(f"TAR: {filename}")
        print()
    if gz_files:
        for filename in gz_files:
            print(f"GZ: {filename}")
        print()
    if zip_files:
        for filename in zip_files:
            print(f"ZIP: {filename}")
        print()
    if others:
        for filename in others:
            print(f"UNKNOWN: {filename}")
        print()
    print(f"All extensions: {extensions}\n")
    print(f"Unknown extensions: {unknown}\n")


def extract_archives_recursive(folder):
    for root, dirs, files in os.walk(folder):
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

    print("Archives extracted.")


def rename_files_recursively(folder):
    for root, dirs, files in os.walk(folder):
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


def find_duplicate_files(folder):
    file_dict = defaultdict(list)

    for root, dirs, files in os.walk(folder):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_dict[filename].append(file_path)

    duplicate_files = {name: paths for name, paths in file_dict.items() if len(paths) > 1}

    if not duplicate_files:
        print("No duplicate files found.")
    else:
        print("Duplicate files:")
        for name, paths in duplicate_files.items():
            print(f"Filename: {name}")
            for path in paths:
                print(f"  Path: {path}")


def rename_duplicate_files(folder):
    file_dict = defaultdict(list)

    for root, dirs, files in os.walk(folder):
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

        for root, dirs, files in os.walk(folder):
            for filename in files:
                file_path = os.path.join(root, filename)
                file_dict[filename].append(file_path)


def scan_and_move(folder, target_root_folder, is_last_call=False):
    for item in folder.iterdir():
        # if item.is_dir():
        #     if item.name not in registered_extensions.values(): # ТАК ІГНОРУЄ ІСНУЮЧІ ПАПКИ З РОЗШИРЕННЯМИ
        #         scan_and_move(item, target_root_folder)  # Рекурсія для вкладених папок
        #     continue
        if item.is_dir():
            scan_and_move(item, target_root_folder)  # Рекурсія для вкладених папок
            continue

        extension = get_extensions(file_name=item.name)
        if not extension:
            continue

        target_folder = os.path.join(target_root_folder, join_extensions.get(extension, "OTHER"))
        create_folder_if_not_exists(target_folder)

        move_file_to_folder(item, target_folder)
    if is_last_call:
        print("Files moved and organized into folders.")


def remove_empty_folders_recursive(folder):
    for root, dirs, files in os.walk(folder, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                os.rmdir(dir_path)
                print(f"Removed empty folder: {dir_path}")
            except OSError:
                pass
    print("Empty folders removed.")


if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")
    arg = Path(path)
    main()
    print()
    print("Organize process successfully finished!")
