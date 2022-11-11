# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'action_tap.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
import enum

from TouchManager.GameControllerModel import GameControllerModel
from TouchManager.QLevelViewer import QLevelViewer

from TouchManager.GameControllerController import GameControllerController


class PlayState(enum.Enum):
    Played = 1
    Playing = 2
    ToBePlayed = 3


class QLevelState(QWidget):
    def __init__(self, model: GameControllerModel, controller: GameControllerController, level_num: int,
                 level_name: str, parent=QWidget):
        super(QWidget, self).__init__()
        self.model = model
        self.controler = controller
        self.level_num = level_num
        self.level_name = level_name
        self.parent = parent
        self.currentLevelViewer = QLevelViewer(self.model, level_num, level_name)
        self.logs = QtWidgets.QPlainTextEdit()
        self.lay = QVBoxLayout()
        self.lblScreenChecks = QtWidgets.QLabel(self)

        self.color_played = (86, 101, 115)
        self.color_playing = (213, 216, 220)
        self.color_not_played = (33, 47, 61)

        self.fgplayed = (255, 255, 255)
        self.fgplaying = (0, 0, 0)

        self.state = PlayState.ToBePlayed

        self.updateStateColor()
        self.currentLogs = []
        self.screensCount = 0
        # self.last_logs = []
        self.setupUi()
        self.reset()

    def changeScreenCount(self, newCount: int):
        self.screensCount = newCount
        if self.screensCount == 0:
            self.lblScreenChecks.setText("")
        else:
            self.lblScreenChecks.setText("Total screens: {}".format(self.screensCount))

    def addLog(self, log: str):
        if log == "screen check":
            self.changeScreenCount(self.screensCount + 1)
        else:
            self.currentLogs.append(log)
            self.logs.appendPlainText(log)

    def reset(self):
        self.SetState(PlayState.ToBePlayed)
        self.logs.clear()
        self.changeScreenCount(0)

    def SetState(self, state: PlayState):
        if state == self.state:
            return
        reset = False
        if self.state in [PlayState.Played, PlayState.Playing] and state in [PlayState.ToBePlayed, PlayState.Playing]:
            reset = True
        self.state = state
        self.updateStateColor()
        if reset:
            # self.last_logs = self.currentLogs.copy()
            self.currentLogs = []
            self.logs.setPlainText("")
            self.changeScreenCount(0)
        # elif state == PlayState.Played and len(self.last_logs) > 0:
        #     for l in self.last_logs:
        #         self.addLog(l)

    def updateStateColor(self):
        bgcolor = (255, 255, 255)
        fgcolor = (0, 0, 0)
        if self.state == PlayState.Played:
            bgcolor = self.color_played
            fgcolor = self.fgplayed
        elif self.state == PlayState.Playing:
            bgcolor = self.color_playing
            fgcolor = self.fgplaying
        elif self.state == PlayState.ToBePlayed:
            bgcolor = self.color_not_played
            fgcolor = self.fgplayed
        self.logs.setStyleSheet("color: rgb({}, {}, {})".format(fgcolor[0], fgcolor[1], fgcolor[2]))
        self.lblScreenChecks.setStyleSheet("color: rgb({}, {}, {})".format(fgcolor[0], fgcolor[1], fgcolor[2]))
        self.setStyleSheet(
            "background-color: rgb({}, {}, {}); border-radius: 5px;".format(bgcolor[0], bgcolor[1], bgcolor[2]))

    def color_from_level(self, level_name: str):
        if level_name not in self.levels_colors:
            return 255, 255, 255
        else:
            return self.levels_colors[level_name]

    def setupUi(self):
        fram_lay = QHBoxLayout()
        self.lay.setAlignment(Qt.AlignTop)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        fram_lay.addWidget(self.currentLevelViewer)
        self.lay.addLayout(fram_lay)
        self.logs.setReadOnly(True)
        self.lblScreenChecks.setAlignment(Qt.AlignCenter)
        self.lay.addWidget(self.logs)
        self.lay.addWidget(self.lblScreenChecks)

        self.setLayout(self.lay)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.currentLevelViewer.setClickable(True)
        self.currentLevelViewer.onLevelClicked.connect(self.requestedLevelChange)

    def requestedLevelChange(self):
        self.controler.changeLevelRequested(self.level_num)
