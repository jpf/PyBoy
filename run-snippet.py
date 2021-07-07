from pyboy import PyBoy
import io
import png
import sys
import tempfile
import zipfile

filename = sys.argv[1]

with open(filename, "rb") as data:
    for tag, chunk in png.Reader(bytes=data.read()).chunks():
        if tag != b"snIp":
            continue
        with zipfile.ZipFile(io.BytesIO(chunk)) as zip:
            files = zip.namelist()
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"Created {temp_dir}")
                if "rom" not in files:
                    print("ROM not found in snippet")
                    sys.exit(1)
                zip.extract("rom", temp_dir)
                emu = PyBoy(f"{temp_dir}/rom", sound=False)
                if "state" in files:
                    state = zip.open("state")
                    emu.load_state(state)
                while not emu.tick():
                    pass
