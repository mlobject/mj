# -*- coding:utf-8 -*-
class CmsMysqlConfig(object):
    """cms的mysql配置"""
    def __init__(self):
        super(CmsMysqlConfig, self).__init__()
        self.mysql_host = '0.0.0.0'
        self.mysql_port = '3306'
        self.mysql_user = 'root'
        self.mysql_password = ''
        self.mysql_db = 'test'

    def __str__(self):
        return 'mysql_host:' + self.mysql_host + \
               'mysql_port: ' + self.mysql_port + \
               'mysql_user: ' + self.mysql_user + \
               'mysql_password: ' + self.mysql_password +\
               'mysql_db: ' + self.mysql_db
