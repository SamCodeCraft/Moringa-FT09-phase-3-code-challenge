from database.connection import get_connection

class Article:
    def __init__(self, author, magazine, title):
        self._author = author
        self._magazine = magazine
        self._title = title
        self._id = self._create_article()

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        # Retrieve author instance from database using SQL JOIN
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT au.* FROM authors au
                JOIN articles a ON au.id = a.author_id
                WHERE a.id = ?
            ''', (self._id,))
            author_data = cursor.fetchone()
            return author_data(author_data[1])  

    @property
    def magazine(self):
        # Retrieve magazine instance from database using SQL JOIN
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT m.* FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.id = ?
            ''', (self._id,))
            magazine_data = cursor.fetchone()
            return magazine_data(magazine_data[1], magazine_data[2])  

    def _create_article(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO articles (author_id, magazine_id, title)
                VALUES (?, ?, ?)
            ''', (self._author.id, self._magazine.id, self._title))
            return cursor.lastrowid
