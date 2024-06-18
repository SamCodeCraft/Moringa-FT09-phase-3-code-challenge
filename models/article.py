from database.connection import get_db_connection

class Article:
    def __init__(self, title, content, author_id, magazine_id, id=None):
        self._id = id
        self._title = title
        self._content = content
        self._author_id = author_id
        self._magazine_id = magazine_id

    @property
    def title(self):
        return self._title

    # Relationship with Author
    @property
    def author(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                SELECT au.* FROM authors au
                JOIN articles a ON au.id = a.author_id
                WHERE a.id = ?
                ''', (self._id,))
            author_data = cursor.fetchone()
            return author_data[1]

    # Relationship with Magazine
    @property
    def magazine(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                SELECT m.* FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.id = ?
                ''', (self._id,))
            magazine_data = cursor.fetchone()
            return magazine_data[1], magazine_data[2]

article = ("id", "title", "content", "author_id", "magazine_id")
print(article)

   


                
           
