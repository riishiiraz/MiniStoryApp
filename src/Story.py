class Story:
    def __init__(self ,title , data , dateCreated , dateModified , id=None):
        self.id = id
        self.title = title
        self.data = data
        self.dateCreated = dateCreated
        self.dateModified = dateModified


    def __repr__(self):
        return "Title : %s\nData : %s\nModified : %s\nCreated : %s\n"%(self.title ,self.data , self.dateModified , self.dateCreated)

