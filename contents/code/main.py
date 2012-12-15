# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdeui import KPageDialog, KDialog, KNotification
from PyKDE4.kdecore import KStandardDirs as KSD
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
import os.path, os
from AppletSettings import AppletSettings
from Functions import *

class CheckAlarmList(QThread):
	def __init__(self, parent = None):
		QThread.__init__(self, parent)
		self.prnt = parent
		self.nextAlarm = ''
		self.runKey = True

	def check_alarm(self):
		alarmNow, msgs, sounds, cmds, newAlarmTime, pause, currTime = \
				alarmTime(self.prnt.Settings, self.prnt.alarmTimesList)
		if self.runKey and alarmNow and not self.prnt.paused :
			self.prnt.alarm.emit(msgs, sounds, cmds)
		ct = '<br><b>Current time ' + currTime +'</b></br>'
		self.prnt.LCD.display(currTime)
		if self.runKey and newAlarmTime is None :
			self.prnt.nextAlarm.emit('<b>Not alarmed.</b>' + ct)
		else :
			if self.nextAlarm != newAlarmTime :
				self.nextAlarm = newAlarmTime
			if self.runKey :
				msg = 'Stopped' if self.prnt.paused else 'Next alarm in ' + self.nextAlarm
				self.prnt.nextAlarm.emit('<b>' + msg +'</b>' + ct)
		return pause

	def run(self):
		while self.runKey :
			pause = self.check_alarm()
			if self.runKey : self.msleep(pause)

	def stop(self): self.runKey = False

	def __del__(self): self.stop()

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
		self.layout.setAlignment(self.timeLCD, Qt.AlignCenter)
		if self.config().readEntry('Time Show', 'True') == 'True' :
			self.layout.addItem(self.timeLCD)
			self.timeLCD.setVisible(True)

		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.setSpacing(0)
		self.setLayout(self.layout)

	def init(self):
		self.initVar()
		self.layout = QGraphicsLinearLayout(self.applet)
		self.alarmIcon = Plasma.IconWidget()
		self.alarmIcon.setIcon(QIcon().fromTheme('alarm-clock', QIcon(':/'+self.alarmIconPath)))

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
		self.alarmIcon.clicked.connect(self.changeActivity)
		self.checkAlarmList = CheckAlarmList(self)
		self.checkAlarmList.start()
		self.timer = QTimer()
		self.timer.timeout.connect(self.blink)
		if self.alarmed : self.alarmIcon.clicked.emit()
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
			self.alarmIcon.setIcon(self.alarm2IconPath)
			self.LCD.setStyleSheet('QWidget {background: rgba(0,0,0,16);}')
			QTimer().singleShot(250, self.unBlink)
		except Exception, err : print err, 'in blink()'
		finally : pass

	def unBlink(self):
		try :
			self.alarmIcon.setIcon(self.alarm1IconPath)
			self.LCD.setStyleSheet('QWidget {background: rgba(0,0,0,0);}')
		except Exception, err : print err, 'in unBlink()'
		finally : pass

	def showAlarm(self, msgs, sounds, cmds):
		#print msgs, sounds, cmds, 'alarmed'
		for sound in sounds :
			self.play = QProcess()
			if not os.path.isfile(sound.toLocal8Bit().data()) :
				sound = QString('/usr/share/sounds/pop.wav')
				#print (sound)
			self.play.start('/usr/bin/play', QStringList() << sound)
		for cmd in cmds :
			#print (cmd)
			if cmd.isEmpty() : continue
			self.play = QProcess()
			self.play.start('/usr/bin/sh', QStringList() << cmd)
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
			del self.checkAlarmList
			self.checkAlarmList = None
		self.alarm.disconnect(self.showAlarm)
		self.nextAlarm.disconnect(self.setNewToolTip)
		#self.alarmIcon.clicked.disconnect(self.changeActivity)
		print 'AlarmClock is closed'

	def __del__(self): self.eventClose()

def CreateApplet(parent):
	return plasmaAlarmClock(parent)
