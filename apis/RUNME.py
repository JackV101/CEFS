import apisHelp
import emailHelp
import sheetsHelp

SPREADSHEET_ID = '1qEqy6Kzv0SOxZT6f_-mvhOaJKo-MQYFgA5A_1KyayPo'
RANGE = 'A2:D'

calService = apisHelp.getCalendarService()
mailService = apisHelp.getGmailService()
sheetsService = apisHelp.getSheetsService()

values = sheetsHelp.getSheetsData(SPREADSHEET_ID,RANGE, sheetsService)

if not values:
	print('No data found.')
else:
	for row in values:
		summary = row[0]
		start = row[1]
		end = row[2]
		email = row[3]
		apisHelp.createEvent(summary,start,end,calService)
		emailHelp.SendMessage(mailService, 'me', emailHelp.CreateMessage(email, "CEFS Email", summary))