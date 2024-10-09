import os
import sys
import SarcLib
import libyaz0
import struct
import math
import ast
from compress import pack 
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
from functions import *

def patch_blarc(aspect_ratio, HUD_pos, unpacked_folder):
    from functions import float2hex
    
    unpacked_folder = str(unpacked_folder)
    aspect_ratio = float(aspect_ratio)
    print(f"Aspect ratio is {aspect_ratio}")
    HUD_pos = str(HUD_pos)
    
    
    layout_map = {
                    'hash_0x196a863d': ['N_LensFlare_00', 'N_All_01'], # Title Loading
                    'hash_0xca612e43': ['L_RaceNum_00', 'L_BtTimer_Ml', 'N_BtInfoView_01', 'N_BtInfoView_00', 'L_BtStartRule_00', 'L_BtKeidoroWantedPos00', 'L_BtTeamScore_00', 'L_ShineScore_00'], # rc_RaceView_cmn_00
                    'hash_0xb061c76e': ['L_BtScore_00', 'L_BtCoinCount_00', 'L_BtKeidoroCoin_00', 'L_Alarm_00', 'L_Alarm_01', 'N_ItemBoxPos_00', 'L_Rank_00', 'L_LapCoin_00'], # rc_RaceView_1P_00
                    'hash_0xa136fd7c': ['N_BtScore_MlTeamPos_00', 'L_BtCoinCount_00', 'L_BtKeidoroCoin_00', 'L_BtStartRule_00'], # rc_RaceView_2P_MI
                    'hash_0x639520ee': ['N_BtScore_MlTeamPos_00', 'L_BtCoinCount_00', 'L_BtKeidoroCoin_00', 'L_BtStartRule_00'], # rc_RaceView_4P_MI
                    'hash_0x4141b313': ['N_All_00'], # rc_Result_00
                    'hash_0xcc5d377a': ['N_Single_00','N_Multi_00','N_Multi_Open_00','N_Multi_Open_01','N_Multi_Open_02','N_Multi_Open_03','N_Multi_Open_04','N_Single_Open_00','N_Single_Open_01','N_Single_Open_02','N_Single_Open_03','N_Single_Open_04',
                                         'N_Online_00','N_LocalCommun_00','N_Record_00','N_amiibo_00','N_MKTV_00','N_Html_00','N_LABO_00','N_DLC_00','N_Sound_00',
                                         'P_BoardShM_00','P_BoardShL_00','W_BoardBlur_M_00','W_BoardBlur_L_00', 'P_Sparkle_01','P_Monogram_01','P_Monogram_02','P_Sparkle_02'], # mn_Background_00
                    # 'hash_0xb291a57f':['N_null_00','N_Loop_00','N_Loop_01'], # cmn_LoadScreen_00
                    'hash_0x9a7a5a0e': ['N_PressABtn_00','N_Logo_00'], # mn_TitleScreen_00
                    'hash_0x6ec7bb3c': ['N_Btn_00'], # mn_TopMenuNX_00
                    'hash_0x44e1a771': ['N_Board_00', 'N_Single_00', 'N_Multi_00'], # mn_ModeSlct_00

                }

    def patch_ui_layouts(direction):
        if direction == "x":
            offset = 0x40
        if direction == 'y':
            offset = 0x48

        for filename, panes in layout_map.items():
            modified_name = filename + "_name"
            path = file_paths.get(modified_name, [])
            print("Shifting", modified_name)
            
            with open(path, 'rb') as f:
                content = f.read().hex()
                
                start_rootpane = content.index(b'RootPane'.hex())
                
                for pane in panes:
                    pane_hex = pane.encode('utf-8').hex()
                    start_pane = content.index(pane_hex, start_rootpane)
                    idx = start_pane + offset 
                    
                    current_value_hex = content[idx:idx+8]
                    current_value = hex2float(current_value_hex)
                    
                    new_value = (current_value * s1**-1)
                    new_value_hex = float2hex(new_value)
                    
                    content = content[:idx] + new_value_hex + content[idx+8:]
                
                with open(path, 'wb') as f:
                    f.write(bytes.fromhex(content))
    
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
   
    do_not_scale_rootpane = [
                            'hash_0xb061c76e', #rc_RaceView_1P_00 in Race
                            'hash_0x904e307e', # rc_Viewer_00 in Race
                            'hash_0x5078a7b0', # Fade Pause
                            'hash_0xc1e2251e', # Page Fade 
                            'hash_0x79edb528', # Page Fade Pause
                            'hash_0x1ef48ed7', # mn_L_BlurBG_00
                            ]
    
    rootpane_stretch_y = ['hash_0xcc5d377a', # Background in Menu
                          'hash_0xb291a57f' # Loading Screen
                          ]

    rootpane_stretch_x = ['hash_0xcc5d377a', # Background in Menu
                          'hash_0xb291a57f' # Loading Screen
                          ]
    
    for root, dirs, files in os.walk(blyt_folder):
        for file_name in files:
            if file_name.endswith(".bflyt"):
                file_names_stripped.append(file_name.strip(".bflyt"))
                stripped_name = file_name.strip(".bflyt")
                full_path = os.path.join(root, file_name)
                modified_name = stripped_name + "_name"
                file_paths[modified_name] = full_path
                if file_names_stripped in do_not_scale_rootpane:
                    print(f"Skipping RootPane horizontal scaling of {name}")

    
    if aspect_ratio >= 16/9:
        s1 = (16/9) / aspect_ratio
        print(f"Scaling factor is set to {s1}")
        s2 = 1-s1
        s3 = s2/s1
        
        for name in file_names_stripped:
            if name not in do_not_scale_rootpane:
                patch_blyt(name, 'RootPane', 'scale_x', s1)
        for name in file_names_stripped:
            if name in rootpane_stretch_y:
                patch_blyt(name, 'RootPane', 'scale_y', 1/s1)
        
        patch_blyt('hash_0x9a7a5a0e', 'N_Capture_0', 'scale_x', 1/s1) # Title Screen Background

        patch_blyt('hash_0xb061c76e', 'N_Pause_00', 'scale_x', s1) # Player HUD 

        patch_blyt('hash_0xb061c76e', 'N_All_00', 'scale_x', s1) # Player HUD 
        patch_blyt('hash_0x4141b313', 'RootPane', 'scale_x', s1) #RC Result
        patch_blyt('hash_0x64f64f62', 'RootPane', 'scale_x', s1) #RC Result Team
        patch_blyt('hash_0x468a66a', 'RootPane', 'scale_x', s1) #RC Result TIme Trial

        patch_blyt('hash_0x196a863d', 'RootPane', 'scale_x', s1) # bt_TitleLoading_00

        patch_blyt('hash_0x196a863d', 'N_Logo_01', 'scale_x', s1) # bt_TitleLoading_00
        patch_blyt('hash_0x196a863d', 'N_Logo_00', 'scale_x', s1) # bt_TitleLoading_00

        patch_blyt('hash_0x196a863d', 'N_All_01', 'scale_y', 1/s1) # bt_TitleLoading_00

        patch_blyt('hash_0x196a863d', 'N_CheckBG_00', 'scale_x', 1/s1) # bt_TitleLoading_00
        patch_blyt('hash_0x196a863d', 'N_CheckBG_00', 'scale_y', 1/s1) # bt_TitleLoading_00

        patch_blyt('hash_0x196a863d', 'P_Black_BG_00', 'scale_x', 1/s1) # bt_TitleLoading_00
        patch_blyt('hash_0x196a863d', 'P_Black_BG_00', 'scale_y', 1/s1) # bt_TitleLoading_00

        patch_blyt('hash_0x196a863d', 'P_BG_02', 'scale_x', 1/s1) # bt_TitleLoading_00
        patch_blyt('hash_0x196a863d', 'P_BG_02', 'scale_y', 1/s1) # bt_TitleLoading_00

        patch_blyt('hash_0xca612e43', 'L_Fade_00', 'scale_x', 1/s1) # rc_RaceView_Cmn_00

        patch_blyt('hash_0xb061c76e', 'L_Fade_00', 'scale_x', 1/s1) # rc_RaceView_1P_00
        patch_blyt('hash_0xa136fd7c', 'L_Fade_00', 'scale_x', 1/s1) # rc_RaceView_2P_MI
        patch_blyt('hash_0x639520ee', 'L_Fade_00', 'scale_x', 1/s1) # rc_RaceView_4P_MI


        patch_blyt('hash_0xfe743133', 'P_BG_00', 'scale_x', 1/s1) # rc_Pause_Cmn_00

        
        patch_blyt('hash_0xcc5d377a', 'P_BlueBG_00', 'scale_x', 1/s1) # mn_Background_00
        patch_blyt('hash_0xcc5d377a', 'P_Sparkle_00', 'scale_x', 1/s1) # mn_Background_00
        patch_blyt('hash_0xcc5d377a', 'P_Monogram_00', 'scale_x', 1/s1) # mn_Background_00

        patch_blyt('hash_0xcc5d377a', 'N_TitelePicAll_00', 'scale_x', 1/s1) # mn_Background_00
        patch_blyt('hash_0xcc5d377a', 'P_TiteleBGBack_00', 'scale_y', 1/s1) # mn_Background_00
        patch_blyt('hash_0xcc5d377a', 'P_TiteleBG_00', 'scale_y', 1/s1) # mn_Background_00
        patch_blyt('hash_0xcc5d377a', 'P_TiteleBG_01', 'scale_y', 1/s1) # mn_Background_00

        patch_blyt('hash_0x61e313d5', 'N_All_00', 'scale_x', 1/s1) # cm_LoadWin_00
        patch_blyt('hash_0x61e313d5', 'N_All_00', 'scale_y', 1/s1) # cm_LoadWin_00

        patch_blyt('hash_0x9a7a5a0e', 'N_Capture_00', 'scale_x', 1/s1) # mn_TitleScene_00
        patch_blyt('hash_0x9a7a5a0e', 'N_Capture_01', 'scale_x', 1/s1) # mn_TitleScene_00
        patch_blyt('hash_0x9a7a5a0e', 'N_Capture_00', 'scale_y', 1/s1) # mn_TitleScene_00
        patch_blyt('hash_0x9a7a5a0e', 'N_Capture_01', 'scale_y', 1/s1) # mn_TitleScene_00


        patch_blyt('hash_0x44e1a771', 'N_Capture_00', 'scale_x', 1/s1) # mn_ModeSlct_00
        patch_blyt('hash_0x44e1a771', 'N_Capture_00', 'scale_y', 1/s1) # mn_ModeSlct_00

        # cm_LoadScreen_00 not working
        # patch_blyt('hash_0xb291a57f', 'P_FadeBG_00', 'scale_x', 1/s1) # cm_LoadScreen_00
        # patch_blyt('hash_0xb291a57f', 'P_FadeBG_00', 'scale_y', 1/s1) # cm_LoadScreen_00

        # cm_Window_00 not working
        # patch_blyt('hash_0x46305bab', 'N_All_00', 'scale_x', 1/s1) # cm_Window_00
        # patch_blyt('hash_0x46305bab', 'N_All_01', 'scale_x', s1) # cm_Window_00

        # rc_Page_RaceResult not working
        # patch_blyt('hash_0x39dcd6cb', 'RootPane', 'scale_x', s1) # rc_Page_RaceResult

        patch_blyt('hash_0x4141b313', 'RootPane', 'scale_x', s1) # rc_Result_00



        if HUD_pos == 'corner':
            print("Shifitng elements for corner HUD")
            patch_ui_layouts("x")

            
    else:
        s1 = aspect_ratio / (16/9)
        s2 = 1-s1
        s3 = s2/s1
        ratio = aspect_ratio
        
        for name in file_names_stripped:
            if name in do_not_scale_rootpane:
                print(f"Skipping root pane scaling of {name}")
            if name not in do_not_scale_rootpane:
                print(f"Scaling root pane vertically for {name}")
                patch_blyt(name, 'RootPane', 'scale_y', s1)
            if name in rootpane_stretch_y:
                patch_blyt(name, 'RootPane', 'scale_y', 1/s1)
             
        patch_blyt('hash_0xb061c76e', 'N_All_00', 'scale_y', s1) # Player HUD 
        patch_blyt('hash_0xb061c76e', 'N_Pause_00', 'scale_y', s1) # Player HUD 
        patch_blyt('hash_0x4141b313', 'RootPane', 'scale_x', s1) #RC Result
        patch_blyt('hash_0x64f64f62', 'RootPane', 'scale_x', s1) #RC Result Team
        patch_blyt('hash_0x468a66a', 'RootPane', 'scale_x', s1) #RC Result TIme Trial
        patch_blyt('hash_0x9a7a5a0e', 'N_Capture_0', 'scale_x', 1/s1) # Title Screen Background
        patch_blyt('hash_0x5078a7b0', 'RootPane', 'scale_x', 1/s1) # Fade Pause
        patch_blyt('hash_0xc1e2251e', 'RootPane', 'scale_x', 1/s1) # Page Fade 
        patch_blyt('hash_0x79edb528', 'RootPane', 'scale_x', 1/s1) # Page Fade Pause

        if HUD_pos == 'corner':
            print("Shifitng elements for corner HUD")                
            patch_ui_layouts("y")