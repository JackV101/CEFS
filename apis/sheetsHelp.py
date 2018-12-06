from re import search
# Dictionary to cache sheets data
# This module stores multiple requests to different spread sheet or ranges
# The results of duplicate requests will be overwritten
__SheetData__ = {}

# fetch data from sheets
# USE getSheetsData to get result
def fetchSheetsData(service, spreadsheetID = '1qEqy6Kzv0SOxZT6f_-mvhOaJKo-MQYFgA5A_1KyayPo', range = 'A2:D'):
	# Fetch from sheets
	result = service.spreadsheets().values().get(spreadsheetId=spreadsheetID, range=range).execute()
	# Store fetch result in dictionary for access later
	__SheetData__[getDictionaryKey(spreadsheetID, range)] = result.get('values', [])

# gets cached result of a query to a sheet and range
# if the result is not cached and service is provided it will be requested from google
# if the result is not cached and service is not provided or is None then None will be returned
# USE fetchSheetsData to refresh the cache for a sheet and range
def getSheetsData(spreadsheetID='1qEqy6Kzv0SOxZT6f_-mvhOaJKo-MQYFgA5A_1KyayPo', range = 'A2:E', service = None):
	cache_key = getDictionaryKey(spreadsheetID, range)
	#If service == None then dont attempt to fetch sheets data
	if service is not None:
		if cache_key not in __SheetData__:
			fetchSheetsData(service, spreadsheetID, range)
	return __SheetData__.get(cache_key, None)

def getDictionaryKey(spreadsheetID, range):
	return str(spreadsheetID)+str(range)

def setProcessedColumn(service, spreadsheetID = '1qEqy6Kzv0SOxZT6f_-mvhOaJKo-MQYFgA5A_1KyayPo', col = "E"):
	if type(col) == type(1):
		colId = col
	else:
		# Convert Column Letter to 0 baised number
		colId = ord(col.upper()) - ord("A")
	print colId
	if service.spreadsheets().developerMetadata().search(spreadsheetId=spreadsheetID, body={"dataFilters":[{"developerMetadataLookup":{"metadataKey":"processed"}}]}).execute():
		request = {
		"requests":{
			"updateDeveloperMetadataRequest": {
				"dataFilters":[{"developerMetadataLookup":{"metadataKey":"processed"}}],
				"developerMetadata": {
					'metadataKey': 'processed',
					'location': {
						'dimensionRange': {
						'sheetId': 0,
						'dimension': 'COLUMNS',
						'startIndex': colId,
						'endIndex': colId + 1
						},
					},
					"visibility": "PROJECT"
				},
				"fields": "location" 
			}
		}
		}
		service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetID, body=request).execute()
	else:
		request = {
		"requests": [
		{
		"createDeveloperMetadata": {
			"developerMetadata": {
				"metadataKey": "processed",
				"location": {
					"dimensionRange": {
						"dimension": "COLUMNS",
						"sheetId": 0,
						"startIndex": colId,
						"endIndex": colId + 1
					}
				},
				"visibility": "PROJECT"
			}
		}
		}
		]
		}
		service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetID, body=request).execute()

def getProcessedColumn(service, spreadsheetID = '1qEqy6Kzv0SOxZT6f_-mvhOaJKo-MQYFgA5A_1KyayPo'):
	responce = service.spreadsheets().developerMetadata().search(spreadsheetId=spreadsheetID, body={"dataFilters":[{"developerMetadataLookup":{"metadataKey":"processed"}}]}).execute()
	return responce["matchedDeveloperMetadata"][0]["developerMetadata"]["location"]["dimensionRange"]["startIndex"]

def setProcessed(service, offset, range, spreadsheetID = '1qEqy6Kzv0SOxZT6f_-mvhOaJKo-MQYFgA5A_1KyayPo'):
	# Get the column Leter for use in A1 notation
	col = chr(ord('A')+ getProcessedColumn(service, spreadsheetID))
	# Do regex search for the numbers in the range
	match = search("[0-9]+", range)
	A1 = ""
	row = None
	if match:
		# calculate the A1 notation for the offset in the range
		row = str(int(match.group()) + offset)
		A1 = col + row
	#make update request to sheets api
	service.spreadsheets().values().update(spreadsheetId=spreadsheetID, range=A1, valueInputOption="USER_ENTERED", body={"values":[["=TRUE"]]}).execute()
	print "Marked Row "+row+" as Processed"