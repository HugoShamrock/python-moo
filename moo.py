#!/usr/bin/env python3

import sqlalchemy as sa
import os.path
import re
import multiprocessing
import sys

class moo():

    def __init__(self, databases=None, script_directory=None, debug=False):
        self.debug = debug
        self.script_directory = script_directory
        if self.debug: print('[moo-debug: debug={}]'.format(self.debug))
        result = self.read_file(databases)
        if result:
            self.databases = result.splitlines()
        else:
            if isinstance(databases, str):
                self.databases = [databases]
            else:
                self.databases = list(databases)

    def read_file(self, filename):
        if os.path.exists(filename):
            with open(filename, mode='r', encoding='utf-8') as f:
                return f.read()
        else:
            return None

    def run(self, filename):
        result = self.read_file(os.path.join(self.script_directory, filename))
        if result:
            self.sql(result.strip())
        else:
            print('[moo-error: file \'{}\' does not exist]'.format(filename))

    def sql(self, query):
        print('[{}]'.format(query))
        sys.stdout.flush()
        w_queue = multiprocessing.JoinableQueue()
        w_count = len(self.databases) # degree of parallelism (max_parallel) ~> len(self.databases)
        for i in range(w_count):
            w_process = multiprocessing.Process(target = lambda: self.w_sql(w_queue, query, i+1, w_count))
            w_process.daemon = True
            w_process.start()
        for database in self.databases:
            w_queue.put(database)
        w_queue.join()
        print()
        sys.stdout.flush()

    def w_sql(self, w_queue, query, w_number, w_count):
        while True:
            try:
                database = w_queue.get()
                parms = self.execute_query(database, query)
                print('\n[{1}/{2}]>[{0}]'.format(self.hide_password(database), w_number, w_count))
                if parms: self.print_rows(*parms)
                sys.stdout.flush()
            finally:
                w_queue.task_done()

    def __call__(self, something): # functor
        if ' ' in something:
            self.sql(something)
        else:
            self.run(something)

    def hide_password(self, database):
        return re.sub(r':[^:]*@', r'@', database)

    def execute_query(self, database, query):
        try:
            engine = sa.create_engine(database)
            connection = engine.connect()
            result = connection.execute(query)
            rows = result.fetchall()
            keys = result.keys()
            result.close()
            connection.close()
            return (rows, keys)
        except Exception as e:
            print('{}'.format(e))

    def print_rows(self, rows, keys):
        print('{}'.format(keys))
        for row in rows:
            print('{}'.format(row))
        if self.debug: print('[moo-debug: num_rows={}]'.format(len(rows)))

if __name__ == '__main__':
    moo('sqlite:///:memory:', debug=True)('select 23 as number')
