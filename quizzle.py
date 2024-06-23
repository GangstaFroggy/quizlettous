from tkinter import *
from tkinter import ttk
from random import *
from tkinter import font
import os
import json

#Transfer term and definition to result label and create term and defintion object
def transfer():
    global pairList, termArr, termTxt, defTxt
    term : str = termTxt.get("1.0", "end").strip()
    define : str = defTxt.get("1.0", "end").strip()
    pairList.insert("end", term + " : " + define)
    pairList.config(width=0)
    termArr.append([term, define])

#delete currently selected term and definition pair in new studyset
def deletePair():
    global pairList, termArr
    selection = pairList.curselection()
    for i in reversed(selection):
        pairList.delete(i)
        termArr.pop(i)
    pairList.config(width=0)

#delete currently selected study set(s)
def deleteSet():
    global setsList, studysets, studysetArr, studysetMenu
    selection = setsList.curselection()
    for i in reversed(selection):
        key = setsList.get(i)
        setsList.delete(i)
        studysets.pop(key)
    with open("studysets.json", "w") as file:
        json.dump(studysets, file)
    studysetArr = list(studysets.keys())
    studysetMenu.set_menu("Select a Study Set", *studysetArr)
    setsList.config(width=0)

#load currently selected study set(s) on to the list of terms
def extractSet():
    global setsList, studysets, termArr, pairList
    selection = setsList.curselection()
    for i in selection:
        key = setsList.get(i)
        for termDef in studysets[key]:
            pairList.insert("end", termDef[0] + " : " + termDef[1])
            termArr.append([termDef[0], termDef[1]])
    pairList.config(width=0)
    deleteSet()


#save new studyset to studysets with name as key
def saveSet():
    global nameSetEntry, studysets, setsList, pairList, termArr, termTxt, defTxt, studysetArr, studysetMenu
    nameSet = nameSetEntry.get()
    if not nameSet in studysets and not nameSet == "Select a Study Set" and not nameSet.strip() == "" and not pairList.size() == 0:
        setsList.insert("end", nameSet)
        studysets[nameSet] = termArr
        with open("studysets.json", "w") as file:
            json.dump(studysets, file)
        pairList.delete(0, pairList.size()-1)
        termTxt.delete("1.0", "end")
        defTxt.delete("1.0", "end")
        termArr=[]
    studysetArr = list(studysets.keys())
    studysetMenu.set_menu("Select a Study Set", *studysetArr)
    studysetMenu.config()

#initialize setsList to include the saved data from previous runs that is stored in a json file
def initSets():
    global studysets, setsList, studysetArr, studysetMenu
    for key in studysets.keys():
        setsList.insert("end", str(key))
    studysetArr = list(studysets.keys())
    studysetMenu.set_menu("Select a Study Set", *studysetArr)
    studysetMenu.config()

#Generates a question from term in studyset and randomly generates the multiple choices
def generateQuestion():
    global questionFrm, studysets, selectOpt, tab2
    selectKey = selectOpt.get()
    if not selectKey == "Select a Study Set":
        questionFrm.destroy()
        questionFrm = Frame(master=tab2)
        questionFrm.pack(expand=True, side='left')
        studyset = studysets[selectKey]
        randnum = randint(0, len(studyset)-1)
        termDef = studyset[randnum]
        qstinLbl = Label(master=questionFrm, text=termDef[0], font=("Georgia", 16))
        qstinLbl.pack()
        answerFrm = Frame(master=questionFrm)
        answerFrm.pack()

        #Generate all choices for question
        choices = []
        randidx = randint(0, min(len(studyset), 4) - 1)
        for i in range(min(len(studyset), 4)):
            #if its correct choice index set answer button to correct 
            if i == randidx:
                answerBtn = Choice(parent=answerFrm, definition=termDef[1], isCorrect=True, choices=choices)
                answerBtn.grid(row=int(i/2), col=i%2)
                choices.append(answerBtn)
            #if it's an incorrect choice set answer button to incorrect and make sure there are no duplicate choices
            else:
                answerBtn = Choice(parent=answerFrm, definition=studyset[randint(0, len(studyset))-1][1], isCorrect=False, choices=choices)
                while(answerBtn in choices or answerBtn.definition == termDef[1]):
                    answerBtn.setDef(studyset[randint(0, len(studyset))-1][1])
                answerBtn.grid(row=int(i/2), col=i%2)
                choices.append(answerBtn)
        nextBtn = Button(master=questionFrm, text="New Question", font = ("Georgia", 12), command=generateQuestion)
        nextBtn.pack()

#class for choice in studying section
#if wrong choice will turn red and if right choice will turn green
class Choice:
    def __init__(self, parent : Frame, isCorrect : bool, definition : str, choices : list) -> None:
        self.isCorrect = isCorrect
        self.btn = Button(master=parent, text=definition, command=self.onClick, font=("Georgia", 14))
        self.definition = definition
        self.choices = choices
    
    def __eq__(self, other):
        if isinstance(other, Choice):
            return other.definition == self.definition
        return False
    
    def onClick(self):
        for choice in self.choices:
            if choice.isCorrect:
                choice.btn.config(background="green2", activebackground="green3")
            else:
                choice.btn.config(background="red2", activebackground="red3")
    
    def setDef(self, definition : str):
        self.definition = definition
        self.btn.config(text=definition)
    
    def grid(self, row : int, col : int):
        self.btn.grid(row=row, column=col, sticky=NSEW)

studysets : dict = {}
if os.path.exists('studysets.json'):
    with open("studysets.json", "r") as file:
        studysets = json.load(file)
else:
    with open("studysets.json", "w") as file:
        json.dump(studysets, file)

window = Tk()
notebook = ttk.Notebook(window)
notebook.pack(expand=1, fill=BOTH)

#Creating study set and editing study set tab
tab1 = Frame(master=notebook)
notebook.add(tab1, text="Create/Edit")

#Left side term and definition creation
LeftFrame = Frame(master = tab1)

termLbl = Label(master = LeftFrame, text = "Term", justify = 'center', anchor='w', font=("Georgia", 12))
termTxt = Text(master = LeftFrame, width=0, height=7, font=("Georgia", 10))

defLbl = Label(master = LeftFrame, text = "Definition", justify = 'center', anchor = 'w', font=("Georgia", 12))
defTxt = Text(master = LeftFrame, width=0, height=7, font=("Georgia", 10))

transferBtn = Button(master = LeftFrame, text="Add Term and Definition->", command=transfer, font=("Georgia", 12))

setsFrm = Frame(master=LeftFrame)

setListFrm = Frame(master=setsFrm)
setsList = Listbox(master=setListFrm, selectmode=MULTIPLE, font=("Georgia", 10))
setsDeleteBtn = Button(master=setListFrm, command=deleteSet, font=("Georgia", 16), text="delete")

setSaveFrm = Frame(master=setsFrm)
extractSetBtn = Button(master=setSaveFrm, command = extractSet, text="Extract Study Set->", font=("Georgia", 12))
nameSetLbl = Label(master=setSaveFrm, text="Study Set Name", font=("Georgia", 12))
nameSetEntry = Entry(master=setSaveFrm, font=("Georgia", 10))
saveSetBtn = Button(master=setSaveFrm, command=saveSet, text="<-Add Study Set", font=("Georgia", 12))

#packing of contents in left frame
LeftFrame.pack(fill = 'both', expand = True, side='left')

termLbl.pack(fill='x')
termTxt.pack(fill='x')

defLbl.pack(fill='x')
defTxt.pack(fill='x')

transferBtn.pack(anchor='e')

#packing of contents in bottom left Frame
setsFrm.pack(fill='both', expand=True, side='bottom')

setListFrm.pack(side='left', fill='both', expand=True)
setsList.pack(fill='both', expand=True)
setsDeleteBtn.pack()

setSaveFrm.pack(side='left', expand=True)
extractSetBtn.pack()
nameSetLbl.pack()
nameSetEntry.pack()
saveSetBtn.pack()

#Right side new studyset display and manipulation
termArr = []
RightFrame = Frame(master = tab1)

pairList : Listbox = Listbox(master=RightFrame, font=("Georgia", 10), selectmode = MULTIPLE)
deleteBtn : Button = Button(master=RightFrame, font=("Georgia", 16), text="delete", command=deletePair)

#packing of contents in left Frame
RightFrame.pack(fill = 'both', side='left', expand=True)

pairList.pack(fill='both', expand=True)
deleteBtn.pack()

#multiple choice quiz style study tab
tab2 = Frame(master=notebook)
notebook.add(tab2, text="Study")

#question settings portion on left side
studysetArr = []
selectOpt = StringVar(master=tab2)
selectOpt.set("Select a Study Set")

settingFrm = Frame(master = tab2)
style = ttk.Style()
style.configure('.', font=('Georgia', 10))
studysetMenu = ttk.OptionMenu(master = settingFrm, variable = selectOpt, *studysetArr)

questionFrm = Frame(master=tab2)
generateBtn = Button(master = questionFrm, text="Generate Question", font=("Georgia", 20), command=generateQuestion)

settingFrm.pack(side="left", expand=True)
studysetMenu.pack(side="top")

questionFrm.pack(side="left", expand=True)
generateBtn.pack(expand=True)

initSets()

window.mainloop()
