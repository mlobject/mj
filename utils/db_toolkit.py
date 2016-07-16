# -*- coding:utf-8 -*-
from memsql.common import database

class DBToolkit(object):
    def __init__(self, config):
        self.config = config
        self.conn = None

    def __connect(self):
        if self.conn is None:
            self.create__connection()

        return self.conn

    def create__connection(self):
        conn = database.connect(host=self.config.mysql_host, port=int(self.config.mysql_port),
                               user=self.config.mysql_user, password=self.config.mysql_password,
                               database=self.config.mysql_db)

        self.conn = conn

    def query_data(self, sql, param=None):
        conn = self.__connect()
        result=conn.query(sql)
        conn.close()
        return result


    def insert_data(self, sql, param=None):
        """
        @summary: 向数据表插入一条记录
        @param sql:要插入的ＳＱＬ格式
        @param value:要插入的记录数据tuple/list
        @return: insertId 受影响的行数
        """
        conn = self.__connect()
        conn.execute(sql)
        conn.close()
        return 'success'

    # def close(self):
    #     if self.conn:
    #         self.conn.close()
