import os
import sys
import subprocess
import functions
import struct
import math

from functions import calculate_rounded_ratio, convert_asm_to_arm64_hex, float2hex

def create_patch_files(patch_folder, ratio_value, scaling_factor, visual_fixes):
    visual_fixesa = visual_fixes[0]
    visual_fixesb = visual_fixes[1]
    scaling_factor = float(scaling_factor)
    ratio_value = float(ratio_value)
    print(f"The scaling factor is {scaling_factor}.")
    rounded_ratio = functions.calculate_rounded_ratio(float(ratio_value))
    asm_code = functions.generate_asm_code(rounded_ratio)
    hex_value = functions.convert_asm_to_arm64_hex(asm_code)
    version_variables = ["3.0.1", "3.0.3"]
    for version_variable in version_variables:
        file_name = f"main-{version_variable}.pchtxt"
        file_path = os.path.join(patch_folder, file_name)

        if version_variable == "3.0.1":
            nsobidid = "9EF5CAA2D5B933C772358C5AA6FABA15"
            visual_fix = visual_fixesa

        if version_variable == "3.0.3":
            nsobidid = "6A85262F21B903649BD7C62628D26E43"
            visual_fix = visual_fixesb
            

        patch_content = f'''@nsobid-{nsobidid}

@flag print_values
@flag offset_shift 0x100

@enabled
003FA89C E87A0FEA
007D9444 040A85EE
007D9448 {hex_value}
007D944C 010A20EE
007D9450 1285F0EA
@disabled

{visual_fix}

// Generated using MK8D-AAR by Fayaz (github.com/fayaz12g/mk8d-aar)'''
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as patch_file:
            patch_file.write(patch_content)
        print(f"Patch file created: {file_path}")
