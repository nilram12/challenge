#!/usr/bin/python
import pyrax
import os

CREDENTIALS=os.path.expanduser('~/.rackspace_cloud_credentials')
CONTAINER="challenge6"

pyrax.set_credential_file(CREDENTIALS)
cf=pyrax.cloudfiles


cont = cf.create_container(CONTAINER)

cont.make_public();
