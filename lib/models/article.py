
from lib.db.connection import get_cursor

class Article:
    def __init__(self,name,title,author,magazine):
        self.id = None
        self.name = name
        self.title = title
        self.author = author
        self.magazine = magazine



    @property
    def name(self):
        return self._name
    
    @property
    def id(self):
        return self._id
    
    @property
    def title(self):
        return self.title
    
    @property
    def author(self):
        return self._author
    
    @property
    def magazine(self):
        return self._magazine
    
    
    
    @name.setter
    def name (self, value):
        if isinstance(value,str) and  len(value) > 0:
            self._name = value

        else :
            raise ValueError("Name must be a non-empty string.") 
        
    @title.setter
    def title (self, value):
        if isinstance(value,str) and  len(value) > 0:
            self._title = value

        else :
            raise ValueError("Title must be a non-empty string.") 
    

    def save(self):
        conn,cursor = get_cursor()

        if self._id is None:
            cursor.execute("INSERT INTO articles (name,title,author,magazine) VALUES (?,?,?,?)", (self.name,self.title,self.author,self.magazine))
            self._id = cursor.lastrowid
        else:
            cursor.execute("UPDATE articles SET name = ?,title=?,author=?,magazine=? WHERE id = ?", (self.name,self.title,self.author,self.magazine, self._id))

        conn.commit()
        conn.close()



    def find_by_title(cls,title):
        conn,cursor = get_cursor()
        cursor.execute ("SELECT * FROM articles WHERE title =? " (title))
        row = cursor.fetchone()
        conn.close()
        if row:
            author = cls(row["title"])
            author._id = row["id"]
            return author
        return None
    
    def find_by_name(cls,name):
        conn,cursor = get_cursor()
        cursor.execute ("SELECT * FROM articles WHERE title =? " (name))
        row = cursor.fetchone()
        conn.close()
        if row:
            articles = cls(row["name"])
            articles._id = row["id"]
            return articles
        return None
    

    def __repr__(self):
        return f"Article id={self._id} name='{self.name}'title='{self.title}' author='self.author}' "




        

    


    






