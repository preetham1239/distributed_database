import mysql.connector


class DBConnector:
    def __init__(self, db_name):
        self.db_name = db_name
        self.host = "localhost"
        self.port = 8080
        self.user = "root"
        self.password = "Root123@#"
        self.conn = None

    def connect(self):
        # connect to mysql db
        self.conn = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.db_name
        )
