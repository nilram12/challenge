#!/usr/bin/python

# Challenge 9: Write an application that when passed the arguments FQDN,
# image, and flavor it creates a server of the specified image and
# flavor with the same name as the fqdn, and creates a DNS entry for the
# fqdn pointing to the server's public IP. Worth 2 Points

import pyrax
import time
import os

TMOUT=5
CREDENTIALS=os.path.expanduser('~/.rackspace_cloud_credentials')

IMAGE="Gentoo" 
NUMSERVERS=3
FLAVOR=512
FQDN="challenge9.hendersonacademy.com"

pyrax.set_credential_file(CREDENTIALS)

cs = pyrax.cloudservers
dns = pyrax.cloud_dns

image=[img for img in cs.images.list()
        if IMAGE in img.name][0]

flavor=[flv for flv in cs.flavors.list()
        if flv.ram == FLAVOR ][0]

domain=[dom for dom in dns.list()
        if FQDN[-len(dom.name):] == dom.name ][0]

server=cs.servers.create(FQDN,image.id,flavor.id)

while (server.networks == {}):
    time.sleep(TMOUT)
    server=cs.servers.get(server.id)



domain.add_records({'type' : 'A', 
                    'name' : FQDN, 
                    'data' : server.networks{'public'}[0]})
