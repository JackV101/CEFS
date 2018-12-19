from re import search
# Dictionary to cache sheets data
# This module stores multiple requests to different spread sheet or ranges
# The results of duplicate requests will be overwritten
__SheetData__ = {}

# fetch data from sheets
# USE getSheetsData to get result
def fetchSheetsData(service, spreadsheetID = '1qEqy6Kzv0SOxZT6f_-mvhOaJKo-MQYFgA5A_1KyayPo', range = 'A2:F'):
	# Fetch from sheets
	result = service.spreadsheets().values().get(spreadsheetId=spreadsheetID, range=range).execute()
	# Store fetch result in dictionary for access later
	__SheetData__[getDictionaryKey(spreadsheetID, range)] = result.get('values', [])

# gets cached result of a query to a sheet and range
# if the result is not cached and service is provided it will be requested from google
# if the result is not cached and service is not provided or is None then None will be returned
# USE fetchSheetsData to refresh the cache for a sheet and range
def getSheetsData(spreadsheetID='1qEqy6Kzv0SOxZT6f_-mvhOaJKo-MQYFgA5A_1KyayPo', range = 'A2:F', service = None):
	cache_key = getDictionaryKey(spreadsheetID, range)
	#If service == None then dont attempt to fetch sheets data
	if service is not None:
		if cache_key not in __SheetData__:
			fetchSheetsData(service, spreadsheetID, range)
	return __SheetData__.get(cache_key, None)

def getDictionaryKey(spreadsheetID, range):
	return str(spreadsheetID)+str(range)

def setProcessedColumn(service, spreadsheetID = '1qEqy6Kzv0SOxZT6f_-mvhOaJKo-MQYFgA5A_1KyayPo', col = "F"):
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
	#calculate the A1 notation for the offset in the range
	A1 = getA1FromOffset([getProcessedColumn(service, spreadsheetID),offset],range)
	#make update request to sheets api
	service.spreadsheets().values().update(spreadsheetId=spreadsheetID, range=A1, valueInputOption="USER_ENTERED", body={"values":[["=TRUE"]]}).execute()
	print "Marked Row "+str(getOffsetFromA1(A1)[1])+" as Processed"

#These methods convert between A1 notation and array offset

def getOffsetFromA1(a1_target, origin=None):
	"""
	convert from A1 notation to offsets from specified offset
	
	a1_target - string - point in A1 notation to convert to offsets
	origin - array of size 2 - index 0 being column and index 1 being row. The column can be a letter sequence or number where column A = 1.
	origin - string - range/point in A1 notation to which the offset is relative to
	If origin == None then the origin of A1 is used
	If origin is a range it is parsed and used as offset
	
	return array of size 2 - index 0 being column and index 1 being row. The column can be a letter sequence or number where column A = 1.
	
	"""
	col_start = 0
	row_start = 0
	result = [0,0]
	if origin != None:
		if type(origin) == type([]):
			if len(origin) != 2:
				# invalid origin could not convert
				return None
			if type(origin[0]) == type(""):
				col_start = ord('A')-upper(origin[0])
			elif type(origin[0]) == type(1):
				col_start = origin[0]
			else:
				#invalid origin could not convert
				return None
			if type(origin[1]) != type(1):
				#invalid origin could not convert
				return None
			else:
				row_start = origin[1]
		elif type(origin) == type(""):
			match = search("[A-Z]+", origin)
			if match:
				col_start = ord('A')-ord(match.group().upper())
			match = search("[1-9][0-9]*", origin)
			if match:
				row_start = int(match.group())
		else:
			#invalid origin could not convert
			return None
	if type(a1_target) != type(""):
		#invalid target could not convert
		return None
	match = search("[A-Z]+",a1_target)
	if not match:
		#invalid notation could not convert
		return None
	result[0] = ord(match.group()) - ord("A") - col_start
	match = search("[1-9][0-9]*",a1_target)
	if not match:
		#invalid notation could not convert
		return None
	result[1] = int(match.group())-row_start
	
	return result

def getA1FromOffset(offset, origin=None):
	"""
	convert from offsets from specified offset to A1 notation
	
	offset - array of size 2 - index 0 being column and index 1 being row. The column can be a letter sequence or number where column A = 1.
	origin - array of size 2 - index 0 being column and index 1 being row. The column can be a letter sequence or number where column A = 1.
	origin - string - range/point in A1 notation to which the offset is relative to
	If origin == None then the origin of A1 is used
	If origin is a range it is parsed and used as offset
	
	return string in A1 notation
	
	"""
	col_start = 0
	row_start = 0
	if origin != None:
		if type(origin) == type([]):
			if len(origin) != 2:
				# invalid origin could not convert
				return None
			if type(origin[0]) == type(""):
				col_start = ord('A')-upper(origin[0])
			elif type(origin[0]) == type(1):
				col_start = origin[0]
			else:
				#invalid origin could not convert
				return None
			if type(origin[1]) != type(1):
				#invalid origin could not convert
				return None
			else:
				row_start = origin[1]
		elif type(origin) == type(""):
			match = search("[A-Z]+", origin)
			if match:
				col_start = ord('A')-ord(match.group().upper())
			match = search("[1-9][0-9]*", origin)
			if match:
				row_start = int(match.group())
		else:
			#invalid origin could not convert
			return None
	if type(offset) != type([]):
		#invalid offset could not convert
		return None
	col = chr(ord("A") + offset[0] + col_start)
	row = offset[1] + row_start
	A1 = col + str(row)
	
	return A1