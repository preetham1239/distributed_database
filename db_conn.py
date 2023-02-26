import yaml
from mysql.connector import connect


class DBConnector:
    def __init__(self, db_id):
        self.db_name = None
        self.db_id = db_id
        self.host = None
        self.user = None
        self.password = None
        self.conn = None
        self.cursor = None

    def connect(self):
        # open yaml file
        with open('database.yaml') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            self.host = data[self.db_id]['host']
            self.password = data[self.db_id]['password']
            self.user = data[self.db_id]['username']
            self.db_name = data[self.db_id]['database']
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
