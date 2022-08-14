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
                self.base.execute(f'CREATE TABLE IF NOT EXISTS {list_select} (user_id PRIMARY KEY, dis_user_id, name, user_status, task)')
            case 'quest_list':
                self.base.execute(f'CREATE TABLE IF NOT EXISTS {list_select} (quest_id PRIMARY KEY, task, answer)')
        self.base.commit()

    def get_user(self, list_select: str, *args):
        match list_select:
            case 'list':
                self.cur.execute(f'SELECT dis_user_id, name, task FROM user_list WHERE dis_user_id = {args[0]}')
                return [tuple(elem) for elem in self.cur]
            case 'task':
                self.cur.execute(f'SELECT task FROM user_list WHERE dis_user_id = {args[0]}')
                return [elem[0] for elem in self.cur]
            case 'status':
                self.cur.execute(f'SELECT user_status FROM user_list WHERE dis_user_id = {args[0]}')
                return [elem[0] for elem in self.cur]


    def get_quest(self, list_select: str, *args):
        match list_select:
            case 'list':
                self.cur.execute(f'SELECT * FROM quest_list')
                return [tuple(elem) for elem in self.cur]
            case 'id':
                self.cur.execute(f'SELECT quest_id FROM quest_list')
                return [elem[0] for elem in self.cur]
            case 'quest':
                self.cur.execute(f'SELECT quest_id, task, answer FROM quest_list WHERE task = {args[0]}').fetchall()
            case 'task':
                self.cur.execute(f'SELECT task FROM quest_list WHERE quest_id = {args[0]}')
                return [elem[0] for elem in self.cur]
            case 'answer':
                self.cur.execute(f'SELECT answer FROM quest_list WHERE quest_id = {args[0]}')
                return [elem for elem in self.cur][0]
            case 'set_quest':
                self.cur.execute(f'UPDATE user_list SET task = {args[1]} WHERE dis_user_id = {args[0]}')
                return [elem for elem in self.cur][0]

    def add_item(self, new_item, list_select: str):
        match list_select:
            case 'new_user':
                self.cur.execute(f'INSERT INTO user_list (dis_user_id, name, task) VALUES (%s, %s, %s)', new_item)
            case 'new_quest':
                self.cur.execute(f'INSERT INTO quest_list (task, answer) VALUES (%s, %s)', new_item)
        self.base.commit()

    def update_item(self, choice, dis_user_id, num):
        match choice:
            case 'set_task':
                self.cur.execute(f'UPDATE user_list SET task = {num} WHERE dis_user_id = {dis_user_id}')
            case 'set_status':
                self.cur.execute(f'UPDATE user_list SET user_status = %s WHERE dis_user_id = %s', num, dis_user_id)
        self.base.commit()

    def delete_item(self, id, list_select: str):
        match list_select:
            case 'user_list':
                self.cur.execute(f'DELETE FROM {list_select} WHERE dis_user_id = {id}')
            case 'quest_list':
                self.cur.execute(f'DELETE FROM {list_select} WHERE quest_id = {id}')
        self.base.commit()