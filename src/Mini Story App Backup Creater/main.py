import os
import time
import sqlite3 as sql

path = os.path.split(os.path.abspath(__file__))[0]
All = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

class SQL:
    def __init__(self):
        self.dbName = "BackUp_Data ["+time.strftime("%d ")+All[int(time.strftime("%m"))]+time.strftime(" %Y]")
        self.con = sql.connect(os.path.join(path , self.dbName+".db"))
        self.cur = self.con.cursor()
        self.createDB()
        
    def createDB(self):
        cmd = "CREATE TABLE IF NOT EXISTS Data (Year INTEGER , Month TEXT , data TEXT);"
        self.cur.execute(cmd)

    def addData(self , data):
        self.cur.execute( "INSERT INTO Data VALUES(? , ? , ?);" ,(data.year , data.month , data.data))
        self.con.commit()
        

class Data:
    def __init__(self , path):
        self.path = path
        self.initData()
        self.initMonth()
        self.initYear()

    def initData(self):
        f = open(self.path)
        self.data = f.read()
        f.close()

    def initMonth(self):
        self.month = os.path.split(self.path)[1][:3]

    def initYear(self):
        p = os.path.split(os.path.split(self.path)[0])[1]
        if(p=="NP"):
            self.year = 2019
        elif (p=="NP2020"):
            self.year = 2020
        

Months = All.values()
def main(path):
    db = SQL()
    # for 2019
    for x in os.listdir(path):
        if(x[:3] in Months):
            obj = Data(os.path.join(path , x))
            db.addData(obj)

        
main(path = r"C:\Users\ASUS\AppData\Local\Programs\Python\Python37-32\NP")
main(path = r"C:\Users\ASUS\AppData\Local\Programs\Python\Python37-32\NP2020")
