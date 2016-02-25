from toontown import AnimationGlobals
from toontown import LocalAvatar
from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from direct.directbase import DirectStart
from direct.task import Task
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase.Transitions import Transitions
from direct.interval.IntervalGlobal import *
from direct.showbase.InputStateGlobal import inputState
from direct.controls.GravityWalker import GravityWalker
from direct.distributed.DistributedObject import DistributedObject
from pandac.PandaModules import NodePath, TextNode, Vec4
from direct.gui.DirectGui import DirectWaitBar, DirectLabel
from direct.interval.IntervalGlobal import LerpColorScaleInterval, Sequence, Func
from direct.directnotify import DirectNotifyGlobal
import atexit
import sys
import Globals
import time
import os
import tempfile
import LocalizerEnglish as Localizer
from random import randint
from panda3d.core import WindowProperties

print 'Gathering Data...'
#time.sleep(0.1)
print 'Loading Toontown...'
print 'DirectStart: Starting Make A Toon.'
base.disableMouse()
wp = WindowProperties()
tempdir = tempfile.mkdtemp()
wp.setTitle('Toontown Emulator')
wp.setCursorFilename('toonmono.cur')
wp.setIconFilename('icon.ico')
base.win.requestProperties( wp )
base.setAspectRatio(1.3333333334)
base.camera.hide()
base.camera.setPos(-0.30, -11, 3)
base.camera.setHpr(-3, 0, 0)

class MakeAToon:
    
    def __init__(self):
        self.notify = DirectNotifyGlobal.directNotify.newCategory("Starting Make A Toon.")
        self.localAvatar = LocalAvatar.toonBody
        base.localAvatar = self.localAvatar
        self.toonColors = Localizer.toonColorDict
        self.colorNum = randint(0, Localizer.numColors)
        self.numColors = Localizer.numColors
        self.goRight()
        self.MakeAToonText = Localizer.MakeAToonText
        self.Mickey = Localizer.Mickey
        self.mickeyFont = loader.loadFont('phase_3/models/fonts/MickeyFont.bam')
        self.Text = OnscreenText(text = "Make A Toon", pos = (0, 0.75), font = self.mickeyFont, fg = (1, 0, 0, 1),scale=(0.2, 0.2, 0.2))
        self.gui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui.bam')
        self.gui.flattenMedium()
        self.gui1 = loader.loadModel('phase_3/models/gui/create_a_toon_gui.bam')
        self.gui2 = loader.loadModel('phase_3/models/gui/gui_toongen.bam')
        self.guiNextUp = self.gui.find('**/tt_t_gui_mat_nextUp')
        self.transition = Transitions(loader)
        self.transition.irisIn(1)
        self.transition.fadeIn(5)
        self.load()

    def load(self):
        self.Music = loader.loadMusic('phase_3/audio/bgm/create_a_toon.mid')
        self.Music.setLoop(1)
        self.MusicVolume = (0.4)
        self.Music.play()
        self.Music.setVolume(self.MusicVolume)
        base.localAvatar.setPos(0.80, 2, 0)
        base.localAvatar.setHpr(176, 0, 0)
        LocalAvatar.setMovementAnimation('neutral')
        self.room = loader.loadModel('phase_3/models/gui/create_a_toon.bam')
        self.room.reparentTo(render)
        self.room.find('**/sewing_machine').removeNode()
        self.room.find('**/drafting_table').removeNode()
        self.room.find("**/wall_floor").setColor(0.7294117647058824, 0.5490196078431373, 0.2392156862745098, 1)
        self.room.setName("Room")
        self.ee = DirectFrame(pos=(-1, 1, 1), frameSize=(-.01, 0.01, -.01, 0.01), frameColor=(0, 0, 0, 0.05), state='normal')
        self.ee.bind(DGG.B1PRESS, lambda x, ee = self.ee: self.toggleSlide())
        self.eee = self.ee
        self.toonSpin = base.localAvatar.hprInterval(2, Vec3(540, 0, 0))
        self.toonSpin2 = base.localAvatar.hprInterval(2, Vec3(180, 0, 0))
        self.CameraMove = camera.posInterval(1,
                                  Point3(-0.50, -11, 3),
                                  startPos=Point3(1, -11, 3))
        self.CameraMoveSequence = Sequence(self.CameraMove)
        self.ToonEnter = base.localAvatar.posInterval(1,
                                  Point3(0.60, 2, 0),
                                  startPos=Point3(-4, 2, 0))
        self.ToonEnterPace = Sequence(self.ToonEnter)
        self.ToonEnter.start()
        self.goLeftButton = DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom = (self.gui1.find("**/CrtATn_R_Arrow_UP"), self.gui1.find("**/CrtATn_R_Arrow_DN"), self.gui1.find("**/CrtATn_R_Arrow_RLVR")), relief=None, hpr=(0, 0, 180), command=self.goRight)
        self.goLeftButton.setScale(1)
        self.goLeftButton.setPos(-0.70,3,-0.25)
        self.goLeftButton.hide()
        self.goRightButton = DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom = (self.gui1.find("**/CrtATn_R_Arrow_UP"), self.gui1.find("**/CrtATn_R_Arrow_DN"), self.gui1.find("**/CrtATn_R_Arrow_RLVR")), relief=None, command=self.goRight)
        self.goRightButton.setScale(1)
        self.goRightButton.setPos(0.80,3,-0.25)
        self.goRightButton.hide()
        self.spinButton = DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom = (self.gui1.find("**/CrtATn_R_Arrow_UP"), self.gui1.find("**/CrtATn_R_Arrow_DN"), self.gui1.find("**/CrtATn_R_Arrow_RLVR")), relief=None, command=self.HprToon)
        self.spinButton.setScale(0.60)
        self.spinButton.setPos(0.50,2,-0.50)
        self.spinButton2 = DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom = (self.gui1.find("**/CrtATn_R_Arrow_UP"), self.gui1.find("**/CrtATn_R_Arrow_DN"), self.gui1.find("**/CrtATn_R_Arrow_RLVR")), relief=None, hpr=(0, 0, 180), command=self.HprToon2)
        self.spinButton2.setScale(0.60)
        self.spinButton2.setPos(-0.40,2,-0.50)
        #self.OK = DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom=(self.gui2.find("**/tt_t_gui_mat_okUp"), self.gui2.find("**/tt_t_gui_mat_okDown")), pos=(1.10,1,-0.80), relief=None, command=self.goForward1)
        self.Next = DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom=(self.gui2.find("**/tt_t_gui_mat_nextUp"), self.gui2.find("**/tt_t_gui_mat_nextDown")), pos=(1.10,1,-0.80), scale=(0.58, 0.58, 0.58), relief=None, command=self.goForward1)
        self.goBackButton1 = DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom=(self.gui2.find("**/tt_t_gui_mat_nextUp"), self.gui2.find("**/tt_t_gui_mat_nextDown")), pos=(-1,1,-0.80), scale=(0.58, 0.58, 0.58), hpr=(0, 0, 180), relief=None, command=self.goBack1)
        self.goBackButton1.hide()
        self.Cancel = DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom=(self.gui2.find("**/tt_t_gui_mat_closeUp"), self.gui2.find("**/tt_t_gui_mat_closeDown")), pos=(-1,1,-0.80), scale=(1, 1, 1), hpr=(0, 0, 180), relief=None, command=self.Cancel)

    def goRight(self):
        for color in self.toonColors[self.colorNum]:
            LocalAvatar.bodyNodes[color].setColor(self.toonColors[self.colorNum][color])
        self.colorNum += 1
        if self.colorNum > self.numColors:
            self.colorNum = 0

    def goLeft(self):
        for color in self.toonColors[self.colorNum]:
            LocalAvatar.bodyNodes[color].setColor(self.toonColors[self.colorNum][color])
        self.colorNum -= 1
        if self.colorNum < 0:
            self.colorNum = self.numColors

    def goBack1(self):
        self.goLeftButton.hide()
        self.goRightButton.hide()
        self.goBackButton1.hide()
        self.Cancel.show()

    def Cancel(self):
        self.transition.irisOut()
        self.Cancel.hide()
        self.Music.stop()
    
    def HprToon(self):
        self.toonSpin.start()

    def HprToon2(self):
        self.toonSpin2.start()

    def goForward1(self):
        self.goRightButton.show()
        self.goLeftButton.show()
        self.goBackButton1.show()
        self.Cancel.hide()


    '''def CameraButton(self):
        self.transition.irisIn()
        self.transition.fadeOut(1)
        self.Music.stop()'''

MakeAToon = MakeAToon()
run()