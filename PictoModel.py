class PictoModel:
    def __init__(self, db):
        self._db = db
        self._cursor = self._db.cursor()
        self._dict_cursor = self._db.cursor(dictionary=True)

    def get_tables(self):
        self._cursor.execute("SHOW TABLES")
        # for row in self._cursor.fetchall():
        #     print(row)
        res = self._cursor.fetchall()
        res = [tbl[0] for tbl in res]
        return res

    def get_table(self, table_name: str):
        query = f"SHOW COLUMNS FROM {table_name}"
        self._dict_cursor.execute(query)

        columns = [row['Field'] for row in self._dict_cursor]

        query = f"SELECT * FROM {table_name}"
        self._cursor.execute(query)
        rows = self._cursor.fetchall()

        return columns, rows
