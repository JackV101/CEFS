from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
from time import localtime, gmtime
from calendar import timegm

SCOPES = "https://www.googleapis.com/auth/calendar.events https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/spreadsheets https://www.googleapis.com/auth/calendar.readonly"

def getCalendarService():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', scope=SCOPES)
        creds = tools.run_flow(flow, store)
    return build('calendar', 'v3', http=creds.authorize(Http()))

def getGmailService():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', scope=SCOPES)
        creds = tools.run_flow(flow, store)
    return build('gmail', 'v1',http=creds.authorize(Http()))

def getSheetsService():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', scope=SCOPES)
        creds = tools.run_flow(flow, store)
    return build('sheets', 'v4', http=creds.authorize(Http()))

def calTest(num,service,clid = 'vtm77ugv7jqrdmk4fos7aa5dg4@group.calendar.google.com'):  
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId=clid, timeMin=now,
                                        maxResults=num, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def createCalendarEvent(summary,date,start_time,end_time,service,description = "",location = '',clid = 'vtm77ugv7jqrdmk4fos7aa5dg4@group.calendar.google.com'):
	return createEvent(summary,date +"T"+start_time,date +"T"+end_time,service,description,location,clid)

def createEvent(summary,start,end,service,description = "",location = '',clid = 'vtm77ugv7jqrdmk4fos7aa5dg4@group.calendar.google.com'):
    
	# Check for access before continueing
	testId = checkCalendarAccess(service, clid)
	if not testId:
		# no calendar with the Id. Check if its a name
		testId = checkCalendarAccess(service, clid, True)
		if type(testId) == type(""):
			#found as name
			clid = testId
		else:
			print("Dont have access to calendar: " + clid)
			return None
	
	start = fixTime(start)
	end = fixTime(end)
	
	event = {
	'summary': summary,
	'location': location,
	'description': description,
	'start': {
		'dateTime':start,
	},
	'end': {
		'dateTime': end,
	},
	}
	event = service.events().insert(calendarId=clid, body=event).execute()
	print('Event created on ' + service.calendars().get(calendarId=clid).execute()['summary'] + ': ' + event.get('htmlLink'))
	return event

def fixTime(time):
	if "-" not in time:
		time = datetime.datetime.today().strftime('%Y-%m-%d')
	if "T" not in time:
		time += "T"
	while len(time[time.index("T"):]) < 9:
		if time[-2:].isdigit():
			time += ":"
		time += "0"
	if len(time) == 19:
		time += getTimeZoneOffset()
	return time

def getTimeZoneOffset():
	""" Get current time zone offset.
	Returns:
		A timezone offset string formated in accordance with RFC 3339.
	"""
	iOffset = timegm(localtime()) - timegm(gmtime())
	iOffset /= 60 # Get the Offset in Minutes
	if(iOffset <= 0):
		sOffset = "-"
		iOffset *= -1 # Multiply by negative one to remove the extra negative. The negative is included in the returned string
	else:
		sOffset = "+"
	iHourOffset = iOffset // 60
	iMinuteOffset = iOffset % 60
	if(iHourOffset < 10):
		sOffset += "0"
	sOffset += str(iHourOffset)
	sOffset += ":"
	if(iMinuteOffset < 10):
		sOffset += "0"
	sOffset += str(iMinuteOffset)
	return sOffset

def checkCalendarAccess(service, calId, is_name=False):
	""" Check if user has access to calendar
	service - calendar service object received with getCalendarService
	calId - string - calendar Id or calendar name to check for access
	is_name - boolean - if true the calId is actually a name not a calender Id
	
	If not calId - Returns true if user has access
	If calId - Returns calId if user has access
	Otherwise - Returns False
	"""
	page_token = None
	while True:
		calendar_list = service.calendarList().list(pageToken=page_token).execute()
		for calendar_list_entry in calendar_list['items']:
			if is_name and calendar_list_entry['summary'] == calId:
				# Return the id of the calendar which matches the requested name and the user has access to
				return calendar_list_entry['id']
			elif not is_name and calendar_list_entry['id'] == calId:
				# The user has access to the requested calendar
				return True
		page_token = calendar_list.get('nextPageToken')
		if not page_token:
			break
	# Could not find the requested calendar in the users calendars
	return False
