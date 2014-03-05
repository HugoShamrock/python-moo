moo - agile descendant foo
==========================

###What is moo:

 * Easy way how to run the same query in multiple SQL databases
 * Python object created for accessing SQL databases (used internally [SQLAlchemy](http://www.sqlalchemy.org/))
 * Simplification of the existing project called foo by using an agile approach to programming

###What is foo:

 * One of my first projects in Python (the best way how to learn programming in any language is, that you try to create something useful)
 * A project with big ambitions (to be universal interface between the database administrator and the rest of the world, foo has connectors to many SQL databases, connectors for SSH, FTP, etc.)
 * A project with a very low quality of source code
 * Still and probably never finished project
 
###Why the name moo:

 * It is similar to foo, you need only change one letter
 * Mnemonically: results from the database are moo-ed you
 * It is my favorite Linux [Easter egg](http://en.wikipedia.org/wiki/Easter_egg_%28media%29) ;)

```shell
root@work:~# apt-get moo
                 (__) 
                 (oo) 
           /------\/ 
          / |    ||   
         *  /\---/\ 
            ~~   ~~   
..."Have you mooed today?"...
```

###How to use moo:

```python
#!/usr/bin/env python3

from moo.moo import moo
m = moo('config.moo', script_directory='./oracle/')

m.sql('select host_name from v$instance')
#m.run('free_space.sql')
```

Any ideas are welcome

idxxx23
