import apisHelp
import emailHelp
import sheetsHelp

SPREADSHEET_ID = '1qEqy6Kzv0SOxZT6f_-mvhOaJKo-MQYFgA5A_1KyayPo'
RANGE = 'A2:F'

calService = apisHelp.getCalendarService()
mailService = apisHelp.getGmailService()
sheetsService = apisHelp.getSheetsService()

values = sheetsHelp.getSheetsData(SPREADSHEET_ID,RANGE, sheetsService)
processed_column = sheetsHelp.getProcessedColumn(sheetsService, SPREADSHEET_ID)

if not processed_column:
	print "Could not find processed column"
	exit()

if not values:
	print('No data found.')
else:
	for offset,row in enumerate(values):
		if len(row) > processed_column and row[processed_column]:
			print("Already Processed Row "+ str(offset))
			continue
		summary = row[0]
		start = row[1]
		end = row[2]
		email = row[3]
		if len(row) >= 5 and processed_column != 4 and row[4]:
			apisHelp.createEvent(summary,start,end,calService, '', '', row[4])
		else:
			apisHelp.createEvent(summary,start,end,calService)
		#emailHelp.SendMessage(mailService, 'me', emailHelp.CreateMessage(email, "CEFS Email", summary))
		sheetsHelp.setProcessed(sheetsService, offset, RANGE, SPREADSHEET_ID)