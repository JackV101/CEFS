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
		self.state = value
		if(self.seq is studentTypes):
			if(self.state == typeTitle):
				schoolC.seq = [""]
			elif self.state == "7/8":
				schoolC.seq = schools78
			else:
				schoolC.seq = schools
			schoolC.updateList()
	
	def updateList(self):
		menu = self.popupMenu['menu']
		# Clear the menu.
		menu.delete(0, 'end')
		for name in self.seq:
			# Add menu items.
			menu.add_command(label=name, command=lambda name=name: self.op.set(name))

#Create Window
window = Tk()
window.title("Testing")
window.geometry("400x400")

#Button
Exit = Button(window,text="Exit",command=exitMe)
Exit.grid(row=10,column=10)

#Drop Down Variables
schools = ["Monsignor Doyle CSS","Our Lady of Mt Carmel","Pere-Rene-de-Galinee","Ressurrection CSS","Rockway MC","St. Benedict","St. David CSS","St. Mary's HS","Woodland CHS"]
schools78 = ["Blessed Sacrament","Canadian Martyrs","John Sweeny","Rockway MC","St Anne","St Daniel","St John Paul II","St Kareri Tekawitha"]
studentTypes = ["7/8","IND","JB","JG","RUN","SB","SG","VAR"]

typeTitle = "Type"
schoolTitle = "School"

typeC = popup(studentTypes,typeTitle,1,1)
if typeC.state == typeTitle:
    schoolC = popup([""],schoolTitle,2,1)
elif typeC.state == "7/8":
    schoolC = popup(schools78,schoolTitle,2,1)
else:
    schoolC = popup(schools,schoolTitle,2,1)

window.mainloop()
