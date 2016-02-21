from panda3d.core import *

# Collision BitMasks
WallBitmask = BitMask32.bit(1)
FloorBitmask = BitMask32.bit(2)
DoorBitmask = BitMask32.bit(3)
GagBitmask = BitMask32.bit(4)
DropBitmask = BitMask32.bit(5)
ProjBitmask = BitMask32.bit(6)

LARGE_BEAN_AMT = 20
THROW_COLOR = VBase3(255 / 255.0, 145 / 255.0, 66 / 255.0)

# Sounds
clickSound = None
rlvrSound = None

def getClickSound():
    clickSound = loader.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.mp3')
    return clickSound

def getRlvrSound():
    rlvrSound = loader.loadSfx('phase_3/audio/sfx/GUI_rollover.mp3')
    return rlvrSound    

def getFont(name):
    return loader.loadFont("phase_3/models/fonts/%s" % (name))