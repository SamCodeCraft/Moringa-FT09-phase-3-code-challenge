from database.connection import get_connection

class Magazine:
    def __init__(self, name, category):
        self._name = name
        self._category = category
        self._id = self._create_magazine()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    def _create_magazine(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self._name, self._category))
            return cursor.lastrowid

    # Object Relationship Methods and Properties

    # 1. Retrieve all articles published in this magazine using SQL JOIN
    def articles(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT a.* FROM articles a
                JOIN magazines m ON a.magazine_id = m.id
                WHERE m.id = ?
            ''', (self._id,))
            return cursor.fetchall()

    # 2. Retrieve all authors who have written articles for this magazine using SQL JOIN
    def contributors(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DISTINCT au.* FROM authors au
                JOIN articles a ON au.id = a.author_id
                WHERE a.magazine_id = ?
            ''', (self._id,))
            return cursor.fetchall()

    # Aggregate and Association Methods

    # 3. Retrieve a list of article titles published in this magazine
    def article_titles(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT a.title FROM articles a
                JOIN magazines m ON a.magazine_id = m.id
                WHERE m.id = ?
            ''', (self._id,))
            titles = cursor.fetchall()
            return [title[0] for title in titles] if titles else None

    # 4. Retrieving authors who have written more than 2 articles for this magazine
    def contributing_authors(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT au.*, COUNT(a.id) as article_count FROM authors au
                JOIN articles a ON au.id = a.author_id
                WHERE a.magazine_id = ?
                GROUP BY au.id
                HAVING article_count > 2
            ''', (self._id,))
            authors = cursor.fetchall()
            return [author for author in authors] if authors else None
