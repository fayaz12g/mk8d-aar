import os
import SarcLib
import libyaz0
import sys
from functions import patch_blyt

def start_decompress(input_folder):
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".sarc"):
                file_path = os.path.join(root, file)
                decompress_sarc(file_path)

def decompress_sarc(file):
    with open(file, "rb") as inf:
        inb = inf.read()

    while libyaz0.IsYazCompressed(inb):
        inb = libyaz0.decompress(inb)

    name = os.path.splitext(os.path.basename(file))[0]
    output_folder = os.path.join(os.path.dirname(file), name)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    ext = SarcLib.guessFileExt(inb)

    if ext == ".sarc":
        arc = SarcLib.SARC_Archive()
        arc.load(inb)

        files = []

        def get_files(folder, path):
            nonlocal files

            for checkObj in folder.contents:
                if isinstance(checkObj, SarcLib.File):
                    files.append([os.path.join(path, checkObj.name), checkObj.data])
                else:
                    path_ = os.path.join(output_folder, path, checkObj.name)
                    if not os.path.isdir(path_):
                        os.makedirs(path_)
                    get_files(checkObj, os.path.join(path, checkObj.name))

        for checkObj in arc.contents:
            if isinstance(checkObj, SarcLib.File):
                files.append([checkObj.name, checkObj.data])
            else:
                path = os.path.join(output_folder, checkObj.name)
                if not os.path.isdir(path):
                    os.makedirs(path)
                get_files(checkObj, os.path.join(output_folder, checkObj.name))

        for extracted_file, fileData in files:
            print(f"Unpacking {extracted_file}")
            extracted_file_path = os.path.join(output_folder, extracted_file)
            with open(extracted_file_path, "wb") as out:
                out.write(fileData)


        os.remove(file)  # Remove the original .sarc file

        # Traverse extracted content for .szs files and decompress
        for root, dirs, files in os.walk(output_folder):
            for file in files:
                if file.lower().endswith(".szs"):
                    szs_file_path = os.path.join(root, file)
                    decompress_szs(szs_file_path)


def decompress_szs(file):
    with open(file, "rb") as inf:
        inb = inf.read()

    while libyaz0.IsYazCompressed(inb):
        inb = libyaz0.decompress(inb)

    name = os.path.splitext(os.path.basename(file))[0]  # Original .sarc file's name
    output_folder = os.path.join(os.path.dirname(file), name)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    arc = SarcLib.SARC_Archive()
    arc.load(inb)

    for checkObj in arc.contents:
        if isinstance(checkObj, SarcLib.File):
            # Extract the filename and the directories
            dirs, filename = os.path.split(checkObj.name)
            
            # Build the destination path
            dest_path = os.path.join(output_folder, dirs, filename)
            
            # Create the necessary directories
            os.makedirs(os.path.join(output_folder, dirs), exist_ok=True)
            
            # Write the file content to the destination
            with open(dest_path, "wb") as out:
                out.write(checkObj.data)


    os.remove(file)  # Remove the original .szs file