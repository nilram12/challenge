#!/usr/bin/python

# Challenge 2: Write a script that clones a server (takes an image and
# deploys the image as a new server). Worth 2 Points

import pyrax
import os
import time

CREDENTIALS=os.path.expanduser('~/.rackspace_cloud_credentials')
NAME="challenge2"
TMOUT=5

pyrax.set_credential_file(CREDENTIALS)
cs = pyrax.cloudservers

PARENT='challenge1-1'

server= [srv for srv in cs.servers.list()
        if PARENT == srv.name][0]


imageid=server.create_image(NAME+'-image')
image=cs.images.get(imageid)

while(image.status != 'ACTIVE'):
    time.sleep(TMOUT)
    image.get()


newserver=cs.servers.create(NAME,image.id,server.flavor['id'])
