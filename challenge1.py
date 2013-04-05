#!/usr/bin/python

# Challenge 1: Write a script that builds three 512 MB Cloud Servers
# that follow a similar naming convention (ie., web1, web2, web3) and
# returns the IP and login credentials for each server. Use any image
# you want. Worth 1 point

import pyrax
import time
import os

BASENAME="challenge1"
IMAGE="Gentoo"     
NUMSERVERS=3
TMOUT=5
SIZE=512
CREDENTIALS=os.path.expanduser('~/.rackspace_cloud_credentials')

pyrax.set_credential_file(CREDENTIALS)
password={}
servers={}
cs = pyrax.cloudservers

image=[img for img in cs.images.list()
        if IMAGE in img.name][0]

flavor=[flv for flv in cs.flavors.list()
        if flv.ram == SIZE ][0]

for count in range(0,NUMSERVERS):
    name=BASENAME+'-'+str(count+1)

    servers[name]=cs.servers.create(name,image.id,flavor.id)
    password[name]=servers[name].adminPass
    
for name in sorted(servers.keys()):
    
    servers[name]=cs.servers.get(servers[name].id)
    while (servers[name].networks == {}):
        time.sleep(TMOUT)
        servers[name].get()
    
    ips=servers[name].networks['public']
    print
    print "Name:         ", name    
    print "password:     ", password[name]
    print "IP4 (public): ", [ip for ip in ips if '.' in ip ][0]
    print "IP6 (public): ", [ip for ip in ips if '.' not in ip][0]
    print "IP4 (private):", servers[name].networks['private'][0]
       
