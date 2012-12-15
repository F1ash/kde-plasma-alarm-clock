#  Functions.py
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

from time import localtime, strftime

def getAlarmTimesList(Settings):
	l = []
	for _name in Settings.childGroups() :
		Settings.beginGroup(_name)
		time = str(Settings.value('Time').toString())
		enable = True if Settings.value('Enable', 'False') == 'True' else False
		Settings.endGroup()
		if enable and len(time.split(':'))==2 :
			l.append(time)
	return l

def getAlarmData(Settings, alarmTime):
	sounds = []
	msgs = []
	cmds = []
	for _name in Settings.childGroups() :
		Settings.beginGroup(_name)
		time = str(Settings.value('Time', '').toString())
		if time == alarmTime :
			sounds.append(Settings.value('Sound', '').toString())
			msgs.append(Settings.value('Message', '').toString())
			cmds.append(Settings.value('Command', '').toString())
		Settings.endGroup()
	return sounds, msgs, cmds

def nextAlarmTime(currTime, alarmTimesList):
	if len(alarmTimesList) :
		nextAlarm = max(alarmTimesList)
	else : return None
	outAlarmList = True
	_currHour, _currMin = currTime
	#print alarmTimesList
	for alarm in alarmTimesList :
		_alarmHour, _alarmMin = alarm.split(':')
		if int(_currHour) <= int(_alarmHour) :
			if int(_currMin) < int(_alarmMin) :
				outAlarmList = False
				if alarm < nextAlarm : nextAlarm = alarm
	if outAlarmList : nextAlarm = min(alarmTimesList)
	return nextAlarm

def alarmTime(Settings, alarmTimesList):
	'''strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
				'Thu, 28 Jun 2001 14:17:15 +0000'''
	_currTime = strftime("%H:%M:%S", localtime())
	_currHour, _currMin, _currSec = _currTime.split(':')
	nextAlarm = nextAlarmTime((_currHour, _currMin), alarmTimesList)
	pause = (60 - int(_currSec))*1000 + 10
	currTime = ''.join((_currHour, ':', _currMin))
	#print currTime, 'currTime', pause, nextAlarm
	if currTime in alarmTimesList :
		sounds, msgs, cmds = getAlarmData(Settings, currTime)
		return True, msgs, sounds, cmds, nextAlarm, pause, currTime
	else :
		return False, None, None, None, nextAlarm, pause, currTime
