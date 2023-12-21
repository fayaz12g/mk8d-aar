# prompt the user for the input race.sarc
# decompress race.sarc using sarc tool into a folder called race in the same directory with it's contents which are szs files
# decompress all the szs files using yaz0 compression. each file should be decompressed into a folder with it's original name, then deleted. 
# the folders should contain folders inside (the contents of the szs) including a blyt folder.
# get the name of the root folder containing every folder decompressed in the szs and save it as "unpacked_folder". 
# set "aspect_ratio" to 2.375
# set HUD_pos to "corner"
# pass "aspect_ratio, HUD_pos, unpacked_folder" into the patch_blarc function

import subprocess
import customtkinter as ctk

race_sarc = input("Enter the path of race.sarc: ")

sarc_tool_path = r"C:\Users\fayaz\OneDrive\Documents\GitHub\mk8d-aar\sarc_tool_x64_v0.5\sarc_tool.exe"

subprocess.run([sarc_tool_path, race_sarc], check=True)


print(sarc_tool_path)