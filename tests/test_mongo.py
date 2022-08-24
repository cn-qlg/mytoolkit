import unittest

db_config = {
    "host": "127.0.0.1",
    "port": 27017,
    "db": "test"
}


class TestMongo(unittest.TestCase):
    def test_connect(self):
        from mytoolkit.db.mongo.connection import connect
        connection = connect(**db_config)
        print(connection)
        self.assertIsNotNone(connection)

    def test_get_db_without_connection(self):
        from mytoolkit.db.mongo.connection import get_db
        print(get_db())

    def test_get_db(self):
        from mytoolkit.db.mongo.connection import connect, get_db
        connect(**db_config)
        get_db()


if __name__ == '__main__':
    unittest.main()
