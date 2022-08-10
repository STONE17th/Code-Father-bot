import mysql.connector as sqdb


class DataBase():
    def __init__(self, base):
        self.base = base
        self.cur = self.base.cursor()
        # self.create_table('user_list')
        # self.create_table('quest_list')

    def create_table(self, list_select: str):
        match list_select:
            case 'user_list':
                self.base.execute(f'CREATE TABLE IF NOT EXISTS {list_select} (id_user PRIMARY KEY, name, task)')
            case 'quest_list':
                self.base.execute(f'CREATE TABLE IF NOT EXISTS {list_select} (id_quest PRIMARY KEY, task, answer)')
        self.base.commit()

    def get_user(self, list_select: str, *args):
        match list_select:
            case 'user_list':
                self.cur.execute(f'SELECT dis_user_id, name, task FROM user_list WHERE dis_user_id = {args[0]}')
                return [tuple(elem) for elem in self.cur]
            case 'user_task':
                self.cur.execute(f'SELECT task FROM user_list WHERE dis_user_id = {args[0]}')
                return [elem[0] for elem in self.cur]


    def get_quest(self, list_select: str, *args):
        match list_select:
            case 'quest_list':
                self.cur.execute(f'SELECT * FROM quest_list')
                return [tuple(elem) for elem in self.cur]
            case 'quest_id':
                self.cur.execute(f'SELECT quest_id FROM quest_list')
                return [elem[0] for elem in self.cur]
            case 'quest_list_new':
                self.cur.execute(f'SELECT quest_id, task, answer FROM quest_list WHERE task = {args[0]}').fetchall()
            case 'quest_task':
                self.cur.execute(f'SELECT task FROM quest_list WHERE quest_id = {args[0]}')
                return [elem[0] for elem in self.cur]
            case 'quest_answer':
                self.cur.execute(f'SELECT answer FROM quest_list WHERE quest_id = {args[0]}')
                return [elem for elem in self.cur][0]


    def add_item(self, new_item, list_select: str):
        match list_select:
            case 'user_list':
                self.cur.execute(f'INSERT INTO {list_select} (dis_user_id, name, task) VALUES (%s, %s, %s)', new_item)
            case 'quest_list':
                self.cur.execute(f'INSERT INTO {list_select} (task, answer) VALUES (?, ?)', new_item)
        self.base.commit()

    def update_item(self, task, user_id, list_select: str):
        match list_select:
            case 'user_list':
                self.cur.execute(f'UPDATE {list_select} SET task = {task} WHERE id_user = {user_id}')
        self.base.commit()

    def delete_item(self, id, list_select: str):
        match list_select:
            case 'user_list':
                self.cur.execute(f'DELETE FROM {list_select} WHERE id_user = {id}')
            case 'quest_list':
                self.cur.execute(f'DELETE FROM {list_select} WHERE id_quest = {id}')
        self.base.commit()