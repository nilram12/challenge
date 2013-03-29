#!/usr/bin/python2.7
import pyrax
import os
import time

CREDENTIALS=os.path.expanduser('~/.rackspace_cloud_credentials')
NAME="challenge2"

pyrax.set_credential_file(CREDENTIALS)
cs = pyrax.cloudservers

parent='challenge1-1'

server= [srv for srv in cs.servers.list()
        if parent == srv.name][0]

#print server.flavor
#print str(server.flavor)
#print server.flavor['id']
#flavor=server.get_id(flavor)
print "Builiding image .", 
imageid=server.create_image(NAME+'-image')
image=cs.images.get(imageid)

while(image.status != 'ACTIVE'):
    time.sleep(10)
    print ".",
    image=cs.images.get(imageid)

print
newserver=cs.servers.create(NAME,image.id,server.flavor['id'])
