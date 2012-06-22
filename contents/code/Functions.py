from time import localtime, strftime

def getAlarmTimesList(Settings):
	l = []
	for _name in Settings.childGroups() :
		Settings.beginGroup(_name)
		time = str(Settings.value('Time').toString())
		Settings.endGroup()
		if len(time.split(':'))==2 :
			l.append(time)
	return l

def getAlarmData(Settings, alarmTime):
	sounds = []
	msgs = []
	for _name in Settings.childGroups() :
		Settings.beginGroup(_name)
		time = str(Settings.value('Time', '').toString())
		if time == alarmTime :
			sounds.append(Settings.value('Sound', '').toString())
			msgs.append(Settings.value('Message', '').toString())
		Settings.endGroup()
	return sounds, msgs

def nextAlarmTime(currTime, alarmTimesList):
	nextAlarm = max(alarmTimesList)
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

def getPause(currTime, nextAlarm):
	pause = 60
	_currHour, _currMin = currTime
	_nextAlarmHour, _nextAlarmMin = nextAlarm.split(':')
	#print _currHour, _currMin, ':', _nextAlarmHour, _nextAlarmMin
	if int(_nextAlarmHour) - int(_currHour) in (0, -23) :
		if int(_nextAlarmMin) - int(_currMin) == 1 :
			pause = pause - int(strftime("%S", localtime())) + 1
	return pause*1000

def alarmTime(Settings, alarmTimesList):
	'''strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
				'Thu, 28 Jun 2001 14:17:15 +0000'''
	currTime = strftime("%H:%M", localtime())
	_currHour, _currMin = currTime.split(':')
	nextAlarm = nextAlarmTime((_currHour, _currMin), alarmTimesList)
	pause = getPause((_currHour, _currMin), nextAlarm)
	#print currTime, 'currTime', pause, nextAlarm
	if currTime in alarmTimesList :
		sounds, msgs = getAlarmData(Settings, currTime)
		return True, msgs, sounds, nextAlarm, pause
	else :
		return False, None, None, nextAlarm, pause
