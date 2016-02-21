from SocketServer import *
from socket import *
import SocketServer
import commands
import compileall
import ConfigParser
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
from direct.actor.Actor import Actor
from direct.directbase import DirectStart
from direct.task import Task
from direct.actor.Actor import Actor
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase.InputStateGlobal import inputState
from direct.controls.GravityWalker import GravityWalker
from direct.actor.Actor import Actor
from direct.distributed.DistributedObject import DistributedObject
from pandac.PandaModules import NodePath, TextNode, Vec4
from direct.gui.DirectGui import DirectWaitBar, DirectLabel
from direct.interval.IntervalGlobal import LerpColorScaleInterval, Sequence, Func
import atexit
import sys
from direct.actor.Actor import Actor
from panda3d.core import WindowProperties
base.disableMouse()
wp = WindowProperties()
wp.setTitle('Toontown Emulator')
base.win.requestProperties( wp )
base.camera.hide()
base.setAspectRatio(1.33333334)
#base.oobe()


legsAnimDict = {'jump-squat': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_jump-zstart.bam',
 'wave': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_wave.bam',
 'victory': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_victory-dance.bam',
 'jump': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_jump.bam',
 'running-jump-land': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_leap_zend.bam',
 'run': 'phase_3/models/char/tt_a_chr_dgs_shorts_legs_run.bam',
 'sidestep-right': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_jump-back-right.bam',
 'running-jump': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_running-jump.bam',
 'walk': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_walk.bam',
 'jump-land': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_jump-zend.bam',
 'right-point': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_right-point.bam',
 'neutral': 'phase_3/models/char/tt_a_chr_dgs_shorts_legs_neutral.bam',
 'jump-idle': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_jump-zhang.bam',
 'running-jump-squat': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_leap_zstart.bam',
 'running-jump-idle': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_leap_zhang.bam',}
torsoAnimDict = {'slip-forward': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_slip-forward.bam',
 'wave': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_wave.bam',
 'victory': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_victory-dance.bam',
 'jump': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_jump.bam',
 'run': 'phase_3/models/char/tt_a_chr_dgl_shorts_torso_run.bam',
 'jump-land': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_jump-zend.bam',
 'neutral': 'phase_3/models/char/tt_a_chr_dgl_shorts_torso_neutral.bam',
 'jump-idle': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_jump-zhang.bam',
 'running-jump-idle': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_leap_zhang.bam',}


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
 'legs': toonLegs}, {'torso': torsoAnimDict,
 'legs': legsAnimDict})
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
#base.camera.reparentTo(toonBody)
#base.camera.setPos(0, -6.0 - offset, 3.1)
wallBitmask = BitMask32(1)
floorBitmask = BitMask32(2)
base.cTrav = CollisionTraverser()

def getAirborneHeight():
    return offset + 0.025


walkControls = GravityWalker(legacyLifter=True)
walkControls.setWallBitMask(wallBitmask)
walkControls.setFloorBitMask(floorBitmask)
walkControls.setWalkSpeed(24.0, 30.0, 15.0, 80.0)
walkControls.initializeCollisions(base.cTrav, toonBody, floorOffset=0.025, reach=4.0)
walkControls.setAirborneHeightFunc(getAirborneHeight)
walkControls.enableAvatarControls()
toonBody.physControls = walkControls

def setWatchKey(key, input, keyMapName):

    def watchKey(active = True):
        if active == True:
            inputState.set(input, True)
            keyMap[keyMapName] = 1
        else:
            inputState.set(input, False)
            keyMap[keyMapName] = 0

    base.accept(key, watchKey, [True])
    base.accept(key + '-up', watchKey, [False])


keyMap = {'left': 0,
 'right': 0,
 'forward': 0,
 'backward': 0,
 'control': 0}
setWatchKey('arrow_up', 'forward', 'forward')
setWatchKey('control-arrow_up', 'forward', 'forward')
setWatchKey('alt-arrow_up', 'forward', 'forward')
setWatchKey('shift-arrow_up', 'forward', 'forward')
setWatchKey('arrow_down', 'reverse', 'backward')
setWatchKey('control-arrow_down', 'reverse', 'backward')
setWatchKey('alt-arrow_down', 'reverse', 'backward')
setWatchKey('shift-arrow_down', 'reverse', 'backward')
setWatchKey('arrow_left', 'turnLeft', 'left')
setWatchKey('control-arrow_left', 'turnLeft', 'left')
setWatchKey('alt-arrow_left', 'turnLeft', 'left')
setWatchKey('shift-arrow_left', 'turnLeft', 'left')
setWatchKey('arrow_right', 'turnRight', 'right')
setWatchKey('control-arrow_right', 'turnRight', 'right')
setWatchKey('alt-arrow_right', 'turnRight', 'right')
setWatchKey('shift-arrow_right', 'turnRight', 'right')
setWatchKey('control', 'jump', 'control')
movingNeutral, movingForward = (False, False)
movingRotation, movingBackward = (False, False)
movingJumping = False

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


def handleMovement(task):
    if keyMap['control'] == 1:
        if keyMap['forward'] or keyMap['backward'] or keyMap['left'] or keyMap['right']:
            if movingJumping == False:
                if toonBody.physControls.isAirborne:
                    setMovementAnimation('running-jump-idle')
                elif keyMap['forward']:
                    if movingForward == False:
                        setMovementAnimation('run')
                elif keyMap['backward']:
                    if movingBackward == False:
                        setMovementAnimation('walk', playRate=-1.0)
                elif keyMap['left'] or keyMap['right']:
                    if movingRotation == False:
                        setMovementAnimation('walk')
            elif not toonBody.physControls.isAirborne:
                if keyMap['forward']:
                    if movingForward == False:
                        setMovementAnimation('run')
                elif keyMap['backward']:
                    if movingBackward == False:
                        setMovementAnimation('walk', playRate=-1.0)
                elif keyMap['left'] or keyMap['right']:
                    if movingRotation == False:
                        setMovementAnimation('walk')
        elif movingJumping == False:
            if toonBody.physControls.isAirborne:
                setMovementAnimation('jump-idle')
            elif movingNeutral == False:
                setMovementAnimation('neutral')
        elif not toonBody.physControls.isAirborne:
            if movingNeutral == False:
                setMovementAnimation('neutral')
    elif keyMap['forward'] == 1:
        if movingForward == False:
            if not toonBody.physControls.isAirborne:
                setMovementAnimation('run')
    elif keyMap['backward'] == 1:
        if movingBackward == False:
            if not toonBody.physControls.isAirborne:
                setMovementAnimation('walk', playRate=-1.0)
    elif keyMap['left'] or keyMap['right']:
        if movingRotation == False:
            if not toonBody.physControls.isAirborne:
                setMovementAnimation('walk')
    elif not toonBody.physControls.isAirborne:
        if movingNeutral == False:
            setMovementAnimation('neutral')
    return Task.cont


base.taskMgr.add(handleMovement, 'controlManager')

def collisionsOn():
    toonBody.physControls.setCollisionsActive(True)
    toonBody.physControls.isAirborne = True


def collisionsOff():
    toonBody.physControls.setCollisionsActive(False)
    toonBody.physControls.isAirborne = True


def toggleCollisions():
    if toonBody.physControls.getCollisionsActive():
        toonBody.physControls.setCollisionsActive(False)
        toonBody.physControls.isAirborne = True
    else:
        toonBody.physControls.setCollisionsActive(True)
        toonBody.physControls.isAirborne = True


base.accept('f1', toggleCollisions)
toonBody.collisionsOn = collisionsOn
toonBody.collisionsOff = collisionsOff
toonBody.toggleCollisions = toggleCollisions
localAvatar = toonBody
base.localAvatar = localAvatar
localAvatar.physControls.placeOnFloor()
onScreenDebug.enabled = True

def updateOnScreenDebug(task):

    onScreenDebug.add('Avatar Position', localAvatar.getPos())
    onScreenDebug.add('Avatar Angle', localAvatar.getHpr())

    return Task.cont

base.taskMgr.add(updateOnScreenDebug, 'UpdateOSD')


class ToonTAGS():

    def setTalk(self, message):
        if hasattr(self, 'chatbubble'):
            self.chatbubble.removeNode()
        self.chatbubble = loader.loadModel('phase_3/models/props/chatbox.bam')
        self.chatbubble.reparentTo(localAvatar)
        self.chatbubble.setPos(0, 0, 3.5)
        self.chatbubble.setBillboardAxis(1)
        self.chatbubble.setScale(0.3)
        self.chatbubble.find('**/chatBalloon').setPos(0, 0.05, 0)
        self.chatbubble.find('**/chatBalloon').setSx(0.8)
        self.talk = OnscreenText(scale=0.7, font=loader.loadFont('phase_3/models/fonts/ImpressBT.ttf'), pos=(0.9, 3), text=message, wordwrap=10, decal=True, parent=self.chatbubble, align=TextNode.ALeft)
        self.tag.hide()
        Sequence(Wait(5), Func(self.chatbubble.removeNode), Func(self.tag.show)).start()

    def toonSound(self, species, type):
        loader.loadSfx('phase_3.5/audio/dial/AV_{0}_{1}'.format(species, type)).play()

    def sendChat(self, message):
        self.toonSpecies = '' + species + ''
        try:
            self.setTalk(message)
            if len(message) <= 4:
                if 'fuck' in message:
                    window.destroy()
                elif '?' in message:
                    self.toonSound(self.toonSpecies, 'question.mp3')
                elif 'ooo' in message:
                    self.toonSound(self.toonSpecies, 'howl.mp3')
                elif '!' in message:
                    self.toonSound(self.toonSpecies, 'exclaim.mp3')
                else:
                    self.toonSound(self.toonSpecies, 'short.mp3')
            elif len(message) >= 5 and len(message) <= 9:
                if '?' in message:
                    self.toonSound(self.toonSpecies, 'question.mp3')
                elif 'ooo' in message:
                    self.toonSound(self.toonSpecies, 'howl.mp3')
                elif '!' in message:
                    self.toonSound(self.toonSpecies, 'exclaim.mp3')
                else:
                    self.toonSound(self.toonSpecies, 'med.mp3')
            elif len(message) >= 10:
                if '?' in message:
                    self.toonSound(self.toonSpecies, 'question.mp3')
                elif 'ooo' in message:
                    self.toonSound(self.toonSpecies, 'howl.mp3')
                elif '!' in message:
                    self.toonSound(self.toonSpecies, 'exclaim.mp3')
                else:
                    self.toonSound(self.toonSpecies, 'long.mp3')
        except Exception as e:
            print e

    def setName(self, name):
        if hasattr(self, 'tag'):
            self.tag.removeNode()
        self.tag = OnscreenText(scale=0.3, font=loader.loadFont('phase_3/models/fonts/ImpressBT.ttf'), pos=(0, 3.25), text=name, bg=(0.9, 0.9, 0.9, 0.3), fg=(0, 0, 1, 1), wordwrap=7, decal=True, parent=DuckBody)
        self.tag.setBillboardAxis(2)

    def __init__(self):
        self.setName('' + name + '')


class ClassicChatBox(ToonTAGS):
    ChatBox = loader.loadModel('phase_3.5/models/gui/chat_input_gui.bam')
    SlipOpen = loader.loadSfx('phase_3.5/audio/sfx/GUI_quicktalker.mp3')

    def __setNone__(self):
        text = self.OldChatBoxEntry['text']
        self.OldChatBoxEntry.set(text)
        return True

    def __action__(self, message):
        self.OldChatBoxGui.removeNode()
        self.OldChatBoxEntry.removeNode()
        self.OldChatBoxClose.removeNode()
        self.OldChatBoxBack.removeNode()
        self.OldChatBoxTalk.removeNode()
        self.__addOnButton__()
        if message != '':
            base.localAvatar.ToonTAGS.sendChat(message)
        else:
            return None
        return True

    def __delNavs__(self):
        self.OldChatBoxGui.removeNode()
        self.OldChatBoxEntry.removeNode()
        self.OldChatBoxClose.removeNode()
        self.OldChatBoxBack.removeNode()
        self.OldChatBoxTalk.removeNode()
        self.__addOnButton__()
        return True

    def __sayIt__(self):
        self.OldChatBoxGui.removeNode()
        self.OldChatBoxEntry.removeNode()
        self.OldChatBoxClose.removeNode()
        self.OldChatBoxBack.removeNode()
        self.OldChatBoxTalk.removeNode()
        self.__addOnButton__()
        base.localAvatar.ToonTAGS.sendChat(self.OldChatBoxEntry.get(1.0))
        return True

    def __addNavs__(self):
        self.OldChatBoxOpen.removeNode()
        self.OldChatBoxGui = DirectFrame(pos=(-0.18, 0, 0.901), scale=1, frameSize=(0, 0, 0, 0), image=self.ChatBox.find('**/Chat_Bx_FNL'))
        self.OldChatBoxEntry = DirectEntry(text='', scale=0.04, command=self.__action__, frameSize=(-0.0, 32.6, 1, -0.5), frameColor=(0, 0, 0, 0), cursorKeys=1, initialText='', numLines=1, width=21.5, focus=1, text_scale=1.5, pos=(-0.85, 0, 0.9))
        self.OldChatBoxBack = DirectButton(frameSize=None, image=(self.ChatBox.find('**/ChtBx_BackBtn_UP'), self.ChatBox.find('**/ChtBx_BackBtn_DN'), self.ChatBox.find('**/ChtBx_BackBtn_Rllvr')), relief=None, command=self.__setNone__, text=('', 'Clear', 'Clear', 'Clear'), text_pos=(0, -0.09), geom=None, scale=1.1, pad=(0.01, 0.01), suppressKeys=0, pos=(-0.85, 0, 0.9), hpr=(0, 0, 0), text_scale=0.05, borderWidth=(0.015, 0.01))
        self.OldChatBoxClose = DirectButton(frameSize=None, image=(self.ChatBox.find('**/CloseBtn_UP'), self.ChatBox.find('**/CloseBtn_DN'), self.ChatBox.find('**/CloseBtn_Rllvr')), relief=None, command=self.__delNavs__, text=('', 'Cancel', 'Cancel', 'Cancel'), text_pos=(0, -0.09), geom=None, scale=1.1, pad=(0.01, 0.01), suppressKeys=0, pos=(-0.85, 0, 0.9), hpr=(0, 0, 0), text_scale=0.05, borderWidth=(0.015, 0.01))
        self.OldChatBoxTalk = DirectButton(frameSize=None, image=(self.ChatBox.find('**/ChtBx_ChtBtn_UP'), self.ChatBox.find('**/ChtBx_ChtBtn_DN'), self.ChatBox.find('**/ChtBx_ChtBtn_RLVR')), relief=None, command=self.__sayIt__, text=('', 'Say It', 'Say It', 'Say It'), text_pos=(0, -0.09), geom=None, scale=1.1, pad=(0.01, 0.01), suppressKeys=0, pos=(0.62, 0, 0.912), hpr=(0, 0, 0), text_scale=0.05, borderWidth=(0.015, 0.01))
        return True

    def __addOnButton__(self):
        self.OldChatBoxOpen = DirectButton(frameSize=None, image=(self.ChatBox.find('**/ChtBx_ChtBtn_UP'), self.ChatBox.find('**/ChtBx_ChtBtn_DN'), self.ChatBox.find('**/ChtBx_ChtBtn_RLVR')), command=self.__addNavs__, relief=None, text=('', 'Chat', 'Chat', 'Chat'), text_pos=(0, -0.09), clickSound=self.SlipOpen, geom=None, scale=1.2, pad=(0.01, 0.01), suppressKeys=0, pos=(-1.7, 0, 0.928), hpr=(0, 0, 0), text_scale=0.06, borderWidth=(0.015, 0.01))
        return True

    def __init__(self):
        self.__addOnButton__()

'''class CameraViews():

    def changeView(self):
        if self.objectId != 7:
            base.camera.posHprInterval(0.5, self.posList[self.objectId], self.hprList[self.objectId]).start()
            self.objectId += 1
        else:
            self.objectId = 0
            base.camera.posHprInterval(0.5, self.posList[self.objectId], self.hprList[self.objectId]).start()
            self.objectId += 1

    def changeViewRev(self):
        if self.objectId != -1:
            base.camera.posHprInterval(0.5, self.posList[self.objectId], self.hprList[self.objectId]).start()
            self.objectId -= 1
        else:
            self.objectId = 6
            base.camera.posHprInterval(0.5, self.posList[self.objectId], self.hprList[self.objectId]).start()
            self.objectId -= 1

    def __init__(self):
        self.objectId = 0
        self.posList = [(0, 1, 3.5),
         (8, 15, 5.5),
         (0, -26, 7),
         (0, -19, 6.5),
         (0, -13.5, 3.0),
         (0, -13.5, 3.0)]
        self.hprList = [(0, 0, 0),
         (150, -5.5, 0),
         (0, -5.5, 0),
         (0, -8.0, 0),
         (0, 0, 0),
         (0, 0, 0)]
        base.accept('tab', self.changeView, [])
        base.accept('shift-tab', self.changeViewRev, [])'''

#base.localAvatar.CameraViews = CameraViews()
base.localAvatar.ClassicChatBox = ClassicChatBox()
Music = loader.loadMusic('phase_4/audio/bgm/TC_nbrhood.mid')
#MusicVolume = (0.10)
Music.play()
Music.setLoop(1)
#Music.setVolume(MusicVolume)
camera.setPos(12, 9, 4)
camera.setHpr(-52, 0, 0)
camera.posHprInterval(2, (0, -6.0 - offset, 3.1), (0, 0, 0), blendType='easeInOut').start()
base.camera.reparentTo(toonBody)
def UpdateTunnel(task):
    pass


ttc = loader.loadModel('phase_4/models/neighborhoods/toontown_central_full.bam')
ttc.reparentTo(render)



run()
