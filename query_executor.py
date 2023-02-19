class QueryExecutor:
    def __init__(self, query, db_conn):
        self.query = query
        self.db_conn = db_conn

    def execute(self):
        # execute query
        cursor = self.db_conn.cursor()
        cursor.execute(self.query)
        data = cursor.fetchall()
        return data
