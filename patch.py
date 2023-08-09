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
    hex_value = functions.convert_asm_to_arm64_hex(ratio_value)
    version_variables = ["1.0.0", "1.3.0"]
    for version_variable in version_variables:
        file_name = f"main-{version_variable}.pchtxt"
        file_path = os.path.join(patch_folder, file_name)

        if version_variable == "1.0.0":
            nsobidid = "3CA12DFAAF9C82DA064D1698DF79CDA100000000"
            replacement_value = "009CF340"
            visual_fix = visual_fixesa

        elif version_variable == "1.3.0":
            nsobidid = "B424BE150A8E7D78701CBE7A439D9EBF"
            replacement_value = "0074D2EC"
            visual_fix = visual_fixesb

        patch_content = f'''@nsobid-{nsobidid}

@flag print_values
@flag offset_shift 0x100
@enabled
{replacement_value} {hex_value}
@stop

{visual_fix}

// Generated using SMO-AAR by Fayaz (github.com/fayaz12g/smo-aar)'''
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as patch_file:
            patch_file.write(patch_content)
        print(f"Patch file created: {file_path}")
