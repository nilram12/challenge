#!/usr/bin/python

# Challenge 5: Write a script that creates a Cloud Database
# instance. This instance should contain at least one database, and the
# database should have at least one user that can connect to it. 
# Worth 1 Point

import pyrax
import os
import time

CREDENTIALS=os.path.expanduser('~/.rackspace_cloud_credentials')

NAME="challenge5"

DISK=2
SIZE=512
TMOUT=5

DBNAME='db'
DBUSER='dbuser'
DBPASS='dbpass'

pyrax.set_credential_file(CREDENTIALS)
cdb = pyrax.cloud_databases

flavor=[flv for flv in cdb.list_flavors()
        if flv.ram == SIZE ][0]

inst = cdb.create(NAME, flavor=flavor.name, volume=DISK)

while (inst.status == 'BUILD'):
    time.sleep (TMOUT)
    inst.get()

db = inst.create_database(DBNAME)

user = inst.create_user(name=DBUSER, password=DBPASS, database_names=[db])
