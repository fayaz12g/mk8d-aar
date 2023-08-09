import os
import SarcLib
import libyaz0
import sys
from functions import patch_blyt

def start_decompress(input_folder):

    if not os.path.exists(input_folder):
        print(f"Error: Folder '{input_folder}' does not exist.")
        sys.exit(1)

    if not os.path.isdir(input_folder):
        print("Error: The input must be a folder path.")
        sys.exit(1)

    for file in os.listdir(input_folder):
        if file.lower().endswith(".szs"):
            file_path = os.path.join(input_folder, file)
            extract_blarc(file_path, input_folder)

def extract_blarc(file, output_folder):
    """
    Extract the given archive.
    """

    with open(file, "rb") as inf:
        inb = inf.read()

    while libyaz0.IsYazCompressed(inb):
        inb = libyaz0.decompress(inb)

    name = os.path.splitext(os.path.basename(file))[0]  # Extract the base name of the file without extension
    ext = SarcLib.guessFileExt(inb)

    if ext != ".sarc":
        with open(os.path.join(output_folder, ''.join([name, ext])), "wb") as out:
            out.write(inb)
    else:
        arc = SarcLib.SARC_Archive()
        arc.load(inb)

        root = os.path.join(output_folder, name)  # Output path will be in the specified output folder
        if not os.path.isdir(root):
            os.makedirs(root)

        files = []

        def getAbsPath(folder, path):
            nonlocal root
            nonlocal files

            for checkObj in folder.contents:
                if isinstance(checkObj, SarcLib.File):
                    files.append([os.path.join(path, checkObj.name), checkObj.data])
                else:
                    path_ = os.path.join(root, path, checkObj.name)
                    if not os.path.isdir(path_):
                        os.makedirs(path_)
                    getAbsPath(checkObj, os.path.join(path, checkObj.name))

        for checkObj in arc.contents:
            if isinstance(checkObj, SarcLib.File):
                files.append([checkObj.name, checkObj.data])
            else:
                path = os.path.join(root, checkObj.name)
                if not os.path.isdir(path):
                    os.makedirs(path)
                getAbsPath(checkObj, os.path.join(root, checkObj.name))

        for extracted_file, fileData in files:
            print(f"Unpacking {extracted_file}")
            extracted_file_path = os.path.join(root, extracted_file)
            with open(extracted_file_path, "wb") as out:
                out.write(fileData)

            # if extracted_file.endswith("bflyt"):
                # patch_blyt(extracted_file_path, "RootPane", "scale_x", scaling_factor)

        layout_lyarc = os.path.join(root, "layout.lyarc")
        if os.path.exists(layout_lyarc):
            extract_blarc(layout_lyarc, root)
            # os.remove(layout_lyarc)

    os.remove(file)