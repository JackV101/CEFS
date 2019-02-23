# Dynamic import of Tkinter
# It has a different name in python 2.7 than python 3
# This will import the correct module depending on the version
try:
	from tkinter import *
except ImportError:
	from Tkinter import *
import time

def exitMe():
    exit()

class popup:

	def __init__(self,s,option,x,y):
		self.seq = s
		self.state = option
		self.display(option,x,y)
		
	def display(self,option,x,y):
		self.op = StringVar(window)
		self.op.set(option)
		self.popupMenu = OptionMenu(window, self.op, *self.seq, command=self.see)
		self.popupMenu.grid(row=y,column=x)
		return self.popupMenu
	
	def see(self,value):
		if self.state != value:
			schoolC.op.set(schoolTitle)
			sportC.op.set(sportTitle)
		self.state = value
		if(self.seq is studentTypes):
			if(self.state == typeTitle):
				schoolC.seq = [""]
				sportC.seq = [""]
			elif self.state == "78":
				schoolC.seq = schools78
				sportC.seq = loadSettingsFromFile("78sports.txt")
			else:
				schoolC.seq = schools
			if(self.state == "IND"):
				sportC.seq = loadSettingsFromFile("INDsports.txt")
			elif self.state == "RUN":
				sportC.seq = loadSettingsFromFile("RUNsports.txt")
			elif self.state == "VAR":
				sportC.seq = loadSettingsFromFile("VARsports.txt")
			elif self.state != "78":
				sportC.seq = loadSettingsFromFile("sports.txt")
			schoolC.updateList()
			sportC.updateList()
	
	def updateList(self):
		menu = self.popupMenu['menu']
		# Clear the menu.
		menu.delete(0, 'end')
		for name in self.seq:
			# Add menu items.
			menu.add_command(label=name, command=lambda name=name: self.op.set(name))

def loadSettingsFromFile(fileName):
	if not fileName.endswith(".txt"):
		fileName += ".txt"
	return list(map(str, open("../settings/"+fileName).read().split("\n")))

#Create Window
window = Tk()
window.title("Testing")
window.geometry("400x400")

#Button
Exit = Button(window,text="Exit",command=exitMe)
Exit.grid(row=10,column=10)

#Drop Down Variables

schools = loadSettingsFromFile("schools.txt")
schools78 = loadSettingsFromFile("78Schools.txt")

studentTypes = loadSettingsFromFile("sportTypes.txt")

typeTitle = "Type"
schoolTitle = "School"
sportTitle = "Sport"

typeC = popup(studentTypes,typeTitle,1,1)

sportC = popup([""],sportTitle,2,1)

if typeC.state == typeTitle:
    schoolC = popup([""],schoolTitle,3,1)
elif typeC.state == "78":
    schoolC = popup(schools78,schoolTitle,3,1)
else:
    schoolC = popup(schools,schoolTitle,3,1)

window.mainloop()
