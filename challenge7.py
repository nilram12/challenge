#!/usr/bin/python2.7
import pyrax
import time
import os

BASENAME="challenge7"
IMAGE="Gentoo"     # Just to be different :)
PORT=80
PROT='HTTP'
NUMSERVERS=2
TMOUT=5
SIZE=512
CREDENTIALS=os.path.expanduser('~/.rackspace_cloud_credentials')

pyrax.set_credential_file(CREDENTIALS)
password={}
servers={}
cs = pyrax.cloudservers
clb= pyrax.cloud_loadbalancers

image=[img for img in cs.images.list()
        if IMAGE in img.name][0]

flavor=[flv for flv in cs.flavors.list()
        if flv.ram == SIZE ][0]

for count in range(1,NUMSERVERS+1):
    name=BASENAME+'-'+str(count)

    servers[name]=cs.servers.create(name,image.id,flavor.id)
    password[name]=servers[name].adminPass
    
for name in sorted(servers.keys()):
    
    servers[name]=cs.servers.get(servers[name].id)
    while (servers[name].networks == {}):
        time.sleep(TMOUT)
        servers[name]=cs.servers.get(servers[name].id)
    print 

    print "Admin password:", password[name]
    print "Networks:", servers[name].networks

vip = clb.VirtualIP(type="PUBLIC")
lb = clb.create(BASENAME, port=PORT, protocol=PROT,  
                nodes=servers.values(), virtual_ips=[vip])
