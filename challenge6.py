#!/usr/bin/python

# Challenge 6: Write a script that creates a CDN-enabled container in
# Cloud Files. Worth 1 Point

import pyrax
import os

CREDENTIALS=os.path.expanduser('~/.rackspace_cloud_credentials')
CONTAINER="challenge6"

pyrax.set_credential_file(CREDENTIALS)
cf=pyrax.cloudfiles


cont = cf.create_container(CONTAINER)

cont.make_public();
