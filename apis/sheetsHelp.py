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