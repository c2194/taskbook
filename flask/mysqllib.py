import pymysql

# wawa wawa88888888b

#makedown 文件的 后缀名为 .md
class MySQL:
    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

    def connect(self):
        try:
            self.conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.db,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print('Connected to MySQL database')
        except Exception as e:
            print(f'Error connecting to MySQL database: {e}')

    def read(self, sql):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f'Error reading data from MySQL database: {e}')
            return []

    def write(self, sql):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
            self.conn.commit()
            print('Data written to MySQL database')
            return 1
        except Exception as e:
            print(f'Error writing data to MySQL database: {e}')
            return 0

    def update(self, sql):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
            self.conn.commit()
            print('Data updated in MySQL database')
        except Exception as e:
            print(f'Error updating data in MySQL database: {e}')
