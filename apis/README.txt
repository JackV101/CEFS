apisHelp.py is the importable script for accessing the calendar and initializing the sheets and email
credentials.json does something, keep it
quickstart.py is a modified quickstart script for reference, it is modified to use your code instead of its own, makes it easier to use
RUNME.py should make a calendar entry at a random time of day in a random day of november for 30 minutes
GetCreds.pyc is for the quickstart to work, it's an older version apisHelp

token.json is not included, if it doesn't create itself when you first connect to the network then I'll send it to you. P.S. DO NOT SHARE this file is a direct connection to downloading anything onto your computer

how to use apisHelp:

get[Calendar/Sheets/Gmail]Service(clsecret) takes clsecret is the client secret from the OAuth2
-this needs to be initialized before anything else will work
-this output should be shaved to a variable

calTest can be ignored

createEvent needs the first 4 and doesn't need the last 3 all arguments are strings
>Summary
-This is the title of the event
>Start
-start time in the format 2010-01-01T14:30:00
-The first part is the date, then T for time then the time in 24 hours with hours,minutes,seconds
>End
-end time, same format as Start
>Service is the output of the getCalendarService()
>description Can be left blank
>location can be left blank
>clid is client id, you can leave this blank, it identifies which calendar is to be identified, the default is the one i've shared with you
