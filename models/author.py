from database.connection import get_db_connection

class Author:
    def __init__(self, name, id=None):
        self._name = name
        self._id = id

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def articles(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT a.* FROM articles a
                JOIN authors au ON a.author_id = au.id
                WHERE au.id = ?
            ''', (self._id,))
            return cursor.fetchall()

    def magazines(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DISTINCT m.* FROM magazines m
                JOIN articles a ON a.magazine_id = m.id
                WHERE a.author_id = ?
            ''', (self._id,))
            return cursor.fetchall()

class Article:
    def __init__(self, title, content, author_id, id=None):
        self._title = title
        self._content = content
        self._author_id = author_id
        self._id = id

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def content(self):
        return self._content

    @property
    def author_id(self):
        return self._author_id

    # Retrieving the author of this article using SQL JOIN
    def author(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT au.* FROM authors au
                JOIN articles a ON a.author_id = au.id
                WHERE a.id = ?
            ''', (self._id,))
            return cursor.fetchone()

    # Retrieving the magazine of this article using SQL JOIN
    def magazine(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT m.* FROM magazines m
                JOIN articles a ON a.magazine_id = m.id
                WHERE a.id = ?
            ''', (self._id,))
            return cursor.fetchone()
