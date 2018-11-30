from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import GetCreds

# If modifying these scopes, delete the file token.json.
SCOPES = 'Q_Q0vu_RxCN87J86EIezDO8m'#'https://www.googleapis.com/auth/calendar.readonly'

def main():
    service = GetCreds.getCalendarService(SCOPES)
    # Call the Calendar API
    print('Getting the upcoming 10 events')
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='vtm77ugv7jqrdmk4fos7aa5dg4@group.calendar.google.com', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

if __name__ == '__main__':
    main()
