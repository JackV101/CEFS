from ConfigParser import ConfigParser

SETTINGSFILE = "../settings/settings.ini"

__config__ = ConfigParser()
fallback =  not __config__.read(SETTINGSFILE)

def save():
	__config__.write(open(SETTINGSFILE,"w"))

def getProperty(section, property, asList = False):
	if fallback:
		if section.startswith("78"):
			return loadSettingsFromFile("78"+property+".txt")
		elif(self.state == "IND"):
			return loadSettingsFromFile("IND"+property+".txt")
		elif self.state == "RUN":
			return loadSettingsFromFile("RUN"+property+".txt")
		elif self.state == "VAR":
			return loadSettingsFromFile("VAR"+property+".txt")
		else:
			return loadSettingsFromFile(property+".txt")
	if __config__.has_section(section):
		if __config__.has_option(section,property):
			value = __config__.get(section, property)
		elif section != "noSection" and __config__.has_option(section,"parent") and __config__.has_option(__config__.get(section,"parent"),property):
			value = __config__.get(__config__.get(section,"parent"), property)
		else:
			value = None
		if value and "," in value:
			value = list(map(str, value.split(",")))
		elif asList:
			value = [value]
		return value
	return None

def setProperty(section, property, value):
	if type(value) == type(list()):
		value = ",".join(value)
	if not __config__.has_section(section):
		__config__.add_section(section)
	__config__.set(section,property,value)
	save()

def deleteType(section):
	result = __config__.remove_section(section)
	save()
	return result

def getTypes(includeNoSection=False):
	if fallback:
		# For some reason we failed to load our saved settings. Return a default list instead
		return ["78 Girls","78 Boys","78 Individual","Junior Girls","Junior Boys","Senior Girls","Senior Boys","Individual","Running","Varsity"]
	types = {}
	for section in __config__.sections():
		if not includeNoSection and __config__.has_option(section,"noSection"):
			continue
		if __config__.has_option(section,"name"):
			types[__config__.get(section,"name")] = section
		else:
			types[section] = section
	return types