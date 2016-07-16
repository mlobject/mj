# -*- coding: utf-8 -*-
#!/usr/bin/python
__author__ = 'huzixu'
import os
import sys
import time
import threading
import argparse
from utils import db_toolkit

from memsql.common import database

parser = argparse.ArgumentParser()

#parser.add_argument("--host", default='hkg02-dx-kafka02.hkg02.baidu.com', help="The hostname of the MemSQL node to connect to")
parser.add_argument("--host", default='127.0.0.1', help="The hostname of the MemSQL node to connect to")
parser.add_argument("--port", default=32769, type=int, help="The port of the MemSQL node to connect to")
parser.add_argument("--user", default="root", help="The user of the MemSQL node to connect to")
parser.add_argument("--password", default="", help="The password of the MemSQL node to connect to")

parser.add_argument("--database", default="mj", help="The database to use - note: this database should not exist")

parser.add_argument("--num-workers", type=int, default=10, help="The number of insert threads")
parser.add_argument("--time", type=int, default=30, help="The number of seconds to run the benchmark for")

options = parser.parse_args()

#HOST = None
#PORT = None

TABLE = "tbl"
BATCH_SIZE = 5000

# Pre-generate the workload query
QUERY_TEXT = "INSERT INTO %s (val) VALUES %s" % (TABLE, ",".join(["(1)"] * BATCH_SIZE))



def get_connection(host=options.host, port=options.port, db=options.database):
    """ Returns a new connection to the database. """
    if host is None:
        host = HOST
    if port is None:
        port = PORT

    return database.connect(
        host=host,
        port=port,
        user=options.user,
        password=options.password,
        database=db)

class InsertWorker(threading.Thread):
    """ A simple thread which inserts empty rows in a loop. """

    def __init__(self, stopping):
        super(InsertWorker, self).__init__()
        self.stopping = stopping
        self.daemon = True
        self.exception = None

    def run(self):
        with get_connection() as conn:
            while not self.stopping.is_set():
                conn.execute(QUERY_TEXT)

def test_connection():
    try:
        with get_connection(db="information_schema") as conn:
            conn.ping()
    except database.MySQLError:
        print("Unable to connect to MemSQL with provided connection details.")
        print("Please verify that MemSQL is running @ %s:%s" % (HOST, PORT))
        sys.exit(1)

def setup_test_db():
    """ Create a database and table for this benchmark to use. """

    with get_connection(db="information_schema") as conn:
        print('Creating database %s' % options.database)

        try:
            # note: the following query will fail if there is an existing database
            conn.query('CREATE DATABASE %s' % options.database)
        except database.MySQLError:
            print("Database %s already exists - since we drop the database at" % options.database)
            print("the end of this script, please specify an un-used database")
            print("with the --database flag.")
            sys.exit(1)

        conn.query('USE %s' % options.database)

        conn.query('CREATE TABLE IF NOT EXISTS %s (id INT AUTO_INCREMENT PRIMARY KEY, val INT)' % TABLE)

def warmup():
    print('Warming up workload')
    with get_connection() as conn:
        conn.execute(QUERY_TEXT)

def run_benchmark():
    """ Run a set of InsertWorkers and record their performance. """

    stopping = threading.Event()
    workers = [ InsertWorker(stopping) for _ in range(options.num_workers) ]

    print('Launching %d workers' % options.num_workers)
    print('Workload will take approximately %d seconds.' % options.time)

    [ worker.start() for worker in workers ]
    time.sleep(options.time)

    print('Stopping workload')

    stopping.set()
    [ worker.join() for worker in workers ]

    with get_connection() as conn:
        count = conn.get("SELECT COUNT(*) AS count FROM %s" % TABLE).count

    print("%d rows inserted using %d threads" % (count, options.num_workers))
    print("%.1f rows per second" % (count / float(options.time)))

def cleanup():
    """ Cleanup the database this benchmark is using. """
    try:
        with get_connection() as conn:
            conn.query('DROP DATABASE IF EXISTS %s' % options.database)
    except database.MySQLError:
        pass

if __name__ == '__main__':
    HOST = options.host or "127.0.0.1"
    PORT = options.port or 3306
    cleanup()

    try:
        test_connection()
        setup_test_db()
        warmup()
        run_benchmark()
    except KeyboardInterrupt:
        print("Interrupted... exiting...")