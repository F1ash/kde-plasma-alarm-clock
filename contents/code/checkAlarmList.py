#  checkAlarmList.py
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

from PyQt4.QtCore import QThread
from Functions import alarmTime

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
		self.prnt.currTime = currTime
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
