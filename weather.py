# -*- coding: utf-8 -*-
import argparse
import locations
import forecast
def getWeather(args):
	locationConfig = locations.Locations()
	location = locationConfig.get(args.location)
	if location is None:
		print "that location doesn't exist in my database. Please add it first."
	else:
		print "Weather for ", args.location
		forecast.start(location.get('lat'), location.get('lng'), args.forecast)


def add(args):
	locationConfig = locations.Locations()
	locationConfig.addLocation(args.alias, args.lat, args.lng)
	locationConfig.close()
	print "location", args.alias, "was added successfully."

def remove(args):
	locationConfig = locations.Locations()
	if locationConfig.removeLocation(args.alias):
		print "location", args.alias, "was removed successfully."
	else:
		print "uh oh, that location couldn't be removed."
	locationConfig.close()


parser = argparse.ArgumentParser(description='get the current weather')

subparsers = parser.add_subparsers()

parser_at = subparsers.add_parser('at', help='Type the location alias for where you want the weather followed by any of hourly, daily, currently')

parser_at.add_argument('location',
	help='The location\'s alias, for example home.')
parser_at.add_argument('forecast',
	choices=['c','h','d', 'hourly', 'daily', 'currently'],
		nargs='?',
	default="c",
	help='Time interval, type h for hourly, c for current, d for daily. (Default: Current)')

parser_at.set_defaults(func=getWeather)
parser_add = subparsers.add_parser('add', help='Type your location in the form alias lat long')
parser_add.add_argument('alias',
	help="A name for the location that you use to get weather. i.e. work, home, grandmas_house, and this shouldn't have spaces.")
parser_add.add_argument('lat',
	help='The laditude for the location. This should be a number.')
parser_add.add_argument('lng',
	help='The longitude for the location. This should be a number.')
parser_add.set_defaults(func=add)

parser_remove = subparsers.add_parser('remove', help='Type the location alias you would like to remove in the form alias ')
parser_remove.add_argument('alias',
	help="A name for the location that you use to get weather. i.e. work, home, grandmas_house, and this shouldn't have spaces.")
parser_remove.set_defaults(func=remove)
args=parser.parse_args()
args.func(args)


#lat = 40.014986
#lng = -105.270546

#user_input(forecast,args.type)




