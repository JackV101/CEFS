# Dynamic import of Tkinter
# It has a different name in python 2.7 than python 3
# This will import the correct module depending on the version
try:
	from tkinter import *
except ImportError:
	from Tkinter import *
import time
import tkcalendar
import tkSimpleDialog
# New Config Manager for handling our settings by using ini files
import ConfigManager

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
		self.x = x
		self.y = y
		self.show()
		return self.popupMenu
	
	def show(self):
		self.popupMenu.grid(row=self.y,column=self.x)
	
	def hide(self):
		self.popupMenu.grid_remove()
	
	def see(self,value):
		if self.state != value:
			schoolC.op.set(schoolTitle)
			sportC.op.set(sportTitle)
		self.state = value
		if(self.seq is studentTypes):
			if(self.state == typeTitle):
				schoolC.seq = [""]
				sportC.seq = [""]
			else:
				schoolC.seq = ConfigManager.getProperty(ConfigManager.getTypes()[self.state],"schools", True)
				sportC.seq = ConfigManager.getProperty(ConfigManager.getTypes()[self.state],"sports", True)
			schoolC.updateList()
			sportC.updateList()

	def updateList(self):
		menu = self.popupMenu['menu']
		# Clear the menu.
		menu.delete(0, 'end')
		for name in self.seq:
			# Add menu items.
			menu.add_command(label=name, command=lambda name=name: self.op.set(name))

class CalendarDialog(tkSimpleDialog.Dialog):
    """Dialog box that displays a calendar and returns the selected date"""
    def body(self, master):
        self.calendar = tkcalendar.Calendar(master)
        self.calendar.pack()

    def apply(self):
        self.result = self.calendar.selection_get()

def onclick():
    cd = CalendarDialog(window)
    date.config(text="Date: "+cd.result.strftime("%Y-%m-%d"))
    print cd.result

#Create Window
window = Tk()
window.title("Testing")
window.geometry("400x400")

#Button
Exit = Button(window,text="Exit",command=exitMe)
Exit.grid(row=10,column=1)

#Drop Down Variables

studentTypes = sorted(ConfigManager.getTypes().keys())

typeTitle = "Type"
schoolTitle = "School"
sportTitle = "Sport"

typeC = popup(studentTypes,typeTitle,1,1)
sportC = popup([""],sportTitle,2,1)
schoolC = popup([""],schoolTitle,3,1)

date = Button(window, text="Date", command=onclick)
date.grid(row=1,column=4)

window.mainloop()
