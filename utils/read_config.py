# -*- coding:utf-8 -*-
__author__ = 'huzixu'
import ConfigParser
import os

config_init = None



def getconfig():
    global  config_init
    if config_init is None:
        config = ConfigParser.ConfigParser()
        rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config.read(rootdir + '/config/conf.ini')
        config.read(rootdir + '/config/' + config.get('online', 'config_file'))
        config.read(rootdir + '/config/' + config.get('impl_sql', 'sql_file'))

        config_init = config
    return config_init

if __name__ == '__main__':
    pass


