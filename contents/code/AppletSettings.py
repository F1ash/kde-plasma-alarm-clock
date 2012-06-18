# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Blank import Blank

class AppletSettings(QWidget):
	def __init__(self, obj = None, parent = None):
		QWidget.__init__(self, parent)

		self.prnt = parent
		self.Settings = obj.Settings
		self.obj = obj

		self.layout = QGridLayout()

		self.clockEnableLabel = QLabel('Alarm Clock Enable :')
		self.layout.addWidget(self.clockEnableLabel, 0, 0, Qt.AlignLeft)

		self.clockEnable = QCheckBox()
		if self.Settings.value('Alarm Clock Enable', 'True') == 'True' :
			value = Qt.Checked
		else:
			value = Qt.Unchecked
		self.clockEnable.setCheckState(value)
		self.layout.addWidget(self.clockEnable, 0, 0, Qt.AlignRight)

		self.alarmList = QListWidget()
		for _name in self.Settings.childGroups() :
			self.Settings.beginGroup(_name)
			if self.Settings.value('Enable', 'False') == 'True' :
				value = Qt.Checked
			else:
				value = Qt.Unchecked
			self.Settings.endGroup()
			item = QListWidgetItem(_name)
			item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
			item.setCheckState(value)
			self.alarmList.addItem(item)
		self.alarmList.setContextMenuPolicy(Qt.CustomContextMenu)
		self.alarmList.customContextMenuRequested.connect(self.itemContextMenuQuired)

		self.addAlarm = QPushButton('Add')
		self.delAlarm = QPushButton('Del')
		self.addAlarm.clicked.connect(self.addAlarmItem)
		self.delAlarm.clicked.connect(self.delAlarmItem)
		self.layout.addWidget(self.alarmList, 1, 0)
		self.layout.addWidget(self.addAlarm, 2, 0, Qt.AlignLeft)
		self.layout.addWidget(self.delAlarm, 2, 0, Qt.AlignRight)

		self.setLayout(self.layout)

	def addAlarmItem(self):
		_addItem = Blank(self.obj, None, self)
		_addItem.exec_()

	def delAlarmItem(self):
		currItem = self.alarmList.takeItem(self.alarmList.currentRow())
		if currItem is not None : self.Settings.remove(currItem.text())

	def itemContextMenuQuired(self, point):
		item = self.alarmList.itemAt(point)
		if item is not None :
			#print point, 'clicked', QtCore.QString().fromUtf8(item.text())
			Editor  = Blank(self.obj, item.text(), self)
			Editor.move(point)
			Editor.exec_()

	def refreshSettings(self, parent = None):
		for i in xrange(self.alarmList.count()) :
			item = self.alarmList.item(i)
			value = bool(item.checkState())
			self.Settings.beginGroup(item.text())
			self.Settings.setValue('Enable', str(value))
			#print item.text(), value
			self.Settings.endGroup()
		self.Settings.setValue('Alarm Clock Enable', str(self.clockEnable.isChecked()))
		self.Settings.sync()

	def eventClose(self, event):
		self.prnt.done(0)
