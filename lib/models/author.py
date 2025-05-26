import sqlite3
from lib.db.connection import get_cursor
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

    def save(self):
        conn,cursor = get_cursor()

        if self._id is None:
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            self._id = cursor.lastrowid
        else:
            cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self._id))

        conn.commit()
        conn.close()



    def find_by_name(cls,name):
        conn,cursor = get_cursor()
        cursor.execute ("SELECT * FROM authors WHERE name =? " (name))
        row = cursor.fetchone()
        conn.close()
        if row:
            author = cls(row["name"])
            author._id = row["id"]
            return author
        return None
    
    def articles(self):
        conn,cursor = get_cursor()
        cursor.execute("SELECT * FROM  articles WHERE author_id =?",(self.id,))
        rows= cursor.fetchall
        
        conn.close()
        return rows
    
    def magazines(self):
        conn,cursor =get_cursor()
        cursor.execute(""" SELECT DISTINCT m.* FROM magazines m JOIN articles a ON m.id = a.magazine_id WHERE a.author_id = ? """, (self.id,))
        rows =cursor.fetchall
        conn.close()
        return rows


        
    def __repr__(self):
        return f"<Author id={self._id} name='{self.name}'>"
    


    






