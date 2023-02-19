from mysql.connector import connect, Error


class DBConnector:
    def __init__(self, db_name):
        self.db_name = db_name
        self.host = "localhost"
        self.user = "root"
        self.password = "Root123@#"
        self.conn = None
        self.cursor = None

    def connect(self):
        # connect to mysql db
        self.conn = connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db_name
        )

        # create cursor
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def execute(self, query):
        print("Executing query: ", query)
        cursor = self.cursor
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    def commit(self):
        self.conn.commit()
