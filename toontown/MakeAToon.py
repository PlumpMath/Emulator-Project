from SocketServer import *
from socket import *
import SocketServer
import commands
import compileall
import ConfigParser
from toontown import AnimationGlobals
from toontown import LocalAvatar
import Cookie
import socket
from subprocess import call
import BaseHTTPServer
import audiodev
import SimpleHTTPServer
import ctypes
from sys import argv
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

notify = DirectNotifyGlobal.directNotify.newCategory("Starting Make A Toon.")

base.win.requestProperties( wp )
base.setAspectRatio(1.3333333334)
base.camera.hide()
base.camera.setPos(-0.30, -11, 3)
base.camera.setHpr(-3, 0, 0)
transition = Transitions(loader)
transition.irisIn(1)
transition.fadeIn(5)


localAvatar = LocalAvatar.toonBody
base.localAvatar = localAvatar

Music = loader.loadMusic('phase_3/audio/bgm/create_a_toon.mid')
Music.setLoop(1)
MusicVolume = (0.4)
Music.play()
Music.setVolume(MusicVolume)
base.localAvatar.setPos(0.80, 2, 0)
base.localAvatar.setHpr(176, 0, 0)
LocalAvatar.setMovementAnimation('neutral')
room = loader.loadModel('phase_3/models/gui/create_a_toon.bam')
room.reparentTo(render)
room.find('**/sewing_machine').removeNode()
room.find('**/drafting_table').removeNode()
room.find("**/wall_floor").setColor(0.7294117647058824, 0.5490196078431373, 0.2392156862745098, 1)
room.setName("Room")
ee = DirectFrame(pos=(-1, 1, 1), frameSize=(-.01, 0.01, -.01, 0.01), frameColor=(0, 0, 0, 0.05), state='normal')
ee.bind(DGG.B1PRESS, lambda x, ee = ee: self.toggleSlide())
eee = ee
gui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui.bam')
gui.flattenMedium()
toonSpin = localAvatar.hprInterval(2, Vec3(540, 0, 0))
toonSpin2 = localAvatar.hprInterval(2, Vec3(180, 0, 0))
MakeAToonText = 'Make a Toon to Play!'
Mickey = 'Mickey.TTF'

CameraMove = camera.posInterval(1,
                                  Point3(-0.50, -11, 3),
                                  startPos=Point3(1, -11, 3))

CameraMoveSequence = Sequence(CameraMove)

def goRight():
    LocalAvatar.bodyNodes[0].setColor(1, 1, 1, 1)
    LocalAvatar.bodyNodes[1].setColor(0.91, 0.1274, 0.1274, 1)
    LocalAvatar.bodyNodes[2].setColor(0.91, 0.1274, 0.1274, 1)
    LocalAvatar.bodyNodes[3].setColor(0.91, 0.1274, 0.1274, 1)
    LocalAvatar.bodyNodes[4].setColor(0.91, 0.1274, 0.1274, 1)
    LocalAvatar.bodyNodes[5].setColor(1, 1, 1, 1)
    LocalAvatar.bodyNodes[6].setColor(0.91, 0.1274, 0.1274, 1)
    LocalAvatar.bodyNodes[7].setColor(0.91, 0.1274, 0.1274, 1)
    LocalAvatar.bodyNodes[8].setColor(0.91, 0.1274, 0.1274, 1)
    LocalAvatar.bodyNodes[9].setColor(0.91, 0.1274, 0.1274, 1)

def goBack():
    LocalAvatar.bodyNodes[0].setColor(1, 1, 1, 1)
    LocalAvatar.bodyNodes[1].setColor(0.7286, 0.5612, 0.92, 1)
    LocalAvatar.bodyNodes[2].setColor(0.7286, 0.5612, 0.92, 1)
    LocalAvatar.bodyNodes[3].setColor(0.7286, 0.5612, 0.92, 1)
    LocalAvatar.bodyNodes[4].setColor(0.7286, 0.5612, 0.92, 1)
    LocalAvatar.bodyNodes[5].setColor(1, 1, 1, 1)
    LocalAvatar.bodyNodes[6].setColor(0.7286, 0.5612, 0.92, 1)
    LocalAvatar.bodyNodes[7].setColor(0.7286, 0.5612, 0.92, 1)
    LocalAvatar.bodyNodes[8].setColor(0.7286, 0.5612, 0.92, 1)
    LocalAvatar.bodyNodes[9].setColor(0.7286, 0.5612, 0.92, 1)

def HprToon():
    toonSpin.start()

def HprToon2():
    toonSpin2.start()

mickeyFont = loader.loadFont('phase_3/models/fonts/MickeyFont.bam')
Text = OnscreenText(text = "Make A Toon", pos = (0, 0.75), font = mickeyFont, fg = (1, 0, 0, 1),
                scale=(0.2, 0.2, 0.2)),
gui1 = loader.loadModel('phase_3/models/gui/create_a_toon_gui.bam')
gui2 = loader.loadModel('phase_3/models/gui/gui_toongen.bam')
guiNextUp = gui.find('**/tt_t_gui_mat_nextUp')
oobeButton = DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom = (gui1.find("**/CrtATn_R_Arrow_UP"), gui1.find("**/CrtATn_R_Arrow_DN"), gui1.find("**/CrtATn_R_Arrow_RLVR")), relief=None, hpr=(0, 0, 180), command=goRight)
oobeButton.setScale(1)
oobeButton.setPos(-0.70,3,-0.25)
goBackButton = DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom = (gui1.find("**/CrtATn_R_Arrow_UP"), gui1.find("**/CrtATn_R_Arrow_DN"), gui1.find("**/CrtATn_R_Arrow_RLVR")), relief=None, command=goBack)
goBackButton.setScale(1)
goBackButton.setPos(0.80,3,-0.25)
spinButton = DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom = (gui1.find("**/CrtATn_R_Arrow_UP"), gui1.find("**/CrtATn_R_Arrow_DN"), gui1.find("**/CrtATn_R_Arrow_RLVR")), relief=None, command=HprToon)
spinButton.setScale(0.60)
spinButton.setPos(0.50,2,-0.50)
spinButton2 = DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom = (gui1.find("**/CrtATn_R_Arrow_UP"), gui1.find("**/CrtATn_R_Arrow_DN"), gui1.find("**/CrtATn_R_Arrow_RLVR")), relief=None, hpr=(0, 0, 180), command=HprToon2)
spinButton2.setScale(0.60)
spinButton2.setPos(-0.40,2,-0.50)

def CameraButton():
    transition.irisIn()
    transition.fadeOut(1)
    Music.stop()


OK = DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom=(gui2.find("**/tt_t_gui_mat_okUp"), gui2.find("**/tt_t_gui_mat_okDown")), pos=(0.90,1,-0.80), relief=None, command=CameraButton)

ToonEnter = localAvatar.posInterval(1,
                                  Point3(0.60, 2, 0),
                                  startPos=Point3(-4, 2, 0))

ToonEnterPace = Sequence(ToonEnter)
ToonEnter.start()


run()
