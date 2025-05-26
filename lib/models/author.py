import sqlite3
from lib.db.connection import get_connection
class Author:
    def __init__(self,name):
        self.id = None
        self.name = name



    @property
    def name(self):
        return self._name
    
    @property
    def id(self):
        return self._id
    
    @name.setter
    def name (self, value):
        if isinstance(value,str) and  1 <= len(value) <=15:
            self._name = value

        else :
            raise ValueError("Name must be a  string with up to 15 characters.") 

    def save(self)    :
        

    


    






