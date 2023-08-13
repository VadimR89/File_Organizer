import os
import sys
from pathlib import Path

registered_extensions = {
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
    "MP4": "MP4",
    "MOV": "MOV",
    "MKV": "MKV"
}


def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()


def move_file_to_folder(source_path, target_folder):
    target_path = os.path.join(target_folder, source_path.name)
    os.rename(source_path, target_path)


def scan_and_move(folder, target_root_folder):
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

        target_folder = os.path.join(target_root_folder, registered_extensions.get(extension, "OTHER"))
        create_folder_if_not_exists(target_folder)

        move_file_to_folder(item, target_folder)


if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)
    scan_and_move(arg, path)

    print("Files moved and organized into folders.")
