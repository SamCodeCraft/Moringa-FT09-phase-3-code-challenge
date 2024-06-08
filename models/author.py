from database.connection import get_connection

class Author:
    def __init__(self, name):
        self._name = name
        self._id = self._create_author()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def _create_author(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self._name,))
            return cursor.lastrowid

    # Object Relationship Methods and Properties

    # 1. Retrieving all articles written by this author using SQL JOIN
    def articles(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT a.* FROM articles a
                JOIN authors au ON a.author_id = au.id
                WHERE au.id = ?
            ''', (self._id,))
            return cursor.fetchall()

    # 2. Retrieving all magazines where the author has written articles using SQL JOIN
    def magazines(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DISTINCT m.* FROM magazines m
                JOIN articles a ON a.magazine_id = m.id
                WHERE a.author_id = ?
            ''', (self._id,))
            return cursor.fetchall()
