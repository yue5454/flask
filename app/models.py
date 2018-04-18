import MySQLdb


class mysqlOperation(object):
    """docstring for mysqlOperation"""
    def __init__(self, **arg):
        self.host = arg['host']
        self.user = arg['user']
        self.passwd = arg['passwd']
        self.db = arg['db']
        self.charset = arg['charset']

    def connect(self):
        return MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, charset=self.charset)

    def close(self):
        self.connect().close()

    def rollback(self):
        self.connect().rollback()

    def select_command(self, sql):
        cursor = self.connect().cursor()
        try:
            cursor.execute(sql)
            return cursor
        except Exception as e:
            raise e
        finally:
            self.close()

    def general_command(self, sql):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            raise e
        finally:
            self.close()


db_dict = {
    'host': 'localhost',
    'user': 'root',
    'passwd': 'nice642354',
    'db': 'lily_test',
    'charset': 'utf8'
}


mySqlDB = mysqlOperation(**db_dict)