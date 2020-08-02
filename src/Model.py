from math import ceil


class Model:
    def __init__(self, db):
        self._db = db
        self._cursor = self._db.cursor()
        self._dict_cursor = self._db.cursor(dictionary=True)
        self._current_table_name = None
        self._PAGE_SIZE = 10
        self._current_page = 0
        self._status_count = None

    def get_tables(self):
        self._cursor.execute("SHOW TABLES")
        res = self._cursor.fetchall()
        res = [tbl[0] for tbl in res]
        return res

    def _count(self):
        query = f"SELECT COUNT(*) FROM {self._current_table_name}"
        self._cursor.execute(query)
        return self._cursor.fetchall()[0][0]

    def get_table(self, table_name: str):
        self._reset_lists()
        if table_name is not None:
            self._current_table_name = table_name
            self._current_page = 0

        query = f"SHOW COLUMNS FROM {self._current_table_name}"
        self._dict_cursor.execute(query)
        for row in self._dict_cursor:
            self._current_columns.append(row['Field'])
            self._current_table_types.append(row['Type'].decode())
            if row['Key'] == 'PRI':
                self._current_table_keys.append(row['Field'])

        count = self._count()

        query = f"SELECT * FROM {self._current_table_name} LIMIT {self._current_page * self._PAGE_SIZE}, {self._PAGE_SIZE}"
        self._cursor.execute(query)
        rows = self._cursor.fetchall()
        for row in rows:
            old = []
            for j in range(len(row)):
                if self._current_columns[j] in self._current_table_keys:
                    old.append(row[j])
            self._current_table_keys_old_vals.append(old)

        self._db.commit()
        print(self._cursor.statement)
        return self._current_columns, rows, (self._current_page > 0), (
                count > (self._current_page + 1) * self._PAGE_SIZE)

    def next_page(self):
        self._current_page += 1

    def prev_page(self):
        self._current_page -= 1

    def update_row(self, row, row_index):
        self._convert_type(row)

        query = f"UPDATE {self._current_table_name} SET "
        for i, col in enumerate(self._current_columns):
            val = f"'{row[i]}'" if isinstance(row[i], str) else str(row[i])
            query += f"{col}={val}, "
        query = query[:-2]
        query += " WHERE "
        for i, old_val in enumerate(self._current_table_keys_old_vals[row_index]):
            query += f"{self._current_table_keys[i]}={old_val} AND "
        query = query[:-5]

        self._cursor.execute(query)
        self._db.commit()
        print(self._cursor.statement)

    def delete_row(self, row_index):
        query = f"DELETE FROM {self._current_table_name} WHERE "
        for i, old_val in enumerate(self._current_table_keys_old_vals[row_index]):
            query += f"{self._current_table_keys[i]}={old_val} AND "
        query = query[:-5]

        self._cursor.execute(query)
        self._db.commit()
        print(self._cursor.statement)

        if self._count() <= self._current_page * self._PAGE_SIZE:
            self.prev_page()


    def insert_row(self, row):
        self._convert_type(row)

        query = f"INSERT INTO {self._current_table_name} VALUES ("
        for i in range(len(row)):
            query += "%s, "
        query = query[:-2] + ")"

        self._cursor.execute(query, row)
        self._db.commit()
        print(self._cursor.statement)

    def get_status_message(self, update_count: bool):
        if self._status_count is None or update_count:
            self._status_count = self._count()
        total_pages = ceil(self._status_count / self._PAGE_SIZE)
        ret = f"{self._current_table_name} table. Page {self._current_page + 1} of {total_pages}. {self._status_count} rows total"
        return ret

    def _convert_type(self, row):
        for i in range(len(self._current_table_types)):
            if self._current_table_types[i].startswith('int'):
                row[i] = None if row[i] == '' else int(row[i])
            else:
                row[i] = str(row[i]) or None

    def _reset_lists(self):
        self._current_columns = []
        self._current_table_types = []
        self._current_table_keys = []
        self._current_table_keys_old_vals = []
