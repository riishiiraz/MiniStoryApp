from tkinter import *
from tkinter.ttk import Combobox
#from tkinter.ttk import Button as ttkButton
from datetime import datetime
from tkinter.scrolledtext import ScrolledText
try:
    from src.DataBase import DataBase
    from src.Story import Story
except ModuleNotFoundError:
    from DataBase import DataBase
    from Story import Story
    
import os
from tkinter.font import Font


ALL_MONTHS = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

class App:
    def __init__(self, root):
        self.CURRENT_YEAR = datetime.now().year
        self.CURRENT_MONTH = datetime.now().month
        #self.CURRENT_MONTH = 7
        self.root = root
        self.root.minsize(400, 400)
        self.root.geometry("804x487+156+156")
        self.LABEL_FRAME_FONT = Font(family="consolas", size=10, slant='roman', underline=0 , weight = "bold")
        self.LABEL_FRAME_CONFIG = {'font':self.LABEL_FRAME_FONT , 'fg':'tomato'}


        # self.root.bind("<Button-1>" , lambda e:self.root.focus())

        self.initDateSelector()
        self.initFileSaver()
        self.initMainBody()
        self.initDirectory()
        self.db = DataBase(self.dbDir)
        self.setData()

        self.setDataToDateSelector()

        popup = self.MONTH_SELECTION_COMBOBOX.tk.eval("ttk::combobox::PopdownWindow %s"%self.MONTH_SELECTION_COMBOBOX)
        self.MONTH_SELECTION_COMBOBOX.tk.call('%s.f.l' % popup, 'configure', '-font', self.MONTH_SELECTION_COMBOBOX['font'])



    def initDirectory(self):
        self.MD = os.path.split(os.path.abspath(__file__))[0]

        if(not os.path.exists(os.path.join(self.MD , "Database"))):
            os.makedirs(os.path.join(self.MD , "Database"))

        self.dbDir = os.path.join(self.MD , "Database")

    def initDateSelector(self):
        #text = "Select Year And Month"
        self.DATE_SELECTION_FRAME = LabelFrame(self.root, text="" ,**self.LABEL_FRAME_CONFIG)
        self.DATE_SELECTION_FRAME.pack(side="top" , anchor = 'nw' , padx = 5 , pady = 10 ,fill = 'x' )

        self.YEAR_SELECTION_FRAME = LabelFrame(self.DATE_SELECTION_FRAME , text = "Select Year" ,**self.LABEL_FRAME_CONFIG)
        self.YEAR_SELECTION_FRAME.pack(side = 'left' , pady = 2 , padx =8)

        self.MONTH_SELECTION_FRAME = LabelFrame(self.DATE_SELECTION_FRAME, text="Select Month" ,**self.LABEL_FRAME_CONFIG)
        self.MONTH_SELECTION_FRAME.pack(side='left' , pady = 2 , padx = 8 )


        self.YEAR_SELECTION_COMBOBOX  = Combobox(self.YEAR_SELECTION_FRAME)
        self.YEAR_SELECTION_COMBOBOX.config( values = [str(x) for x in range(2010 , self.CURRENT_YEAR+1)] , state = "readonly")
        self.YEAR_SELECTION_COMBOBOX.config(font = 'consolas' ,width = 10)
        self.YEAR_SELECTION_COMBOBOX.pack()
        self.YEAR_SELECTION_COMBOBOX.bind("<<ComboboxSelected>>" , lambda e:self.manageWhenYearChanged())

        self.MONTH_SELECTION_COMBOBOX = Combobox(self.MONTH_SELECTION_FRAME)
        self.MONTH_SELECTION_COMBOBOX.config(values = ["All Months"]+[x for x in ALL_MONTHS.values()] , state = "readonly")
        self.MONTH_SELECTION_COMBOBOX.config(font = "consolas" , width = 10)
        self.MONTH_SELECTION_COMBOBOX.pack(side='right')
        self.MONTH_SELECTION_COMBOBOX.bind("<<ComboboxSelected>>", lambda e: self.manageWhenMonthChanged())

    def setDataToDateSelector(self):
        years=set()
        months = set()
        for x in self.CurData:
            years.add(x.dateCreated.year)
        self.YEAR_SELECTION_COMBOBOX.config(values = [x for x in years])
        print(years)


    def manageWhenYearChanged(self):
        pass

    def manageWhenMonthChanged(self , mode = 0):
        if(self.MONTH_SELECTION_COMBOBOX.get() == self.PRE_MONTH_ON_COMBOBOX and mode!=1):
            print("NO Need")
            return
        self.PRE_MONTH_ON_COMBOBOX = self.MONTH_SELECTION_COMBOBOX.get()
        All_Story = self.db.getAll()
        tempStories = []

        if(self.MONTH_SELECTION_COMBOBOX.get() == "All Months"):
            for story in All_Story:
                if (str(story.dateCreated.year) == self.YEAR_SELECTION_COMBOBOX.get()):
                    tempStories.append(story)
        else:
            for story in All_Story:
                if(str(story.dateCreated.year) == self.YEAR_SELECTION_COMBOBOX.get() and ALL_MONTHS[story.dateCreated.month] == self.MONTH_SELECTION_COMBOBOX.get()):
                    tempStories.append(story)

        print("Total = ",len(tempStories))

        self.CurData = tempStories
        self.LISTBOX.delete(0,END)
        for story in self.CurData:
            self.LISTBOX.insert(END , story.title)
        if (self.MONTH_SELECTION_COMBOBOX.get() == ALL_MONTHS[self.CURRENT_MONTH]):
            self.LISTBOX.insert(END, "Add a Story")
        self.EDITTEXT.delete("1.0",END)
        self.ToggleSaveMenuVisibility(False)





    def initMainBody(self):
        self.MAIN_BODY_FRAME = LabelFrame(self.root ,text = "" ,**self.LABEL_FRAME_CONFIG)
        self.MAIN_BODY_FRAME.pack(fill = 'both',expand=1)

        self.PANED_WINDOW_LIST_BOX = PanedWindow(self.MAIN_BODY_FRAME )
        self.PANED_WINDOW_LIST_BOX.pack( fill = BOTH, expand = 1)

        self.LISTBOX_FRAME = LabelFrame(self.PANED_WINDOW_LIST_BOX  , text = "ListBox" ,**self.LABEL_FRAME_CONFIG)
        self.PANED_WINDOW_LIST_BOX.add(self.LISTBOX_FRAME)

        self.LISTBOX = Listbox(self.LISTBOX_FRAME )
        self.LISTBOX.config(font = "consolas 12")
        self.LISTBOX.pack(expand =1 ,fill='both')
        self.LISTBOX.bind("<Double-1>" , lambda e:self.onListBoxClick())
        #self.LISTBOX.insert(0 , "HEllo")


        self.PANED_WINDOW_EDITTEXT = PanedWindow(self.PANED_WINDOW_LIST_BOX , orient = VERTICAL )
        self.PANED_WINDOW_LIST_BOX.add(self.PANED_WINDOW_EDITTEXT )

        self.EDITTEXT_FRAME = LabelFrame(self.PANED_WINDOW_EDITTEXT , text ="EditText" ,**self.LABEL_FRAME_CONFIG)
        #"DejaVu Sans Mono"
        self.EDITTEXT = ScrolledText(self.EDITTEXT_FRAME ,padx=5,pady=5, font = ("Source code pro","13") , wrap='word')
        self.EDITTEXT.pack(fill = 'both' , expand =1 )
        self.PANED_WINDOW_EDITTEXT.add(self.EDITTEXT_FRAME)

    def setData(self):
        self.YEAR_SELECTION_COMBOBOX.set(self.CURRENT_YEAR)
        self.MONTH_SELECTION_COMBOBOX.set(ALL_MONTHS[self.CURRENT_MONTH])
        self.PRE_MONTH_ON_COMBOBOX = self.MONTH_SELECTION_COMBOBOX.get()
        self.CurData = self.db.getAll()
        self.LastId = self.CurData[-1].id
        self.manageWhenMonthChanged(1)
        #self.LISTBOX.insert(END, "Add a Story")
        #return
        #for x in self.CurData:
        #    self.LISTBOX.insert(END , x.title)


    def onListBoxClick(self):
        self.LISTBOX_CUR_IND = self.LISTBOX.curselection()[0]
        self.LISTBOX_CUR_VAl = self.LISTBOX.get(self.LISTBOX_CUR_IND)
        print(self.LISTBOX_CUR_VAl)


        if(self.LISTBOX_CUR_VAl == self.LISTBOX.get(END) and self.MONTH_SELECTION_COMBOBOX.get() == ALL_MONTHS[self.CURRENT_MONTH]): #End Item Clicked [Adding new Story]
            date = datetime.now()
            #print(type(date))
            new = Story("Story "+self.formatDate(date) , "My Data" , date , date , )
            self.db.addStory(new)
            self.LastId+=1
            self.LISTBOX.insert(self.LISTBOX_CUR_IND , new.title)
            #self.CurData.append(new)
            self.CurData.append(self.db.getStory(self.LastId))
            #self.CurData = self.db.getAll()
            self.LISTBOX.select_clear(END)
            self.LISTBOX.select_set(self.LISTBOX_CUR_IND)
            self.onListBoxClick()

        else:

            self.C_Story = self.CurData[self.LISTBOX_CUR_IND]
            print("Id = ",self.C_Story.id)
            self.EDITTEXT.delete("0.0",END)
            self.EDITTEXT.insert(END , self.C_Story.data)
            self.EDITTEXT.focus_force()
            self.ToggleSaveMenuVisibility(True)
            self.DATE_CREATED_LABEL.config(text = self.formatDate(self.C_Story.dateCreated))
            self.DATE_MODIFIED_LABEL.config(text = self.formatDate(self.C_Story.dateModified))
            self.TITLE_VAR.set(self.C_Story.title)


    def initFileSaver(self):
        self.SEPARATOR = Label(self.DATE_SELECTION_FRAME , text="|" ,font = 'consolas 25' , fg = "#eab")
        self.SEPARATOR.pack(side='left') #separator

        self.DATE_CREATED_FRAME = LabelFrame(self.DATE_SELECTION_FRAME , text = "Date Created" ,**self.LABEL_FRAME_CONFIG)
        self.DATE_CREATED_FRAME.pack(side = 'left' , padx=5)
        self.DATE_CREATED_LABEL = Label(self.DATE_CREATED_FRAME  )
        #self.DATE_CREATED_LABEL.pack()
        #self.DATE_CREATED_LABEL.pack_forget()

        self.DATE_MODIFIED_FRAME = LabelFrame(self.DATE_SELECTION_FRAME , text = "Date Modified" ,**self.LABEL_FRAME_CONFIG)
        self.DATE_MODIFIED_FRAME.pack(side='left' ,padx=5)
        self.DATE_MODIFIED_LABEL = Label(self.DATE_MODIFIED_FRAME)

        self.TITLE_FRAME = LabelFrame(self.DATE_SELECTION_FRAME , text = "Title" ,**self.LABEL_FRAME_CONFIG)
        self.TITLE_FRAME.pack(side='left' ,padx=5)
        self.TITLE_VAR = StringVar(self.root)
        self.TITLE_ENTRY = Entry(self.TITLE_FRAME , textvariable = self.TITLE_VAR)

        self.SAVE_BTN = Button(self.DATE_SELECTION_FRAME , text="Save"  , bd=1 , cursor = "hand2" , bg="#fff000" ,font = 'consolas 14' ,height = 1)
        #self.SAVE_BTN.pack(side = 'left')
        self.SAVE_BTN.config(command = self.Save)

        #self.ToggleSaveMenuVisibility(True)

    def ToggleSaveMenuVisibility(self , flag):
        if(flag == True):
            #self.SEPARATOR.pack(side='left')
            self.DATE_CREATED_LABEL.pack()
            self.DATE_MODIFIED_LABEL.pack()
            self.TITLE_ENTRY.pack()
            self.SAVE_BTN.pack(side='left' ,padx=15)
        elif(flag==False):
            #self.SEPARATOR.pack_forget()
            self.DATE_CREATED_LABEL.pack_forget()
            self.DATE_MODIFIED_LABEL.pack_forget()
            self.TITLE_ENTRY.pack_forget()
            self.SAVE_BTN.pack_forget()

    def Save(self):
        self.C_Story.title = self.TITLE_VAR.get()
        self.C_Story.data = self.EDITTEXT.get('1.0' , END)
        self.C_Story.dateModified = datetime.now()
        self.DATE_MODIFIED_LABEL.config(text = self.formatDate(self.C_Story.dateModified) )

        self.LISTBOX.delete(self.LISTBOX_CUR_IND)
        self.LISTBOX.insert(self.LISTBOX_CUR_IND , self.C_Story.title)

        self.db.updateStory(self.C_Story)

    def formatDate(self , timestamp):
        #return str((timestamp.day))
        return "%d %s %d , %02d:%02d"%(timestamp.day , ALL_MONTHS[timestamp.month] , timestamp.year , timestamp.hour , timestamp.minute)



if __name__ =="__main__":
    root = Tk()
    root.title("Mini Story App")
    app = App(root)
    root.focus_force()
    root.mainloop()



