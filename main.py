class Account:
    import sqlite3 as sq
    filename = None

    @classmethod
    def create_empty_table(cls, filename):
        with cls.sq.connect(f'{filename}.db') as con:
            cls.filename = filename
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS data (
                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            login TEXT,
                            password TEXT,
                            money INTEGER DEFAULT 0,
                            experience INTEGER DEFAULT 0
                            )""")

    @classmethod
    def register(cls):
        with cls.sq.connect(f'{cls.filename}.db') as con:
            cur = con.cursor()
            while True:
                login = input('Придумайте логин: ')
                if (login,) in list(cur.execute("""SELECT login from data""")):
                    print('Этот логин уже занят')
                    continue
                else:
                    password = input('Придумайте пароль: ')
                    cur.execute(f"""INSERT INTO data (login, password) VALUES ('{login}', '{password}')""")
                    print('Регистрация прошла успешно!')
                    break

    @classmethod
    def enter(cls, log):
        with cls.sq.connect(f'{cls.filename}.db') as con:
            cur = con.cursor()
            while True:
                password = input('Введите пароль: ')
                if (password,) == list(cur.execute(f"""SELECT password from data WHERE login = '{log}'"""))[0]:
                    print(f'Приветствую, {log}!')
                    break
                else:
                    print('Неверный пароль')
                    continue

    def __new__(cls, *args, **kwargs):
        with cls.sq.connect(f'{cls.filename}.db') as con:
            cur = con.cursor()
            logins = list(cur.execute("""SELECT login from data"""))
            login = args[0]
            if (login,) not in logins:
                print('Такого пользователя не существует')
                ans = input('Зарегистрироваться?(д/н) ')
                if ans.lower() == 'д':
                    cls.register()
                    return super().__new__(cls)
                else:
                    return None
            else:
                cls.enter(login)
                return super().__new__(cls)

    def __init__(self, name):
        self.name = name

    def add_money(self, m):
        with self.sq.connect(f'{self.filename}.db') as con:
            cur = con.cursor()
            cur.execute(f"""UPDATE data SET money = money + {m} WHERE login = '{self.name}'""")
            print('Количество ваших денег изменено')

    def add_xp(self, x):
        with self.sq.connect(f'{self.filename}.db') as con:
            cur = con.cursor()
            cur.execute(f"""UPDATE data SET experience = experience + {x} WHERE login = '{self.name}'""")
            print('Количество вашего опыта изменено')

    def spend_money(self, s):
        with self.sq.connect(f'{self.filename}.db') as con:
            cur = con.cursor()
            cur.execute(f"""UPDATE data SET money = money - {s} WHERE login = '{self.name}'""")
            print('Остаток денег изменен')

    def get_balance(self):
        with self.sq.connect(f'{self.filename}.db') as con:
            cur = con.cursor()
            cur.execute(f"""SELECT money, experience from data WHERE login = '{self.name}'""")
            for data in cur:
                lst_data = data
            return lst_data


Account.create_empty_table('data')
login = input('Введите логин: ') # вход или регистрация
obj = Account(login) # аккаунт во время сессии, если None - программа завершается

if obj is not None:
    while True:
        command = input('Введите команду: ')
        if command.lower() == 'добавить деньги':
            m = int(input('Введите сумму денег: '))
            obj.add_money(m)
        elif command.lower() == 'добавить опыт':
            x = int(input('Введите количество опыта: '))
            obj.add_xp(x)
        elif command.lower() == 'потратить деньги':
            s = int(input('Введите потраченную сумму: '))
            obj.spend_money(s)
        elif command.lower() == 'баланс':
            bal = obj.get_balance()
            print(f'Деньги: {bal[0]}\nОпыт: {bal[1]}')
        elif command.lower() == 'выход':
            break
