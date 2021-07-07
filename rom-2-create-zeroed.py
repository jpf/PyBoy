import sys
import os
import pickle

if __name__ == '__main__':
    filename = sys.argv[1]
    base_name = filename.split(".")[0]
    rom_size = os.stat(filename).st_size
    rom = open(filename, "rb")
    
    found = {}
    pickle_file = f"{filename}.pickle"
    with open(pickle_file, "rb") as input:
        found = pickle.load(input)

    # Copy cartridge header from original ROM to new ROM
    # The cartridge header is the bytes from 0x0100 to 0x014F
    for i in range(256, 335):
        rom.seek(i)
        found[i] = int.from_bytes(rom.read(1), byteorder='big')

    zeroed_rom = f"{base_name}.0"
    with open(zeroed_rom, "wb") as zeroed:
        for i in range(0, rom_size):
            if i in found:
                val = found[i]
            else:
                val = 0
            zeroed.write(val.to_bytes(1, byteorder='big'))

    print("Done")
