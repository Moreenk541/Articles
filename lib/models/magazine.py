from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f"<Magazine {self.id}: {self.name}, Category: {self.category}>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if not (2 <= len(value) <= 16):
            raise ValueError("Name must be between 2 and 16 characters")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise TypeError("Category must be a string")
        if not (2 <= len(value) <= 16):
            raise ValueError("Category must be between 2 and 16 characters")
        self._category = value

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                "INSERT INTO magazines (name, category) VALUES (?, ?)",
                (self.name, self.category)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                (self.name, self.category, self.id)
            )
        conn.commit()
        conn.close()

    @classmethod
    def create(cls, name, category):
        magazine = cls(name, category)
        magazine.save()
        return magazine

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row["name"], row["category"], row["id"])
        return None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row["name"], row["category"], row["id"])
        return None

    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(row["name"], row["category"], row["id"]) for row in rows]

    @classmethod
    def get_all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines")
        rows = cursor.fetchall()
        conn.close()
        return [cls(row["name"], row["category"], row["id"]) for row in rows]

    def articles(self):
        from lib.models.article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM articles
            WHERE magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(row["title"], row["author_id"], row["magazine_id"], row["id"]) for row in rows]

    def contributors(self):
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT a.* FROM authors a
            JOIN articles art ON a.id = art.author_id
            WHERE art.magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(row["name"], row["id"]) for row in rows]

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT title FROM articles
            WHERE magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [row["title"] for row in rows]

    def contributing_authors(self):
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, COUNT(art.id) AS article_count
            FROM authors a
            JOIN articles art ON a.id = art.author_id
            WHERE art.magazine_id = ?
            GROUP BY a.id
            HAVING article_count > 2
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(row["name"], row["id"]) for row in rows]
