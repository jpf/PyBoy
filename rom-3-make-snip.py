import sys
import png
import io
import zipfile

filename = sys.argv[1]
base_name = filename.split(".")[0]
screenshot_name = f"{base_name}.gb.png"
savestate_name = f"{base_name}.gb.state"
zeroedrom_name = f"{base_name}.0"

screenshot = png.Reader(screenshot_name)
chunks = list(screenshot.chunks())

zip_bytes = io.BytesIO()
with zipfile.ZipFile(zip_bytes, "w", compression=zipfile.ZIP_DEFLATED) as zip:
    zip.write(zeroedrom_name, arcname="rom")
    zip.write(savestate_name, arcname="state")
    zip.printdir()
zip_bytes.seek(0)

with open(f"{base_name}.snip.png", "wb") as dest:
    my_chunk = (b"snIp", zip_bytes.read())
    index = 1
    chunks.insert(index, my_chunk)
    png.write_chunks(dest, chunks)
