import struct
import math
import os
import keystone
from keystone import *

def hex2float(h):
    return struct.unpack('<f', struct.pack('>I', int(h, 16)))[0]

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
    asm_code = f"vmov.f32 s2, #{rounded_ratio}e+00"
    return asm_code

def float2hex(f):
    return hex(struct.unpack('>I', struct.pack('<f', f))[0]).lstrip('0x').rjust(8,'0').upper()

