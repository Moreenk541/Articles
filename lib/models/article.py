from lib.db.connection import get_connection

class Article:
    def __init__(self, title, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f"<Article {self.id}: {self.title}, Author ID: {self.author_id}, Magazine ID: {self.magazine_id}>"

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        if not (5 <= len(value) <= 50):
            raise ValueError("Title must be between 5 and 50 characters")
        self._title = value

    @property
    def author_id(self):
        return self._author_id

    @author_id.setter
    def author_id(self, value):
        if not isinstance(value, int):
            raise TypeError("author_id must be an integer")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM authors WHERE id = ?", (value,))
        if cursor.fetchone() is None:
            raise ValueError("author_id must reference an existing author in the database")
        conn.close()
        self._author_id = value

    @property
    def magazine_id(self):
        return self._magazine_id

    @magazine_id.setter
    def magazine_id(self, value):
        if not isinstance(value, int):
            raise TypeError("magazine_id must be an integer")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM magazines WHERE id = ?", (value,))
        if cursor.fetchone() is None:
            raise ValueError("magazine_id must reference an existing magazine in the database")
        conn.close()
        self._magazine_id = value

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (self.title, self.author_id, self.magazine_id)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                (self.title, self.author_id, self.magazine_id, self.id)
            )
        conn.commit()
        conn.close()

    @classmethod
    def create(cls, title, author_id, magazine_id):
        article = cls(title, author_id, magazine_id)
        article.save()
        return article

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row["title"], row["author_id"], row["magazine_id"], row["id"])
        return None

    @classmethod
    def find_by_title(cls, title):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row["title"], row["author_id"], row["magazine_id"], row["id"])
        return None

    @classmethod
    def get_all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles")
        rows = cursor.fetchall()
        conn.close()
        return [cls(row["title"], row["author_id"], row["magazine_id"], row["id"]) for row in rows]

    def author(self):
        from lib.models.author import Author
        return Author.find_by_id(self.author_id)

    def magazine(self):
        from lib.models.magazine import Magazine
        return Magazine.find_by_id(self.magazine_id)
