# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdeui import KTimeComboBox
import os.path, os, stat

class Blank(QDialog):
	def __init__(self, obj = None, name = None, parent = None):
		QDialog.__init__(self, parent)

		self.prnt = parent
		self.Settings = obj.Settings
		self.name = name
		self.itemEnable = Qt.Unchecked

		if self.name is not None :
			self.Settings.beginGroup(self.name)
			msg = self.Settings.value('Message', '').toString()
			cmd = self.Settings.value('Command', '').toString()
			_time = str(self.Settings.value('Time', '').toString())
			if len(_time.split(':'))==2 :
				_h, _m = _time.split(':')
			else : _h, _m = 0, 0
			#print _h, _m
			time = (int(_h), int(_m))
			path = self.Settings.value('Sound', '').toString()
			self.Settings.endGroup()
		else : time = path = None

		self.layout = QGridLayout()

		self.nameLabel = QLabel("Name :")
		self.layout.addWidget(self.nameLabel, 0, 0)
		self.nameAlarm = QLineEdit()
		self.nameAlarm.setText('' if self.name is None else self.name)
		self.nameAlarm.setMinimumWidth(220)
		self.layout.addWidget(self.nameAlarm, 0, 1)

		self.timeLabel = QLabel("Alarm Time (hh:mm):")
		self.layout.addWidget(self.timeLabel, 1, 0)
		self.timeBox = KTimeComboBox()
		self.timeBox.setTime(QTime(0, 0) if self.name is None else QTime(time[0], time[1]))
		#self.timeBox.setMaximumWidth(80)
		self.layout.addWidget(self.timeBox, 1, 1, Qt.AlignRight)

		self.msgLabel = QLabel("Alarm message :")
		self.layout.addWidget(self.msgLabel, 2, 0)
		self.alarmMsg = QLineEdit()
		self.alarmMsg.setText('' if self.name is None else msg)
		self.alarmMsg.setMinimumWidth(220)
		self.layout.addWidget(self.alarmMsg, 2, 1)

		self.commandLabel = QLabel("Command :")
		self.layout.addWidget(self.commandLabel, 3, 0)
		self.alarmCmd = QLineEdit()
		self.alarmCmd.setText('' if self.name is None else cmd)
		self.alarmCmd.setMinimumWidth(220)
		self.layout.addWidget(self.alarmCmd, 3, 1)

		self.pathButton = QPushButton("Path")
		self.pathButton.clicked.connect(self.searchPath)
		self.layout.addWidget(self.pathButton, 4, 0)
		self.soundPath = QLineEdit('' if path is None else path)
		self.layout.addWidget(self.soundPath, 4, 1)

		self.playButton = QPushButton("Play")
		self.playButton.clicked.connect(self.playPath)
		self.layout.addWidget(self.playButton, 5, 0)

		self.okButton = QPushButton('&Ok')
		self.okButton.clicked.connect(self.ok)
		self.layout.addWidget(self.okButton, 5, 1, Qt.AlignLeft)

		self.cancelButton = QPushButton('&Cancel')
		self.cancelButton.clicked.connect(self.cancel)
		self.layout.addWidget(self.cancelButton, 5, 1, Qt.AlignRight)

		self.setLayout(self.layout)

	def searchPath(self):
		fileName = QFileDialog.getOpenFileName(self, 'Path_to_sound', '~', "Sound (*.wav *.ogg)")
		name_ = fileName.toLocal8Bit().data()
		if not stat.S_ISLNK(os.lstat(name_).st_mode) and os.access(name_, os.R_OK) :
			self.soundPath.setText(fileName)
		else :
			showHelp = QMessageBox.information(self, 'Error', "Bad path", buttons = QMessageBox.Ok)

	def enablePlay(self): self.playButton.setEnabled(True)
	def disablePlay(self): self.playButton.setEnabled(False)

	def playPath(self):
		path = self.soundPath.text()
		#print path
		self.play = QProcess()
		self.play.started.connect(self.disablePlay)
		self.play.finished.connect(self.enablePlay)
		self.play.start('/usr/bin/play', QStringList()<<path)
		if self.play.waitForStarted() :
			self.runned = True
			#print self.t.state()
		else :
			self.playButton.setEnabled(True)

	def ok(self):
		if self.name is not None :
			items = self.prnt.alarmList.findItems(self.name, Qt.MatchExactly)
			if len(items) :
				item = items[0]
				self.itemEnable = item.checkState()
				self.prnt.alarmList.takeItem(self.prnt.alarmList.row(item))
				self.Settings.remove(self.name)
		if not self.nameAlarm.text().isEmpty() :
			self.Settings.beginGroup(self.nameAlarm.text())
			self.Settings.setValue('Message', self.alarmMsg.text())
			self.Settings.setValue('Command', self.alarmCmd.text())
			_time = self.timeBox.time()
			hours = '0' + str(_time.hour()) if _time.hour() < 10 else str(_time.hour())
			minutes = '0' + str(_time.minute()) if _time.minute() < 10 else str(_time.minute())
			time = hours + ':' + minutes
			self.Settings.setValue('Time', time)
			self.Settings.setValue('Sound', self.soundPath.text())
			self.Settings.setValue('Enable', str(self.itemEnable))
			self.Settings.endGroup()
			item = QListWidgetItem(self.nameAlarm.text())
			item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
			item.setCheckState(self.itemEnable)
			self.prnt.alarmList.addItem(item)
		self.done(0)

	def cancel(self):
		self.done(0)

	def closeEvent(self, event):
		event.ignore()
		self.done(0)
