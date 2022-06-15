import sqlite3
from translator import Interpreter
import time


class ETL:
    """ ETL is used to get parsed data from database.
    It makes translation of foreign texts,
    expands database to fit new data, and loads transformed data back to db

    By default ETL addresses to db "news.db" with table name "news".
    You can change both names with set_db_method

    Use run() method to run ETL script automatically
    """
    def __init__(self, name="news.db", table_name: str = "news",
                 trans_from="summary", trans_to="translation"):
        self.trans_from = trans_from
        self.trans_to = trans_to
        self.name = name
        self.table_name = table_name
        self.db = sqlite3.connect(self.name)
        self.cursor = self.db.cursor()
        self.sqlite_select_query = """SELECT * from news"""
        self.sqlite_select_query_partial = """SELECT id, summary from news"""
        self.dictionary = None

    def set_db_name(self, db_name: str = "news.db", table_name: str = "news"):
        self.name = db_name
        self.table_name = table_name

    def update_db(self, *args):
        for arg in args[0]:
            values = [arg['translation'], arg['id']]
            update_query = f''' UPDATE {self.table_name}
                          SET {self.trans_to} = ? 
                          WHERE id = ?'''
            self.cursor.execute(update_query, values)
            self.db.commit()

    def select_all(self):
        self.cursor.execute(self.sqlite_select_query)
        #self.cursor.execute(self.sqlite_select_query_partial)
        self.records = self.cursor.fetchall()
        self.column_names = [descript[0] for descript in self.cursor.description]
        print("!!!", self.column_names)
        # print(self.records)

    def add_column(self, name: str = 'translation'):
        if self.trans_to not in self.column_names:
            sqlite_add_column = f"""ALTER TABLE news ADD COLUMN {self.trans_to} VARCHAR(200) """
            self.cursor.execute(sqlite_add_column)
            self.db.commit()

    def drop_column(self, name: str = 'translation'):
        sqlite_drop_column = f"""ALTER TABLE news DROP COLUMN {name}"""
        self.cursor.execute(sqlite_drop_column)
        self.db.commit()

    def pack_dict(self):
        body = [summary for (id_, title, link, published, summary, dump)
                in self.records]
        inter = Interpreter()
        body_translate = inter.translate(body)
        self.dictionary = [{'id': int(news_id), 'title': title, 'link': link, 'published': published, 'summary': summary,
                            'translation': body} for (news_id, title, link, published, summary, dump), body
                           in zip(self.records, body_translate)]

    # def pack_dict(self):
    #     body = [summary for (id, summary) in self.records]
    #     inter = Interpreter()
    #     body_translate = inter.translate(body)
    #     self.dictionary = [{'id': int(id), 'summary': summary,
    #                         'translation': body} for (id, summary), body
    #                        in zip(self.records, body_translate)]

    def update(self):
        self.update_db(self.dictionary)

    def print_all(self):
        self.cursor.execute(self.sqlite_select_query)
        print_rows = self.cursor.fetchall()
        print(*print_rows, sep="\n")

    def close(self):
        self.db.close()

    def run(self):
        self.select_all()
        self.add_column()
        self.pack_dict()
        self.update()
        self.print_all()
        self.close()
