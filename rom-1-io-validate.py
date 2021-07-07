import sys
import pickle

class GreenBytes:
    def __init__(self):
        self.found = {}

    def add(self, line):
        (_, rw, addr, val) = line.split(",")
        if rw == "r" and addr not in self.found:
            self.found[int(addr)] = int(val)

    def report(self):
        addrs = sorted(list(self.found.keys()))
        for addr in addrs:
            print(addr)

    def sorted(self):
        return sorted(list(self.found.keys()))

if __name__ == '__main__':
    filename = sys.argv[1]
    rom = open(filename, "rb")
    g = GreenBytes()

    with open(f"{filename}.io.csv", "r") as io_log:
        for line in io_log.readlines():
            g.add(line.strip())

    for addr in g.sorted():
        val = g.found[addr]
        rom.seek(addr)
        inrom = int.from_bytes(rom.read(1), byteorder='big')
        as_hex = hex(addr)
        status = "OK"
        if val != inrom:
            status = "ERROR"
        print(f"{addr:<10} {as_hex:<10} {hex(val):<4} {hex(inrom):<4} {status}")
        if status == "ERROR":
            sys.exit(1)

    pickle_file = f"{filename}.pickle"
    print(f"Pickling GreenBytes().found to {pickle_file}")
    with open(pickle_file, "wb") as output:
        pickle.dump(g.found, output)
