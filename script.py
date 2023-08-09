import os
import sys
import SarcLib
import libyaz0
import struct
import math
import ast
from compress import pack 
from compress import pack_folder_to_blarc
import customtkinter
import tkinter
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter.filedialog import askdirectory
from customtkinter import *
from threading import Thread
import shutil
from download import download_extract_copy
from patch import create_patch_files
from functions import float2hex

def patch_blarc(aspect_ratio, HUD_pos, unpacked_folder):
    from functions import float2hex
    
    unpacked_folder = str(unpacked_folder)
    aspect_ratio = float(aspect_ratio)
    print(f"Aspect ratio is {aspect_ratio}")
    HUD_pos = str(HUD_pos)
     
    def patch_blyt(filename, pane, operation, value):
        if value < 1:
            command = "Squishing"
        if value > 1:
            command = "Stretching"
        if value == 1:
            command = "Ignoring"
        print(f"{command} {pane} of {filename}")
        offset_dict = {'shift_x': 0x40, 'shift_y': 0x48, 'scale_x': 0x70, 'scale_y': 0x78} 
        modified_name = filename + "_name"
        full_path_of_file = file_paths.get(modified_name)
        with open(full_path_of_file, 'rb') as f:
            content = f.read().hex()
        start_rootpane = content.index(b'RootPane'.hex())
        pane_hex = str(pane).encode('utf-8').hex()
        start_pane = content.index(pane_hex, start_rootpane)
        idx = start_pane + offset_dict[operation]
        content_new = content[:idx] + float2hex(value) + content[idx+8:]
        with open(full_path_of_file, 'wb') as f:
            f.write(bytes.fromhex(content_new))


    def patch_anim(filename, offset, value):
        full_path = os.path.join(unpacked_folder, 'anim', f'{filename}.bflan')
        with open(full_path, 'rb') as f:
            content = f.read().hex()
        idx = offset
        content_new = content[:idx] + float2hex(value) + content[idx+8:]
        with open(full_path, 'wb') as f:
            f.write(bytes.fromhex(content_new))  

    file_paths = {}

    blyt_folder = os.path.abspath(os.path.join(unpacked_folder))
    file_names_stripped = []
   
    do_not_scale_rootpane = ['WipeCircle']

    for root, dirs, files in os.walk(blyt_folder):
        for file_name in files:
            if file_name.endswith(".bflyt"):
                file_names_stripped.append(file_name.strip(".bflyt"))
                stripped_name = file_name.strip(".bflyt")
                full_path = os.path.join(root, file_name)
                modified_name = stripped_name + "_name"
                file_paths[modified_name] = full_path
                if file_names_stripped in do_not_scale_rootpane:
                    print(f"Skipping RootPane scaling of {name}")

    
    if aspect_ratio >= 16/9:
        s1 = (16/9) / aspect_ratio
        print(f"Scaling factor is set to {s1}")
        s2 = 1-s1
        s3 = s2/s1
        
        for name in file_names_stripped:
            if name not in do_not_scale_rootpane:
                patch_blyt(name, 'RootPane', 'scale_x', s1)

        patch_blyt('TalkMessage', 'PicBase', 'scale_x', 1/s1)
        patch_blyt('PlayGuide', 'PicBase', 'scale_x', 1/s1)
        patch_blyt('PlayGuideMovie', 'PicMovie', 'scale_x', 1/s1)
        patch_blyt('TalkMessage', 'PicBase', 'scale_x', 1/s1)
        # patch_blyt('ContinueLoading', 'ParBG', 'shift_x', 1/s1) 
        # patch_blyt('BootLoading', 'ParBG', 'shift_x', 1/s1) 
        # patch_blyt('ContinueLoading', 'PicFooter', 'shift_x', 1/s1) 
        # patch_blyt('ContinueLoading', 'PicFooterBar', 'shift_x', 1/s1) 
        # patch_blyt('ContinueLoading', 'PicProgressBar', 'shift_x', 1/s1) 
        
        
        if HUD_pos == 'corner':
            print("Shifitng elements for corner HUD")
            patch_blyt('MapMini', 'RootPane', 'shift_x', 660*s2) 
            patch_blyt('CounterLife', 'RootPane', 'shift_x', 660*s2) 
            patch_blyt('CounterCoin', 'RootPane', 'shift_x', -660*s2) 
            patch_blyt('SaveMessage', 'All', 'shift_x', -660*s2) 
            patch_blyt('CounterCollectCoin', 'RootPane', 'shift_x', -660*s2) 
            patch_blyt('CounterLifeUp', 'RootPane', 'shift_x', 660*s2) 
            patch_blyt('CounterLifeKids', 'RootPane', 'shift_x', 660*s2) 
            
    else:
        s1 = aspect_ratio / (16/9)
        s2 = 1-s1
        s3 = s2/s1
        
        for name in file_names_stripped:
            if name in do_not_scale_rootpane:
                print(f"Skipping root pane scaling of {name}")
            if name not in do_not_scale_rootpane:
                print(f"Scaling root pane vertically for {name}")
                patch_blyt(name, 'RootPane', 'scale_y', s1)
             
        # patch_anim('PaMapIconDragonTears_00_Zoom', 672, 1.28/s1)

        if HUD_pos == 'corner':
            print("Shifitng elements for corner HUD")
            # patch_blyt('ChallengeLog_00', 'RootPane', 'shift_y', 540*s2)