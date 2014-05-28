#!/usr/bin/env python3

import os, paramiko
from configurator.formats import json as configurator
import moo.connector

class execute(moo.connector.execute):

    def get_connections(self, connections, config):    
        if config and (connections is None):
            return configurator.load(config)['connections']

    def hide_password(self, connection):
        #del connection['password'] # $$del~>bug$$
        return connection

    def execute_query(self, connection):
        r_queue = []
        r_queue.append('\n[{}] pid={}'.format(self.hide_password(connection), os.getpid()))
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            #client.connect(connection)
            #stdin, stdout, stderr = client.exec_command(self.query) # command
            client.close()
            #r_queue.append(stdout.read())
            #r_queue.append(stderr.read())
            return r_queue
        except Exception as e:
            print('{}'.format(e))
            raise
