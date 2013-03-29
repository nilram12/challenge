#!/usr/bin/python2.7
import pyrax
import os

CREDENTIALS=os.path.expanduser('~/.rackspace_cloud_credentials')
directory='/home/nilram/challenges/'

pyrax.set_credential_file(CREDENTIALS)
cf=pyrax.cloudfiles

cf.upload_folder(directory,container='challenges')
