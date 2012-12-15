# -*- coding: utf-8 -*-
#  AppletSettings.py
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

		self.iconShowLabel = QLabel('Icon show :')
		self.layout.addWidget(self.iconShowLabel, 1, 0, Qt.AlignLeft)

		self.iconShow = QCheckBox()
		if self.obj.config().readEntry('Icon Show', 'True') == 'True' :
			value = Qt.Checked
		else:
			value = Qt.Unchecked
		self.iconShow.setCheckState(value)
		self.layout.addWidget(self.iconShow, 1, 0, Qt.AlignRight)

		self.timeShowLabel = QLabel('Time show :')
		self.layout.addWidget(self.timeShowLabel, 2, 0, Qt.AlignLeft)

		self.timeShow = QCheckBox()
		if self.obj.config().readEntry('Time Show', 'True') == 'True' :
			value = Qt.Checked
		else:
			value = Qt.Unchecked
		self.timeShow.setCheckState(value)
		self.layout.addWidget(self.timeShow, 2, 0, Qt.AlignRight)

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

		add = QIcon().fromTheme('list-add')
		self.addAlarm = QPushButton(add, '')
		self.addAlarm.setToolTip('Add to Alarms')
		_del = QIcon().fromTheme('list-remove')
		self.delAlarm = QPushButton(_del, '')
		self.delAlarm.setToolTip('Delete from Alarms')
		self.addAlarm.clicked.connect(self.addAlarmItem)
		self.delAlarm.clicked.connect(self.delAlarmItem)
		self.iconShow.stateChanged.connect(self.iconStateChanged)
		self.timeShow.stateChanged.connect(self.timeStateChanged)
		self.layout.addWidget(self.alarmList, 3, 0)
		self.layout.addWidget(self.addAlarm, 4, 0, Qt.AlignLeft)
		self.layout.addWidget(self.delAlarm, 4, 0, Qt.AlignRight)

		self.setLayout(self.layout)

	def iconStateChanged(self):
		if not self.iconShow.isChecked() and not self.timeShow.isChecked() :
			self.timeShow.setCheckState(Qt.Checked)

	def timeStateChanged(self):
		if not self.iconShow.isChecked() and not self.timeShow.isChecked() :
			self.iconShow.setCheckState(Qt.Checked)

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
		self.obj.config().writeEntry('Icon Show', str(self.iconShow.isChecked()))
		self.obj.config().writeEntry('Time Show', str(self.timeShow.isChecked()))
		self.Settings.sync()

	def eventClose(self, event):
		self.prnt.done(0)
