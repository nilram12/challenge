#!/usr/bin/python

# Challenge 3: Write a script that accepts a directory as an argument as
# well as a container name. The script should upload the contents of the
# specified directory to the container (or create it if it doesn't
# exist). The script should handle errors appropriately. (Check for
# invalid paths, etc.) Worth 2 Points

import pyrax
import os
import sys

CREDENTIALS=os.path.expanduser('~/.rackspace_cloud_credentials')

if (len(sys.argv)!=3):
    print "Usage:",sys.argv[0],"Directory container" 
    sys.exit(1)

CONTAINER=sys.argv[2] #  'challenge'
DIRECTORY=sys.argv[1] # os.path.expanduser('~/challenge')

if (not os.path.isdir(DIRECTORY)):
    print DIRECTORY,"is not a directory"
    sys.exit(1)

pyrax.set_credential_file(CREDENTIALS)
cf=pyrax.cloudfiles

cf.upload_folder(DIRECTORY,container=CONTAINER) 
        # Does not like broken symbolic links
