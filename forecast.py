import datetime
import forecastio
import textwrap
import webbrowser

def makeForecast(forecast, item):
	try:
		for i in forecast.alerts():
			print "{:^80}".format(i.title)
			print "would you like to know more? (Y/N)"
			choice=getInput("y","n")
			if choice=='y':
				print "displaying warning in web browser."
				webbrowser.open(i.uri)
				print "done. press enter to continue."
				getInput("")
	except NameError:
		pass
	if item=='c' or item=='currently':
		current=forecast.currently()
		print "It is currently", current.summary, "and", int(current.temperature), "degrees f"
		day=forecast.daily()
		today=day.data[0]
		print today.summary
		print "there is a {0:.0%} chance of precipitation.".format(today.precipProbability)
		highTime= datetime.datetime.fromtimestamp(today.temperatureMaxTime)
		print "daily high", today.temperatureMax, "at", "{}:{}".format(highTime.hour, highTime.minute)
		lowTime=datetime.datetime.fromtimestamp(today.temperatureMinTime)
		print "daily low", today.temperatureMin, "at", "{}:{}".format(lowTime.hour, lowTime.minute)
		print "It is", windy(today.windSpeed)+",", "the wind speed is ", today.windSpeed, "mph"
		
	elif item== 'h' or item == 'hourly':
		hourly=forecast.hourly()
		hourData=[(i.time.hour, i.temperature, i.precipProbability) for i in hourly.data]
		i=hourData[0][0]
		lastIndex=1
		while lastIndex<len(hourData):
			if hourData[lastIndex][0] == i:
				break
			lastIndex+=1
		print "time\tTemperature\tprecipitation"
		for i in range(lastIndex+1):
			cur=hourData[i]
			print "{0}:00\t{1} F\t{2:.0%}".format(cur[0],int(cur[1]), cur[2])
	elif item == 'd' or item == "daily":
		daily = forecast.daily()
		W_DAYS = ['Monday', 'Tuesday', 'Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday']
		for i in daily.data:
			formatter={}
			try:
				formatter['weekday'] = W_DAYS[i.time.weekday()]
				tmxt = datetime.datetime.fromtimestamp(i.temperatureMaxTime)
				tmnt = datetime.datetime.fromtimestamp(i.temperatureMinTime)
				temperatureMaxTime = "{:02}:{:02}".format(tmxt.hour, tmxt.minute)
				temperatureMinTime = "{:02}:{:02}".format(tmnt.hour, tmnt.minute)
				formatter['temperaturemax']=i.temperatureMax
				formatter['temperaturemaxtime'] = temperatureMaxTime
				formatter['temperaturemin'] = i.temperatureMin
				formatter['temperaturemintime'] = temperatureMinTime
				if i.precipProbability > 0:
					formatter['preciptype']= "chance of "+i.precipType
					formatter['precipprobability'] = "{:.0%}".format(i.precipProbability)
				else:
					formatter['preciptype'] = 'No precipitation is expected '
					formatter['precipprobability'] = ""
				formatter['summary'] = i.summary.replace(u'\u2013','--')
				formatter['wind'] = windy(i.windSpeed)+" Wind speed: "+str(int(i.windSpeed))+" mph "
				print textwrap.fill("{weekday}: {summary} {wind}High: {temperaturemax} degrees at {temperaturemaxtime}. Low: {temperaturemin} Degrees  at {temperaturemintime}. {preciptype}{precipprobability}".format(**formatter))
				print ""
				
			except  NameError as e:
				print e.message
				print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


def getInput(*choices):
	while True:
		a=raw_input()
		if a in choices:
			return a
		else:
			print "bad option, try again."

def windy(speed):
	if speed <= 10:
		return "calm"
	elif speed > 10 and speed <= 15:
		return "breezey"
	elif speed > 15 and speed <= 20:
		return "quite breezey"
	elif speed > 20 and speed <= 30:
		return "windy"
	elif speed > 30 and speed <= 40:
		return "quite windy"
	elif speed > 40 and speed <= 75:
		return "extremely windy"
	else:
		return "a hurricane forced wind."
		pass

def start(lat, lng, item):
	api_key = open("apikey").read(300)
	forecast = forecastio.load_forecast(api_key, lat, lng)
	makeForecast(forecast, item)
