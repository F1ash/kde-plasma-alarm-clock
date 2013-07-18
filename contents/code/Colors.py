#  Colors.py
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

class ColorWidget(QWidget):
	def __init__(self, obj = None, parent= None):
		QWidget.__init__(self, parent)

		self.prnt = parent
		self.obj = obj
		self.Settings = obj.config()
		colorNames = QColor().colorNames()

		fontColour = self.Settings.readEntry('fontColour', 'yellow').toString()
		unblinkColour = self.Settings.readEntry('unblinkColour', 'silver').toString()

		self.layout = QVBoxLayout()

		self.fontColourLabel = QLabel("Blink Font Colour:")
		self.layout.addWidget(self.fontColourLabel)
		self.fontColourBox = QComboBox()
		self.fontColourBox.setMaximumWidth(150)
		self.fontColourBox.addItems(colorNames)
		self.fontColourBox.currentIndexChanged["const QString&"].connect(self.blinkLabelStyle)
		self.fontColourBox.setCurrentIndex(self.fontColourBox.findText(fontColour))
		self.layout.addWidget(self.fontColourBox)

		self.unblinkColourLabel = QLabel("Unblink Font Colour:")
		self.layout.addWidget(self.unblinkColourLabel)
		self.unblinkColourBox = QComboBox()
		self.unblinkColourBox.setMaximumWidth(150)
		self.unblinkColourBox.addItems(colorNames)
		self.unblinkColourBox.currentIndexChanged["const QString&"].connect(self.unblinkLabelStyle)
		self.unblinkColourBox.setCurrentIndex(self.unblinkColourBox.findText(unblinkColour))
		self.layout.addWidget(self.unblinkColourBox)

		self.setLayout(self.layout)

	def blinkLabelStyle(self, s):
		self.fontColourLabel.setStyleSheet('QWidget {color : %s ;}' % s)

	def unblinkLabelStyle(self, s):
		self.unblinkColourLabel.setStyleSheet('QWidget {color : %s ;}' % s)

	def refreshSettings(self, parent = None):
		self.Settings.writeEntry('fontColour', self.fontColourBox.currentText())
		self.Settings.writeEntry('unblinkColour', self.unblinkColourBox.currentText())
		self.Settings.sync()

	def eventClose(self, event):
		self.prnt.done(0)
