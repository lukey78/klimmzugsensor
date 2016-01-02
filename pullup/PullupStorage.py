__author__ = 'Jens'

import MySQLdb
from datetime import datetime


class PullupStorage:

    def __init__(self, db_host, db_name, db_user, db_pass):
        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass

    def __connect(self):
        self.db = MySQLdb.connect(self.db_host, self.db_user, self.db_pass, self.db_name)

    def __disconnect(self):
        self.db.close()

    def setup(self):
        sql = """CREATE TABLE IF NOT EXISTS `pullup` (
                   `datetime` datetime NOT NULL,
                   PRIMARY KEY (`datetime`)
                 ) ENGINE=InnoDB DEFAULT CHARSET=latin1;"""
        self.__connect()
        self.db.cursor().execute(sql)
        self.__disconnect()

    def count_pullup(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.__connect()
        self.db.cursor().execute("INSERT INTO pullup (datetime) VALUES (%s)", timestamp)
        try:
            self.db.commit()
        except:
            self.db.rollback()
        self.__disconnect()

    def get_alltime_count(self):
        self.__connect()
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(datetime) AS cnt FROM pullup")
        result = cursor.fetchone()
        self.__disconnect()
        return int(result[0])

    def get_today_count(self):
        self.__connect()
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(datetime) AS cnt FROM pullup WHERE DATE(datetime) = DATE(NOW())")
        result = cursor.fetchone()
        self.__disconnect()
        return int(result[0])
