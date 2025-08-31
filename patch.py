import os
import sys
import subprocess
import functions
import struct
import math

from functions import *

def create_patch_files(patch_folder, ratio_value, scaling_factor, visual_fixes):
    scaling_factor = float(scaling_factor)
    ratio_value = float(ratio_value)
    print(f"The scaling factor is {scaling_factor}.")
    rounded_ratio = functions.calculate_rounded_ratio(float(ratio_value))
    asm_code = functions.generate_asm_code(rounded_ratio)
    hex_value = functions.convert_asm_to_arm64_hex(asm_code)
    version_variables = ["3.0.1", "3.0.3", "3.0.4", "3.0.5"]
    for version_variable in version_variables:
        file_name = f"main-{version_variable}.pchtxt"
        file_path = os.path.join(patch_folder, file_name)

        if version_variable == "3.0.1":
            nsobidid = "9EF5CAA2D5B933C772358C5AA6FABA15"
            visual_fix = visual_fixes[0]

        elif version_variable == "3.0.3":
            nsobidid = "6A85262F21B903649BD7C62628D26E43"
            visual_fix = visual_fixes[1]
            
        elif version_variable == "3.0.4":
            nsobidid = "2452C49BC26EC15904C507A34B6F16AE"
            visual_fix = visual_fixes[2]

        if version_variable == "3.0.5":
            nsobidid = "FE941ED5BA14BE5D505698DA1BBF4FE7"
            visual_fix = visual_fixes[3]
            
            # Step 1: float -> hex string
            hex_str = float_to_hex(scaling_factor)
            print(f"Float {scaling_factor} -> hex {hex_str}")

            # Step 2: split into two halves
            first_half = hex_str[:4]  
            second_half = hex_str[4:] 
            print(f"First half: {first_half}, Second half: {second_half}")

            # Step 3: convert halves into ARM assembly
            # (example: MOVW/MOVT for lower/upper 16 bits)
            asm_first = f"MOVZ W0, #0x{second_half}"
            asm_second = f"MOVK W0, #0x{first_half}, LSL #16"

            # Step 4: assemble to ARM64 hex
            hex_first = convert_asm_to_arm64_hex_new(asm_first)
            hex_second = convert_asm_to_arm64_hex_new(asm_second)

            patches = f'''003cb1ac {hex_first}
003cb1b0 {hex_second}
003cb1b4 C003271E'''
            
        else:
            patches = f'''003FA89C E87A0FEA
007D9444 040A85EE
007D9448 {hex_value}
007D944C 010A20EE
007D9450 1285F0EA'''

        patch_content = f'''@nsobid-{nsobidid}

@flag print_values
@flag offset_shift 0x100

@enabled
{patches}
@disabled

{visual_fix}

// Generated using MK8D-AAR by Fayaz (github.com/fayaz12g/mk8d-aar)'''
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as patch_file:
            patch_file.write(patch_content)
        print(f"Patch file created: {file_path}")
