#!/usr/bin/python

# Challenge 9: Write an application that when passed the arguments FQDN,
# image, and flavor it creates a server of the specified image and
# flavor with the same name as the fqdn, and creates a DNS entry for the
# fqdn pointing to the server's public IP. Worth 2 Points

import pyrax
import time
import os
import sys

TMOUT=5
CREDENTIALS=os.path.expanduser('~/.rackspace_cloud_credentials')

if (len(sys.argv)!=4):
    print "Usage:",sys.argv[0],"FQDN image flavor" 
    sys.exit(1)


FLAVOR=sys.argv[3] 
if (FLAVOR.isdigit()):
    FLAVOR=int(FLAVOR)
else:
    print FLAVOR, "must be numeric"
    sys.exit(1)

IMAGE=sys.argv[2] #"Gentoo" 

FQDN=sys.argv[1] 

pyrax.set_credential_file(CREDENTIALS)

cs = pyrax.cloudservers
dns = pyrax.cloud_dns

try:
    image=[img for img in cs.images.list()
           if IMAGE in img.name][0]
except IndexError:
    print "I could not find an image named", image
    sys.exit(1)

try:
    flavor=[flv for flv in cs.flavors.list()
            if flv.ram == FLAVOR ][0]
except IndexError:
    print "I can't find flavor:", FLAVOR
    sys.exit(1)

try:
    domain=[dom for dom in dns.list()
            if FQDN[-len(dom.name):] == dom.name ][0]
except IndexError:
    print NAME,"does not appear to be a valid domain name"
    sys.exit(1)

server=cs.servers.create(FQDN,image.id,flavor.id)

while (server.networks == {}):
    time.sleep(TMOUT)
    server=cs.servers.get(server.id)

domain.add_records({'type' : 'A', 
                    'name' : FQDN, 
                    'data' : [ip for ip in server.networks['public'] 
                              if '.' in ip][0]})
