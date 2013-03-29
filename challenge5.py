#!/usr/bin/python2.7
import pyrax
import os
import time

CREDENTIALS=os.path.expanduser('~/.rackspace_cloud_credentials')

NAME="challenge5"

DISK=2
SIZE=512

DBNAME='db'
DBUSER='dbuser'
DBPASS='dbpass'

pyrax.set_credential_file(CREDENTIALS)
cdb = pyrax.cloud_databases

flavor=[flv for flv in cdb.list_flavors()
        if flv.ram == SIZE ][0]

inst = cdb.create(NAME, flavor=flavor.name, volume=DISK)

while (inst.status == 'BUILD'):
    time.sleep (5)
    inst.get()

db = inst.create_database(DBNAME)

user = inst.create_user(name=DBUSER, password=DBPASS, database_names=[db])
