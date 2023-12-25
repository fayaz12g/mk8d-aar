
import os
import sys
import time
import SarcLib
import struct
import libyaz0

def extract_sarc(file):
    with open(file, "rb") as inf:
        inb = inf.read()

    while libyaz0.IsYazCompressed(inb):
        inb = libyaz0.decompress(inb)

    name = os.path.splitext(file)[0]
    ext = SarcLib.guessFileExt(inb)
    
    # if ext == ".szs":
    #     inb = DecompressYaz(inb)

    if ext != ".sarc":
        with open(''.join([name, ext]), "wb") as out:
            out.write(inb)

    else:
        arc = SarcLib.SARC_Archive()
        arc.load(inb)

        root = os.path.join(os.path.dirname(file), name)
        if not os.path.isdir(root):
            os.mkdir(root)

        files = []

        def getAbsPath(folder, path):
            nonlocal root
            nonlocal files

            for checkObj in folder.contents:
                if isinstance(checkObj, SarcLib.File):
                    files.append(["/".join([path, checkObj.name]), checkObj.data])

                else:
                    path_ = os.path.join(root, "/".join([path, checkObj.name]))
                    if not os.path.isdir(path_):
                        os.mkdir(path_)

                    getAbsPath(checkObj, "/".join([path, checkObj.name]))

        for checkObj in arc.contents:
            if isinstance(checkObj, SarcLib.File):
                files.append([checkObj.name, checkObj.data])

            else:
                path = os.path.join(root, checkObj.name)
                if not os.path.isdir(path):
                    os.mkdir(path)

                getAbsPath(checkObj, checkObj.name)

        for file, fileData in files:
            print(file)
            with open(os.path.join(root, file), "wb") as out:
                out.write(fileData)
                
def extract_szs(file):
    with open(file, "rb") as inf:
        inb = inf.read()

    inb = libyaz0.decompress(inb)

    name = os.path.splitext(file)[0]
    ext = SarcLib.guessFileExt(inb)
    
    inb = DecompressYaz(inb)

    # if ext != ".sarc":
    #     with open(''.join([name, ext]), "wb") as out:
    #         out.write(inb)

    arc = SarcLib.SARC_Archive()
    arc.load(inb)

    root = os.path.join(os.path.dirname(file), name)
    if not os.path.isdir(root):
        os.mkdir(root)

    files = []

    def getAbsPath(folder, path):
        nonlocal root
        nonlocal files

        for checkObj in folder.contents:
            if isinstance(checkObj, SarcLib.File):
                files.append(["/".join([path, checkObj.name]), checkObj.data])

            else:
                path_ = os.path.join(root, "/".join([path, checkObj.name]))
                if not os.path.isdir(path_):
                    os.mkdir(path_)

                getAbsPath(checkObj, "/".join([path, checkObj.name]))

    for checkObj in arc.contents:
        if isinstance(checkObj, SarcLib.File):
            files.append([checkObj.name, checkObj.data])

        else:
            path = os.path.join(root, checkObj.name)
            if not os.path.isdir(path):
                os.mkdir(path)

            getAbsPath(checkObj, checkObj.name)

    for file, fileData in files:
        print(file)
        with open(os.path.join(root, file), "wb") as out:
            out.write(fileData)

def DecompressYaz(src):
    src_end = len(src)

    dest_end = struct.unpack(">I", src[4:8])[0]
    dest = bytearray(dest_end)

    code = src[16]

    src_pos = 17
    dest_pos = 0

    while src_pos < src_end and dest_pos < dest_end:
        for _ in range(8):
            if src_pos >= src_end or dest_pos >= dest_end:
                break

            if code & 0x80:
                dest[dest_pos] = src[src_pos]; dest_pos += 1; src_pos += 1

            else:
                b1 = src[src_pos]; src_pos += 1
                b2 = src[src_pos]; src_pos += 1

                copy_src = dest_pos - ((b1 & 0x0f) << 8 | b2) - 1

                n = b1 >> 4
                if not n:
                    n = src[src_pos] + 0x12; src_pos += 1

                else:
                    n += 2

                for _ in range(n):
                    dest[dest_pos] = dest[copy_src]; dest_pos += 1; copy_src += 1

            code <<= 1

        else:
            if src_pos >= src_end or dest_pos >= dest_end:
                break

            code = src[src_pos]; src_pos += 1

    return bytes(dest)

