from SocketServer import *
from socket import *
import SocketServer
import commands
import compileall
import ConfigParser
from toontown import AnimationGlobals
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
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from direct.directbase import DirectStart
from direct.task import Task
from direct.actor.Actor import Actor
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase.InputStateGlobal import inputState
from direct.controls.GravityWalker import GravityWalker
from direct.distributed.DistributedObject import DistributedObject
from pandac.PandaModules import NodePath, TextNode, Vec4
from direct.gui.DirectGui import DirectWaitBar, DirectLabel
from direct.interval.IntervalGlobal import LerpColorScaleInterval, Sequence, Func
import atexit
import sys
from panda3d.core import WindowProperties
toonHead = loader.loadModel('phase_3/models/char/cat-heads-1000.bam')
otherParts = toonHead.findAllMatches('**/*long*')

for partNum in range(0, otherParts.getNumPaths()):
    otherParts.getPath(partNum).removeNode()

ntrlMuzzle = toonHead.find('**/*muzzle*neutral')
otherParts = toonHead.findAllMatches('**/*muzzle*')
for partNum in range(0, otherParts.getNumPaths()):
    part = otherParts.getPath(partNum)
    if part != ntrlMuzzle:
        otherParts.getPath(partNum).removeNode()

toonTorso = loader.loadModel('phase_3/models/char/tt_a_chr_dgl_shorts_torso_1000.bam')
toonLegs = loader.loadModel('phase_3/models/char/tt_a_chr_dgs_shorts_legs_1000.bam')
otherParts = toonLegs.findAllMatches('**/boots*') + toonLegs.findAllMatches('**/shoes')
for partNum in range(0, otherParts.getNumPaths()):
    otherParts.getPath(partNum).removeNode()

toonBody = Actor({'head': toonHead,
 'torso': toonTorso,
 'legs': toonLegs}, {'torso': AnimationGlobals.torsoAnimDict,
 'legs': AnimationGlobals.legsAnimDict})
toonBody.attach('head', 'torso', 'def_head')
toonBody.attach('torso', 'legs', 'joint_hips')
gloves = toonBody.findAllMatches('**/hands')
ears = toonBody.findAllMatches('**/*ears*')
head = toonBody.findAllMatches('**/head-*')
sleeves = toonBody.findAllMatches('**/sleeves')
shirt = toonBody.findAllMatches('**/torso-top')
shorts = toonBody.findAllMatches('**/torso-bot')
neck = toonBody.findAllMatches('**/neck')
arms = toonBody.findAllMatches('**/arms')
legs = toonBody.findAllMatches('**/legs')
feet = toonBody.findAllMatches('**/feet')
bodyNodes = []
bodyNodes += [gloves]
bodyNodes += [head, ears]
bodyNodes += [sleeves, shirt, shorts]
bodyNodes += [neck,
 arms,
 legs,
 feet]
bodyNodes[0].setColor(1, 1, 1, 1)
bodyNodes[1].setColor(0.264, 0.308, 0.676, 1)
bodyNodes[2].setColor(0.264, 0.308, 0.676, 1)
bodyNodes[3].setColor(0.264, 0.308, 0.676, 1)
bodyNodes[4].setColor(0.264, 0.308, 0.676, 1)
bodyNodes[5].setColor(1, 1, 1, 1)
bodyNodes[6].setColor(0.264, 0.308, 0.676, 1)
bodyNodes[7].setColor(0.264, 0.308, 0.676, 1)
bodyNodes[8].setColor(0.264, 0.308, 0.676, 1)
bodyNodes[9].setColor(0.264, 0.308, 0.676, 1)
topTex = loader.loadTexture('phase_4/maps/tt_t_chr_avt_shirt_sellbotCrusher.jpg')
botTex = loader.loadTexture('phase_4/maps/tt_t_chr_avt_shirtSleeve_sellbotCrusher.jpg')
sleeveTex = loader.loadTexture('phase_4/maps/tt_t_chr_avt_shirtSleeve_sellbotCrusher.jpg')
shoes = loader.loadTexture('phase_4/maps/tt_t_chr_avt_acc_sho_athleticBlack.jpg')
bodyNodes[3].setTexture(sleeveTex, 1)
bodyNodes[4].setTexture(topTex, 1)
bodyNodes[5].setTexture(botTex, 1)
toonBody.reparentTo(render)
geom = toonBody.getGeomNode()
geom.getChild(0).setSx(0.730000019073)
geom.getChild(0).setSz(0.730000019073)
offset = 3.2375
wallBitmask = BitMask32(1)
floorBitmask = BitMask32(2)
base.cTrav = CollisionTraverser()
footStepSound = loader.loadSfx('phase_3.5/audio/sfx/AV_footstep_runloop.wav')


def setMovementAnimation(loopName, playRate = 1.0):
    global movingRotation
    global movingBackward
    global movingForward
    global movingNeutral
    global movingJumping
    if 'jump' in loopName:
        movingJumping = True
        movingForward = False
        movingNeutral = False
        movingRotation = False
        movingBackward = False
    elif loopName == 'run':
        footStepSound.setLoop(1)
        movingJumping = False
        movingForward = True
        movingNeutral = False
        movingRotation = False
        movingBackward = False
    elif loopName == 'walk':
        movingJumping = False
        movingForward = False
        movingNeutral = False
        if playRate == -1.0:
            movingBackward = True
            movingRotation = False
        else:
            movingBackward = False
            movingRotation = True
    elif loopName == 'neutral':
        movingJumping = False
        movingForward = False
        movingNeutral = True
        movingRotation = False
        movingBackward = False
    else:
        movingJumping = False
        movingForward = False
        movingNeutral = False
        movingRotation = False
        movingBackward = False
    ActorInterval(toonBody, loopName, playRate=playRate).loop()