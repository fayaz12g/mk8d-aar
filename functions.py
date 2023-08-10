import struct
import math
import os
import keystone
from keystone import *

def convert_asm_to_arm64_hex(asm_code):
    import binascii
    ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    encoding, _ = ks.asm(asm_code)
    return binascii.hexlify(bytearray(encoding)).decode('utf-8').upper()

def calculate_rounded_ratio(ratio_value):
    if ratio_value <= 2:
        rounded_ratio = round(ratio_value * 16) / 16
    elif ratio_value > 2 and ratio_value <= 4:
        rounded_ratio = round(ratio_value * 8) / 8
    else:
        rounded_ratio = round(ratio_value * 4) / 4
    return rounded_ratio

def generate_asm_code(rounded_ratio):
    asm_code = f"vmov.f32 s0, #{rounded_ratio}e+00"
    return asm_code

def float2hex(f):
    return hex(struct.unpack('>I', struct.pack('<f', f))[0]).lstrip('0x').rjust(8,'0').upper()

def patch_blyt(filename, pane, operation, value):
    print(f"Scaling {pane} by {value}")
    offset_dict = {'shift_x': 0x40, 'shift_y': 0x48, 'scale_x': 0x70, 'scale_y': 0x78} 
    full_path = filename
    with open(full_path, 'rb') as f:
        content = f.read().hex()
    start_rootpane = content.index(b'RootPane'.hex())
    pane_hex = str(pane).encode('utf-8').hex()
    start_pane = content.index(pane_hex, start_rootpane)
    idx = start_pane + offset_dict[operation]
    content_new = content[:idx] + float2hex(value) + content[idx+8:]
    with open(full_path, 'wb') as f:
        f.write(bytes.fromhex(content_new))

