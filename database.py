#!/usr/bin/env python3

# $$todo$$ ~> multiprocessing unexpectedly kill encfs mount-points

import os, re, sqlalchemy as sa
from multiprocessing import Pool
from multiprocessing.dummy import Pool
from multiprocessing.pool import ThreadPool as Pool # http://stackoverflow.com/questions/3033952/python-thread-pool-similar-to-the-multiprocessing-pool
import moo.connector

class execute(moo.connector.execute):

    class moo_error(Exception): pass

    def __init__(self, connections=None, *, config=None, script_directory='', parallel=None, debug=False):
        self.connections = self.get_connections(connections, config)
        self.script_directory = script_directory
        self.parallel = parallel
        self.debug = debug
        if self.debug:
            self.print_debug = print
        else:
            self.print_debug = self.nothing
        self.print_debug('$debug={}$'.format(self.debug))

    def nothing(*args, **kwargs): pass

    def get_connections(self, connections, config):
        if config and (connections is None):
            return self.read_file(config).splitlines()
        elif isinstance(connections, str) and (config is None):
            return [connections]
        elif connections and (config is None):
            return connections
        else:
            raise self.moo_error('get_connections({}, {})'.format(connections, config))

    def get_command(self, command, script):
        if script and (command is None):
            return self.read_file(os.path.join(self.script_directory, script)).strip()
        elif command and (script is None):
            return command
        else:
            raise self.moo_error('get_command({}, {})'.format(command, script))

    def read_file(self, filename):
        if os.path.exists(filename):
            with open(filename, mode='r', encoding='utf-8') as f:
                return f.read()
        else:
            raise self.moo_error('file {} does not exist'.format(filename))

    def get_parallel(self, parallel):
        parallel = parallel or self.parallel or None
        self.print_debug('$parallel={}$'.format(parallel))
        return parallel

    def __call__(self, command=None, *, script=None, parallel=None): # functor
        self.command = self.get_command(command, script)
        print('[{}]'.format(self.command))
        with Pool(self.get_parallel(parallel)) as pool:
            pool.map_async(self.execute_command, self.connections, 1, self.r_print)
            pool.close()
            pool.join()
        print()

    def script(self, script=None, *, parallel=None):
        self.__call__(script=script, parallel=parallel)

    def hide_password(self, connection):
        return re.sub(r':[^:]*@', r'@', connection)

    def execute_command(self, connection):
        r_queue = []
        r_queue.append('\n[{}] pid={}'.format(self.hide_password(connection), os.getpid()))
        try:
            engine = sa.create_engine(connection)
            connection = engine.connect()
            result = connection.execute(self.command)
            keys, rows = result.keys(), result.fetchall()
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
        for rows in r_queue:
            for row in rows:
                print(row)

if __name__ == '__main__':
    execute('sqlite:///:memory:', debug=True)('select 23 as number union select 42 as number')
    execute('sqlite:///:memory:')('select 23 as number union select 42 as number')
