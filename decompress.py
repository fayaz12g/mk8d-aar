import os
import SarcLib
import libyaz0
import sys
from functions import patch_blyt
import subprocess

def start_decompress(input_folder):
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".sarc"):
                file_path = os.path.join(root, file)
                decompress_sarc(file_path)

def decompress_sarc(file):
    sarc_tool_path = r"C:\Users\fayaz\OneDrive\Documents\GitHub\mk8d-aar\sarc_tool_x64_v0.5\sarc_tool.exe"
    subprocess.run([sarc_tool_path, file], check=True)

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