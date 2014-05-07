#!/usr/bin/env python3

import sqlalchemy as sa
import os
import re
#from multiprocessing import Pool
#from multiprocessing.dummy import Pool # multiprocessing down/kill unexpectedly encfs mount points
#http://stackoverflow.com/questions/3033952/python-thread-pool-similar-to-the-multiprocessing-pool
from multiprocessing.pool import ThreadPool as Pool # ~> $$still broken encfs$$ :(

class moo():

    class mooError(Exception): pass

    def __init__(self, databases=None, *, config=None, script_directory='', parallel=None, debug=False):
        self.databases = self.get_databases(databases, config)
        self.script_directory = script_directory
        self.parallel = parallel
        self.debug = debug
        if debug:
            self.print_debug = lambda *args, **kwargs: print(*args, **kwargs)
        else:
            self.print_debug = lambda *args, **kwargs: None
        self.print_debug('$debug={}$'.format(self.debug))

    def get_databases(self, databases, config):
        if config and (databases is None):
            return self.read_file(config).splitlines()
        elif isinstance(databases, str) and (config is None):
            return [databases]
        elif databases and (config is None):
            return databases
        else:
            raise self.mooError('get_databases({}, {})'.format(databases, config))

    def get_query(self, query, script):
        if script and (query is None):
            return self.read_file(os.path.join(self.script_directory, script)).strip()
        elif query and (script is None):
            return query
        else:
            raise self.mooError('get_query({}, {})'.format(query, script))

    def read_file(self, filename):
        if os.path.exists(filename):
            with open(filename, mode='r', encoding='utf-8') as f:
                return f.read()
        else:
            raise self.mooError('file {} does not exist'.format(filename))

    def get_parallel(self, parallel):
        parallel = parallel or self.parallel or None
        self.print_debug('$parallel={}$'.format(parallel))
        return parallel

    def __call__(self, query=None, *, script=None, parallel=None): # functor
        self.query = self.get_query(query, script)
        print('[{}]'.format(self.query))
        with Pool(self.get_parallel(parallel)) as pool:
            pool.map_async(self.execute_query, self.databases, 1, self.r_print)
            pool.close()
            pool.join()
        print()

    def hide_password(self, database):
        return re.sub(r':[^:]*@', r'@', database)

    def execute_query(self, database):
        r_queue = []
        r_queue.append('\n[{}] pid={}'.format(self.hide_password(database), os.getpid()))
        try:
            engine = sa.create_engine(database)
            connection = engine.connect()
            result = connection.execute(self.query)
            rows = result.fetchall()
            keys = result.keys()
            result.close()
            connection.close()
            r_queue.append('{}'.format(keys))
            for row in rows:
                r_queue.append('{}'.format(row))
            if self.debug: r_queue.append('$num_rows={}$'.format(len(rows)))
            return r_queue
        except Exception as e:
            print('{}'.format(e))
            raise

    def r_print(self, r_queue):
        for results in r_queue:
            for result in results:
                print(result)

if __name__ == '__main__':
    moo('sqlite:///:memory:', debug=True)('select 23 as number union select 42 as number')
