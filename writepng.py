#!/usr/bin/env python3

import zlib


def main():
    signature = bytes((137, 80, 78, 71, 13, 10, 26, 10))

    print(f"\nsignature = {signature}\n")


if __name__ == "__main__":
    main()