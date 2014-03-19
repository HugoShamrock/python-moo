#!/usr/bin/env python3

import sqlalchemy as sa
import os.path
import re

class moo():

    def __init__(self, databases=None, debug=False, script_directory=None):
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
        for database in self.databases:
            print('\n[{}]'.format(self.hide_password(database)))
            parms = self.execute_query(database, query)
            if parms: self.print_rows(*parms)
        print()

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
    moo('sqlite:///:memory:', True).sql('select 23 as number')
