import sys
import os.path
from pyboy import PyBoy
from pyboy.utils import WindowEvent

filename = sys.argv[1]
base_name = filename.split(".")[0]
save_state = filename + ".state"

pyboy = PyBoy(filename, sound=False)
if os.path.isfile(save_state):
    state_file = open(save_state, "rb")
    pyboy.load_state(state_file)
while not pyboy.tick():
    inputs = pyboy.get_input()
    for event in inputs:
        if event == WindowEvent.STATE_SAVE:
            pil_image = pyboy.screen_image()
            pil_image.save(f"{filename}.png")
