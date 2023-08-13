import sys
from pathlib import Path

jpeg_files = list()  # файли зображень
png_files = list()  # файли зображень
jpg_files = list()  # файли зображень
svg_files = list()  # файли зображень
txt_files = list()  # файли документів
docx_files = list()  # файли документів
doc_files = list()  # файли документів
xlsx_files = list()  # файли документів
xls_files = list()  # файли документів
pdf_files = list()  # файли документів
pptx_files = list()  # файли документів
avi_files = list()  # файли відео
mp4_files = list()  # файли відео
mov_files = list()  # файли відео
mkv_files = list()  # файли відео
folders = list()
zip_files = list()
gz_files = list()
tar_files = list()
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


def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()


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


if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)
    scan(arg)

if (jpeg_files):
    for filename in jpeg_files:
        print(f"JPEG: {filename}")
    print()

if (jpg_files):
    for filename in jpg_files:
        print(f"JPG: {filename}")
    print()

if (png_files):
    for filename in png_files:
        print(f"PNG: {filename}")
    print()

if (svg_files):
    for filename in svg_files:
        print(f"SVG: {filename}")
    print()

if (txt_files):
    for filename in txt_files:
        print(f"TXT: {filename}")
    print()

if(docx_files):
    for filename in docx_files:
        print(f"DOCX: {filename}")
    print()

if(doc_files):
    for filename in doc_files:
        print(f"DOC: {filename}")
    print()

if(xlsx_files):
    for filename in xlsx_files:
        print(f"XLSX: {filename}")
    print()

if(xls_files):
    for filename in xls_files:
        print(f"XLS: {filename}")
    print()

if(pdf_files):
    for filename in pdf_files:
        print(f"PDF: {filename}")
    print()

if(pptx_files):
    for filename in pptx_files:
        print(f"PPTX: {filename}")
    print()

if(avi_files):
    for filename in avi_files:
        print(f"AVI: {filename}")
    print()

if(mp4_files):
    for filename in mp4_files:
        print(f"MP4: {filename}")
    print()

if(mov_files):
    for filename in mov_files:
        print(f"MOV: {filename}")
    print()

if(mkv_files):
    for filename in mkv_files:
        print(f"MKV: {filename}")
    print()

if(tar_files):
    for filename in tar_files:
        print(f"TAR: {filename}")
    print()

if(gz_files):
    for filename in gz_files:
        print(f"GZ: {filename}")
    print()

if(zip_files):
    for filename in zip_files:
        print(f"ZIP: {filename}")
    print()

if(others):
    for filename in others:
        print(f"UNKNOWN: {filename}")
    print()

print(f"All extensions: {extensions}\n")
print(f"Unknown extensions: {unknown}\n")
