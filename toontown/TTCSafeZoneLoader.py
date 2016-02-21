from pandac.PandaModules import *
import random 
import TTCPlayground

class TTCSafeZoneLoader:

    def __init__(self, doneEvent):
    	SafeZoneLoader.SafeZoneLoader.__init__(self, doneEvent)
        self.music = 'phase_1audio/bgm/TC_nbrhood.mid'
        self.Model = 'phase_1/models/toontown_central_full.bam'

    def load(self):
        self.birdSound = map(base.loadSfx, ['phase_1/audio/sfx/SZ_TC_bird1.mp3', 'phase_1/audio/sfx/SZ_TC_bird2.mp3', 'phase_1/audio/sfx/SZ_TC_bird3.mp3'])
        loader.loadModel(self.Model)

    def unload(self):
      	del self.birdSound
      	del self.Model
