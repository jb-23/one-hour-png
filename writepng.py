#!/usr/bin/env python3

import zlib


def main():
    signature = bytes((137, 80, 78, 71, 13, 10, 26, 10))

    print(f"\nsignature = {signature}\n")

    chunk_ihdr = make_chunk("IHDR", make_header(width=4, height=4))

    print(f"header = {chunk_ihdr}\n")


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


if __name__ == "__main__":
    main()