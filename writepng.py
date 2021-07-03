#!/usr/bin/env python3

import zlib


def main():
    signature = bytes((137, 80, 78, 71, 13, 10, 26, 10))

    print(f"\nsignature = {signature}\n")

    chunk_ihdr = make_chunk("IHDR", make_header(width=4, height=4))

    print(f"header = {chunk_ihdr}\n")

    red =   [   0,  85, 170, 255,     0,  85, 170, 255,     0,  85, 170, 255,     0,  85, 170, 255 ]
    green = [   0,   0,   0,   0,    85,  85,  85,  85,   170, 170, 170, 170,   255, 255, 255, 255 ]
    blue =  [ 255,   0,   0,   0,     0, 255,   0,   0,     0,   0, 255,   0,     0,   0,   0, 255 ]

    blob = pass_image(width=4, planes=[red, green, blue])
    data = zlib.compress(bytes(blob))
    chunk_idat = make_chunk("IDAT", data)

    print(f"data = {chunk_idat}\n")


def make_chunk(type, data=b""):
    b = len(data).to_bytes(4, byteorder="big")  # Length of Data
    b += bytes(type, "ascii")                   # Chunk Type
    b += data                                   # Data Field
    crc = zlib.crc32(bytes(type, "ascii"))
    crc = zlib.crc32(data, crc)
    b += crc.to_bytes(4, byteorder="big")       # CRC
    return b

def make_header(width, height):
    b = width.to_bytes(4, byteorder="big")    # Width
    b += height.to_bytes(4, byteorder="big")  # Height
    b += (8).to_bytes(1, byteorder="big")     # Bit Depth
    b += (2).to_bytes(1, byteorder="big")     # Color Type = Truecolor
    b += (0).to_bytes(1, byteorder="big")     # Compression Method
    b += (0).to_bytes(1, byteorder="big")     # Filter Method
    b += (0).to_bytes(1, byteorder="big")     # Interlace Method = None
    return b

def pass_image(width, planes):
    lines = int(len(planes[0]) / width)
    blob = []
    for i in range(0, lines):
        scanline = get_scanline(i, width, planes)
        filtered = filter_0(scanline)
        blob += filtered
    return blob

def get_scanline(line_number, width, planes):
    start = line_number * width
    scanline = []
    for i in range(start, start+width):
        for p in planes:
            scanline.append(p[i])
    return scanline

def filter_0(scanline):
    return [0] + scanline


if __name__ == "__main__":
    main()