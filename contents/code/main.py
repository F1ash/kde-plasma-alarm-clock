# -*- coding: utf-8 -*-
#  main.py
#  
#  Copyright 2012 Flash <kaperang07@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdeui import KPageDialog, KDialog, KNotification
from PyKDE4.kdecore import KStandardDirs as KSD
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from checkAlarmList import CheckAlarmList
from AppletSettings import AppletSettings
from Functions import getAlarmTimesList
import os

class plasmaAlarmClock(plasmascript.Applet):
	alarm = pyqtSignal(list, list, list)
	nextAlarm = pyqtSignal(str)
	def __init__(self, parent = None):
		plasmascript.Applet.__init__(self, parent)
		self.name = 'kde-plasma-alarm-clock'
		self.Settings = QSettings(self.name, self.name)

		mark = 'plasma/plasmoids/' + self.name
		self.plasmaPath = ''
		for d in KSD().resourceDirs('data') :
			_path = os.path.join(str(d), mark)
			if os.path.isfile(os.path.join(_path, 'contents/icons/alarm.png')) :
				self.plasmaPath = _path
		if self.plasmaPath == '' :
			self.plasmaPath = os.path.join(os.getcwd(), self.name)
		self.appletWD = os.path.join(self.plasmaPath, 'contents')

		self.alarmIconPath = self.appletWD + '/icons/alarm.png'
		self.alarm1IconPath = self.appletWD + '/icons/alarm1.png'
		self.alarm2IconPath = self.appletWD + '/icons/alarm2.png'
		self.alarm_disabledIconPath = self.appletWD + '/icons/alarm_disabled.png'
		#print self.alarmIconPath, ':', self.appletWD
		self.paused = True

	def initVar(self):
		if self.Settings.value('Alarm Clock Enable', 'True') == 'True' :
			self.alarmed = True
		else:
			self.alarmed = False
		self.alarmTimesList = getAlarmTimesList(self.Settings)
		#print self.alarmTimesList

	def initLayout(self):
		if hasattr(self.layout,'count') :
			while self.layout.count() > 0 :
				idx = self.layout.count()-1
				self.layout.itemAt(idx).setVisible(False)
				self.layout.removeAt(idx)
		self.layout.setOrientation(Qt.Vertical)
		if self.config().readEntry('Icon Show', 'True') == 'True' :
			self.layout.addItem(self.alarmIcon)
			self.layout.setAlignment(self.alarmIcon, Qt.AlignCenter)
			self.alarmIcon.setVisible(True)
		if self.config().readEntry('Time Show', 'True') == 'True' :
			self.layout.addItem(self.timeLCD)
			self.layout.setAlignment(self.timeLCD, Qt.AlignCenter)
			self.timeLCD.setVisible(True)

		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.setSpacing(0)
		self.setLayout(self.layout)

	def init(self):
		self.initVar()
		self.layout = QGraphicsLinearLayout(self.applet)
		self.alarmIcon = Plasma.IconWidget()
		self.alarmIcon.setIcon(QIcon().fromTheme('alarm-clock', QIcon(':/'+self.alarmIconPath)))
		self.alarmIcon.mouseReleaseEvent = self.mouseReleaseEvent

		self.LCD = QLCDNumber()
		self.LCD.setSegmentStyle(QLCDNumber.Flat)
		self.LCD.setStyleSheet('QWidget {background: rgba(0,0,0,0);}')
		self.LCD.setSmallDecimalPoint(True)
		self.timeLCD = QGraphicsProxyWidget()
		self.timeLCD.setWidget(self.LCD)
		self.timeLCD.mouseReleaseEvent = self.mouseReleaseEvent
		self.initLayout()
		self.setHasConfigurationInterface(True)

		self.setNewToolTip()

		self.alarm.connect(self.showAlarm)
		self.nextAlarm.connect(self.setNewToolTip)
		self.checkAlarmList = CheckAlarmList(self)
		self.checkAlarmList.started.connect(self.start)
		self.checkAlarmList.start()

	def start(self):
		self.checkAlarmList.started.disconnect(self.start)
		self.timer = QTimer()
		self.timer.timeout.connect(self.blink)
		if self.alarmed : self.changeActivity()
		else : self.setNewToolTip('Stopped')
		self.connect(self.applet, SIGNAL('destroyed()'), self.eventClose)

	def mousePressEvent(self, ev):
		if ev.type() == QEvent.GraphicsSceneMousePress :
			ev.accept()
	def mouseReleaseEvent(self, ev):
		if ev.type() == QEvent.GraphicsSceneMouseRelease :
			self.changeActivity()

	def changeActivity(self):
		if not self.paused :
			self.timer.stop()
			self.alarmIcon.setIcon(self.alarm_disabledIconPath)
			self.setNewToolTip('Stopped')
			self.paused = True
		else :
			self.alarmIcon.setIcon(self.alarm1IconPath)
			self.timer.start(1000)
			self.paused = False
			self.checkAlarmList.check_alarm()

	def blink(self):
		try :
			if self.alarmIcon.isVisible() :
				self.alarmIcon.setIcon(self.alarm2IconPath)
			self.LCD.setStyleSheet('QWidget {background: rgba(0,0,0,16);}')
			if self.LCD.isVisible() :
				self.LCD.display(self.currTime.replace(':', ' '))
			QTimer().singleShot(250, self.unBlink)
		except Exception, err : print err, 'in blink()'
		finally : pass

	def unBlink(self):
		try :
			if self.alarmIcon.isVisible() :
				self.alarmIcon.setIcon(self.alarm1IconPath)
			self.LCD.setStyleSheet('QWidget {background: rgba(0,0,0,0);}')
			self.LCD.display(self.currTime)
		except Exception, err : print err, 'in unBlink()'
		finally : pass

	def showAlarm(self, msgs, sounds, cmds):
		#print msgs, sounds, cmds, 'alarmed'
		playSounds = []
		runCmds = []
		for sound in sounds :
			if not os.path.isfile(sound.toLocal8Bit().data()) :
				sound = QString('/usr/share/sounds/pop.wav')
				#print (sound)
			playSounds.append(QProcess())
			playSounds[len(playSounds)-1].startDetached('/usr/bin/play', QStringList() << sound)
		for cmd in cmds :
			if cmd.isEmpty() : continue
			runCmds.append(QProcess())
			runCmds[len(runCmds)-1].startDetached('/usr/bin/sh', QStringList() << '-c' << cmd)
		for msg in msgs :
			if msg.isEmpty() : continue
			notify = KNotification.event(\
						KNotification.Notification, \
						'Alarm Clock', \
						msg, \
						QPixmap(self.alarmIconPath))

	def setNewToolTip(self, msg = ''):
		Plasma.ToolTipManager.self().setContent( \
				self.applet, \
				Plasma.ToolTipContent( \
								'Alarm Clock', \
								QString(msg), \
								QIcon(self.alarmIconPath) ) )

	def createConfigurationInterface(self, parent):
		self.appletSettings = AppletSettings(self, parent)
		parent.addPage(self.appletSettings, "Settings")
		self.connect(parent, SIGNAL("okClicked()"), self.configAccepted)
		self.connect(parent, SIGNAL("cancelClicked()"), self.configDenied)

	def showConfigurationInterface(self):
		self.dialog = KPageDialog()
		self.dialog.setModal(True)
		self.dialog.setFaceType(KPageDialog.List)
		self.dialog.setButtons( KDialog.ButtonCode(KDialog.Ok | KDialog.Cancel) )
		self.createConfigurationInterface(self.dialog)
		self.dialog.move(self.popupPosition(self.dialog.sizeHint()))
		self.dialog.exec_()

	def configAccepted(self):
		self.appletSettings.refreshSettings(self)
		self.initVar()
		self.dialog.done(0)
		self.initLayout()
		self.checkAlarmList.check_alarm()

	def configDenied(self):
		self.dialog.done(0)

	def eventClose(self):
		self.timer.stop()
		self.timer.timeout.disconnect(self.blink)
		if hasattr(self, 'checkAlarmList') :
			self.checkAlarmList.stop()
			self.checkAlarmList.quit()
			del self.checkAlarmList
			self.checkAlarmList = None
		self.alarm.disconnect(self.showAlarm)
		self.nextAlarm.disconnect(self.setNewToolTip)
		print 'AlarmClock is closed'

	def __del__(self): self.eventClose()

def CreateApplet(parent):
	return plasmaAlarmClock(parent)
