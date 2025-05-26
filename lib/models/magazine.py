import sqlite3
from lib.db.connection import get_cursor
class Magazine:
    def __init__(self,name,category):
        self.id = None
        self.name = name
        self.category =category



    @property
    def name(self):
        return self._name
    
    @property
    def id(self):
        return self._id
    
    @property
    def category(self):
        return self._category
    
    @name.setter
    def name (self, value):
        if isinstance(value,str) and  1 <= len(value) <=15:
            self._name = value

        else :
            raise ValueError("Name must be a  string with up to 15 characters.") 
        
    @category.setter
    def category (self, value):
        if isinstance(value,str) and  1 <= len(value) <=15:
            self._category = value

        else :
            raise ValueError("Category must be a  string with up to 15 characters.") 

    def save(self):
        conn,cursor = get_cursor()

        if self._id is None:
            cursor.execute("INSERT INTO magazines (name,category) VALUES (?,?)", (self.name,self.category))
            self._id = cursor.lastrowid
        else:
            cursor.execute("UPDATE magazines SET name = ?, category=? WHERE id = ?", (self.name,self.category, self._id))

        conn.commit()
        conn.close()



    @classmethod
    def find_by_category(cls,category):
        conn,cursor = get_cursor()
        cursor.execute("SELECT * FROM magazines WHERE category =?",category)
        row = cursor.fetchone
        conn.close()

        if row :
            magazine =cls(row["name","category"])
            magazine._id =["id"]
            return magazine
        return None


    