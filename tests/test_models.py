import unittest
from models.author import Author
from models.magazine import Magazine
from models.article import Article
from database.connection import get_db_connection

class TestModels(unittest.TestCase):
    def setUp(self):
        # Initialize database and tables here before each test
        conn = get_db_connection()
        with conn:
            conn.executescript('''
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS magazines (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY,
                author_id INTEGER,
                magazine_id INTEGER,
                title TEXT NOT NULL,
                FOREIGN KEY (author_id) REFERENCES authors (id),
                FOREIGN KEY (magazine_id) REFERENCES magazines (id)
            );
            ''')

    def tearDown(self):
        # Clean up the database after each test
        conn = get_db_connection()
        with conn:
            conn.executescript('''
            DROP TABLE IF EXISTS articles;
            DROP TABLE IF EXISTS magazines;
            DROP TABLE IF EXISTS authors;
            ''')

    def test_author_creation(self):
        author = Author(name="John Doe")
        self.assertIsNotNone(author.id)
        self.assertEqual(author.name, "John Doe")

    def test_magazine_creation(self):
        magazine = Magazine(name="Tech Times", category="Technology")
        self.assertIsNotNone(magazine.id)
        self.assertEqual(magazine.name, "Tech Times")
        self.assertEqual(magazine.category, "Technology")

    def test_article_creation(self):
        author = Author(name="John Doe")
        magazine = Magazine(name="Tech Times", category="Technology")
        article = Article(author, magazine, "AI in 2024")
        self.assertIsNotNone(article.title)
        self.assertEqual(article.title, "AI in 2024")

    def test_author_articles(self):
        author = Author(name="John Doe")
        magazine = Magazine(name="Tech Times", category="Technology")
        article = Article(author, magazine, "AI in 2024")
        self.assertGreaterEqual(len(author.articles()), 1)

    def test_magazine_contributors(self):
        author = Author(name="John Doe")
        magazine = Magazine(name="Tech Times", category="Technology")
        article = Article(author, magazine, "AI in 2024")
        self.assertGreaterEqual(len(magazine.contributors()), 1)

if __name__ == "__main__":
    unittest.main()