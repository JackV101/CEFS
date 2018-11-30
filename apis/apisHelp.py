from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
from time import localtime, gmtime
from calendar import timegm

SCOPES = "https://www.googleapis.com/auth/calendar.events https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/spreadsheets.readonly"

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

def createEvent(summary,start,end,service,description = "",location = '',clid = 'vtm77ugv7jqrdmk4fos7aa5dg4@group.calendar.google.com'):
    # Add time zone offset if it is missing
	if len(start) == 19:
		start += getTimeZoneOffset()
	if len(end) == 19:
		end += getTimeZoneOffset()
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
	print(start)
	print(end)
	event = service.events().insert(calendarId='primary', body=event).execute()
	print('Event created: ' + event.get('htmlLink'))
	return event

def getTimeZoneOffset():
	"""Get current time zone offset.
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