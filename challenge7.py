#!/usr/bin/python

# Challenge 7: Write a script that will create 2 Cloud Servers and add
# them as nodes to a new Cloud Load Balancer. Worth 3 Points

import pyrax
import time
import os


BASENAME="challenge7"
IMAGE="Gentoo"   
PORT=80
PROT='HTTP'
NUMSERVERS=2
TMOUT=5
SIZE=512
CREDENTIALS=os.path.expanduser('~/.rackspace_cloud_credentials')

pyrax.set_credential_file(CREDENTIALS)
node=[]
servers=[]
cs = pyrax.cloudservers
clb= pyrax.cloud_loadbalancers

image=[img for img in cs.images.list()
        if IMAGE in img.name][0]

flavor=[flv for flv in cs.flavors.list()
        if flv.ram == SIZE ][0]

for count in range(0,NUMSERVERS):
    name=BASENAME+'-'+str(count+1)

    servers.append(cs.servers.create(name,image.id,flavor.id))
    
for count in range(0,NUMSERVERS):
    servers[count].get()
    while (servers[count].networks == {}):
        time.sleep(TMOUT)
        servers[count].get()
    #end while
    node.append(clb.Node(address=servers[count].networks['private'][0],
                         port=PORT, condition='ENABLED'));
#end for

vip = clb.VirtualIP(type="PUBLIC")
lb = clb.create(BASENAME, port=PORT, protocol=PROT,  
                nodes=node, virtual_ips=[vip])
