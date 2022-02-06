import sys
from pwn import *

SIGNATURE = bytearray(
    [102, 185, 255, 255, 235, 25, 94, 139,
     254, 131, 199, 0, 139, 215, 59, 242,
     125, 11, 176, 123, 242, 174, 255, 207,
     172, 40, 7, 235, 241, 235, 5, 232,
     226, 255, 255, 255]
)

if len(sys.argv) < 2:
    print(f"USAGE: {sys.argv[0]} [filename] ...")
    sys.exit()

print("Start file(s) processing...")

for filename in sys.argv[1:]:
    print(f"\nSearching signature in '{filename}'...")
    data = read(filename)
    offset = data.find(SIGNATURE)
    if offset == -1:
        print("Signature not found!")
        continue
    print(f"Signature found at offset 0x{offset}, size {len(SIGNATURE)}")
    shellcode = data[offset + len(SIGNATURE):]
    print(shellcode)
    print(hexdump(shellcode, hexii=True))
    print(disasm(shellcode))

print("\nDone")
