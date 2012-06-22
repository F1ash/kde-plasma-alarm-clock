# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdeui import KPageDialog, KDialog, KNotification
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
import os.path, os
from AppletSettings import AppletSettings
from Functions import *

class IconBlink(QThread):
	def __init__(self, parent = None):
		QThread.__init__(self, parent)
		self.prnt = parent
		self.runKey = True

	def run(self):
		while self.runKey :
			self.prnt.alarmIcon.setIcon(self.prnt.alarm2IconPath)
			if self.runKey :
				self.msleep(250)
				self.prnt.alarmIcon.setIcon(self.prnt.alarm1IconPath)
				if self.runKey : self.msleep(3750)

	def stop(self): self.runKey = False

	def __del__(self):
		self.stop()

class CheckAlarmList(QThread):
	def __init__(self, parent = None):
		QThread.__init__(self, parent)
		self.prnt = parent
		self.nextAlarm = ''
		self.runKey = True

	def run(self):
		while self.runKey :
			alarmNow, msgs, sounds, newAlarmTime, pause = alarmTime(self.prnt.Settings, self.prnt.alarmTimesList)
			if alarmNow :
				self.prnt.alarm.emit(msgs, sounds)
			if self.nextAlarm != newAlarmTime :
				self.nextAlarm = newAlarmTime
				self.prnt.nextAlarm.emit('<b>Next alarm in ' + newAlarmTime +'</b>')
			if self.runKey : self.msleep(pause)

	def stop(self): self.runKey = False

	def __del__(self):
		self.stop()

class plasmaAlarmClock(plasmascript.Applet):
	alarm = pyqtSignal(list, list)
	nextAlarm = pyqtSignal(str)
	def __init__(self, parent = None):
		plasmascript.Applet.__init__(self, parent)

		self.kdehome = '/usr/share/kde4/apps/plasma/plasmoids/kde-plasma-alarm-clock/contents/'
		self.Settings = QSettings('kde-plasma-alarm-clock', 'kde-plasma-alarm-clock')

		if os.path.exists(self.kdehome + 'icons/alarm.png') :
			self.alarmIconPath = self.kdehome + 'icons/alarm.png'
			self.alarm1IconPath = self.kdehome + 'icons/alarm1.png'
			self.alarm2IconPath = self.kdehome + 'icons/alarm2.png'
			self.alarm_disabledIconPath = self.kdehome + 'icons/alarm_disabled.png'
		else :
			self.alarmIconPath = os.path.join(os.getcwd(), 'kde-plasma-alarm-clock/contents/icons/alarm.png')
			self.alarm1IconPath = os.path.join(os.getcwd(), 'kde-plasma-alarm-clock/contents/icons/alarm1.png')
			self.alarm2IconPath = os.path.join(os.getcwd(), 'kde-plasma-alarm-clock/contents/icons/alarm2.png')
			self.alarm_disabledIconPath = os.path.join(os.getcwd(), 'kde-plasma-alarm-clock/contents/icons/alarm_disabled.png')

	def initVar(self):
		if self.Settings.value('Alarm Clock Enable', 'True') == 'True' :
			self.alarmed = True
		else:
			self.alarmed = False
		self.alarmTimesList = getAlarmTimesList(self.Settings)
		#print self.alarmTimesList

	def init(self):
		self.initVar()
		self.layout = QGraphicsLinearLayout(self.applet)
		self.alarmIcon = Plasma.IconWidget()
		self.alarmIcon.setIcon(self.alarmIconPath)
		if self.applet.formFactor() == Plasma.Horizontal :
			self.alarmIcon.setOrientation(Qt.Horizontal)
			self.layout.setOrientation(Qt.Horizontal)
		else :
			self.alarmIcon.setOrientation(Qt.Vertical)
			self.layout.setOrientation(Qt.Vertical)
		self.layout.addItem(self.alarmIcon)

		self.layout.setAlignment(self.alarmIcon, Qt.AlignLeft)
		self.layout.setSpacing(0)
		self.setLayout(self.layout)
		self.setHasConfigurationInterface(True)

		self.setNewToolTip()

		self.alarm.connect(self.showAlarm)
		self.nextAlarm.connect(self.setNewToolTip)
		self.alarmIcon.clicked.connect(self.changeActivity)
		if self.alarmed : self.alarmIcon.clicked.emit()
		else : self.setNewToolTip('Stopped')

	def changeActivity(self):
		if hasattr(self, 'checkAlarmList') and self.checkAlarmList is not None :
			self.checkAlarmList.stop()
			del self.checkAlarmList
			if hasattr(self, 'iconBlink') and self.iconBlink is not None :
				self.iconBlink.stop()
				del self.iconBlink
			self.alarmIcon.setIcon(self.alarm_disabledIconPath)
			self.setNewToolTip('Stopped')
		else :
			if not hasattr(self, 'iconBlink') or self.iconBlink is None :
				self.iconBlink = IconBlink(self)
				self.iconBlink.start()
			self.checkAlarmList = CheckAlarmList(self)
			self.checkAlarmList.start()

	def showAlarm(self, msgs, sounds):
		#print msgs, sounds, 'alarmed'
		for sound in sounds :
			self.play = QProcess()
			if not os.path.isfile(sound.toLocal8Bit().data()) :
				sound = QString('/usr/share/sounds/pop.wav')
				#print (sound)
			self.play.start('/usr/bin/play', QStringList() << sound)
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

	def configDenied(self):
		self.dialog.done(0)

	def __del__(self):
		if hasattr(self, 'iconBlink') :
			self.iconBlink.stop()
			del self.iconBlink
		if hasattr(self, 'checkAlarmList') :
			self.checkAlarmList.stop()
			del self.checkAlarmList

def CreateApplet(parent):
	return plasmaAlarmClock(parent)
