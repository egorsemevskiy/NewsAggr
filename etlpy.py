import sqlite3
from translator import Interpreter
import time


class ETL:
    """ ETL is used to get parsed data from database.
    It makes translation of foreign texts,
    expands database to fit new data, and loads transformed data back to db

    By default ETL addresses to db "n_db.db" with table name "news".
    You can change both names with set_db_method

    Use run() method to run ETL script automatically
    """
    def __init__(self, name="news.db", table_name: str = "news"):
        self.name = name
        self.table_name = table_name
        self.q = Interpreter()
        self.db = sqlite3.connect(self.name)
        self.cursor = self.db.cursor()
        self.sqlite_select_query = """SELECT * from news"""

    def set_db_name(self, db_name: str = "news.db", table_name: str = "news"):
        self.name = db_name
        self.table_name = table_name

    def update_db(self, *args):
        for arg in args[0]:
            _ = [arg['translation'], arg['id']]
            query_ = ''' UPDATE news
                          SET translation = ? 
                          WHERE id = ?'''
            self.cursor.execute(query_, _)
            self.db.commit()

    def select_all(self):
        self.cursor.execute(self.sqlite_select_query)
        self.records = self.cursor.fetchall()
        print(self.records)

    def add_column(self, name: str = 'translation'):
        sqlite_add_column = f"""ALTER TABLE news ADD COLUMN {name} VARCHAR(200) """
        self.cursor.execute(sqlite_add_column)
        self.db.commit()

    def drop_column(self, name: str = 'translation'):
        sqlite_drop_column = f"""ALTER TABLE news DROP COLUMN {name}"""
        self.cursor.execute(sqlite_drop_column)
        self.db.commit()

    def pack_dict(self):
        self.dicty_ = [{'id': int(id_), 'title': title, 'link': link, 'published': published, 'summary': summary,
                        'translation': self.q.translate(summary)} for (id_, title, link, published, summary, dump)
                       in self.records]

    def update(self):
        self.update_db(self.dicty_)

    def print_all(self):
        self.cursor.execute(self.sqlite_select_query)
        a = self.cursor.fetchall()
        print(*a, sep="\n")

    def close(self):
        self.db.close()

    def run(self):
        self.select_all()
        self.pack_dict()
        self.update()
        self.print_all()
        self.close()

if __name__ == '__main__':       
    etl = ETL()
    #etl.add_column()
    etl.run()
