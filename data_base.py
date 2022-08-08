import sqlite3 as sqdb


class DataBase():
    def __init__(self, path=None):
        self.path = path
        self.base = sqdb.connect(self.path)
        self.cur = self.base.cursor()
        self.create_table()

    def create_table(self):
        self.base.execute('CREATE TABLE IF NOT EXISTS user_list (id_user PRIMARY KEY, name, task)')
        self.base.commit()

    def get_data(self, user_id):
        res = self.cur.execute(f'SELECT id_user, name, task FROM user_list WHERE id_user = {user_id}').fetchall()
        return res

    def add_item(self, new_item):
        self.cur.execute('INSERT INTO user_list (id_user, name, task) VALUES (?, ?, ?)', new_item)
        self.base.commit()

    def update_item(self, task, user_id):
        self.cur.execute(f'UPDATE user_list SET task = {task} WHERE id_user = {user_id}')
        self.base.commit()