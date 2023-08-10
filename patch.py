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
    version_variables = ["1.0.0", "2.4.0"]
    for version_variable in version_variables:
        file_name = f"main-{version_variable}.pchtxt"
        file_path = os.path.join(patch_folder, file_name)

        if version_variable == "1.0.0":
            nsobidid = "FE1B230800D4933C617C691273CA5978"
            replacement_value = "009CF340"
            visual_fix = visual_fixesa

        elif version_variable == "2.4.0":
            nsobidid = "4B7A0BB5AE57E627B63E2247F9470E57"
            replacement_value = "003cfb98"
            visual_fix = visual_fixesb

        patch_content = f'''@nsobid-{nsobidid}

@flag print_values
@flag offset_shift 0x100

@enabled
{replacement_value} {hex_value}
@stop

{visual_fix}

// Generated using MK8D-AAR by Fayaz (github.com/fayaz12g/mk8d-aar)'''
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as patch_file:
            patch_file.write(patch_content)
        print(f"Patch file created: {file_path}")
