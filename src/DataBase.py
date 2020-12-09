import sqlite3
try:
    from src.Story import Story
except:
    from Story import Story
import os

class DataBase:
    # Your Todays Work is to Remove the year, month args from consructor of DataBase class and Merge all Month data in on one Database
    # and then you can arrange the data in any style [by datetime.datetime.now()]
    # [NOTE] : [All Upper Work is Been Done]
    def __init__(self ,path):
        self.path = path

        self.dbName = "Story.db"

        self.connection = sqlite3.connect(os.path.join(self.path , self.dbName) , detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.connection.cursor()
        self.createDb()

    def createDb(self):
        #self.cursor.execute("DROP TABLE IF EXISTS Story;")
        cmd = "CREATE TABLE IF NOT EXISTS Story (Id INTEGER PRIMARY KEY ,Title TEXT, Data TEXT , DateModified timestamp , DateCreated timestamp);"
        self.cursor.execute(cmd)

    def addStory(self , story):
        #print(type(story.dateCreated))
        #cmd = "INSERT INTO Story VALUES (NULL , '%s', '%s' , '%s' , '%s');"%(story.title ,story.data , story.dateModified , story.dateCreated )
        self.cursor.execute("INSERT INTO Story VALUES(NULL , ? ,? ,? ,?)" , (story.title ,story.data , story.dateModified , story.dateCreated))
        #self.cursor.execute(cmd)
        self.connection.commit()

    def getAll(self):
        cmd = "SELECT * FROM Story;"
        self.cursor.execute(cmd)
        rows = self.cursor.fetchall()
        #print(rows.__len__())
        return [Story(x[1] , x[2] , x[4] ,x[3] , x[0]) for x in rows]

    def getStory(self, id):
        cmd = "SELECT * FROM Story WHERE Id LIKE %d"%id
        self.cursor.execute(cmd)
        row = self.cursor.fetchone()
        if(row==None):
            return None
        return Story(row[1] , row[2] , row[4] , row[3] , row[0])

    def updateStory(self , newStory ):
        cmd = "UPDATE Story SET Id=? , Title=? , Data=? , DateModified=? , DateCreated=? WHERE Id LIKE ?"
        self.cursor.execute(cmd , (newStory.id , newStory.title , newStory.data , newStory.dateModified , newStory.dateCreated , newStory.id))
        print(1234567)
        self.connection.commit()