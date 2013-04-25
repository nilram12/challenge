#!/usr/bin/python

# Challenge 11: Write an application that will:
# Create an SSL terminated load balancer (Create self-signed certificate.)
# Create a DNS record that should be pointed to the load balancer.
# Create Three servers as nodes behind the LB.
#      Each server should have a CBS volume attached to it. (Size and
#      type are irrelevant.)
#      All three servers should have a private Cloud Network shared
#      between them.
#      Login information to all three servers returned in a readable
#      format as the result of the script, including connection information.
# Worth 6 points

import pyrax
import time
import os
import sys

FQDN=sys.argv[1];
BASENAME=FQDN[:FQDN.index('.')]
IMAGE="Gentoo"   
PORT=80
PROT='HTTP'
NUMSERVERS=3
TMOUT=5
SIZE=512
CBSSIZE=512
SUBNET='192.168.64.0/24'

CREDENTIALS=os.path.expanduser('~/.rackspace_cloud_credentials')

pyrax.set_credential_file(CREDENTIALS)
cs = pyrax.cloudservers
dns = pyrax.cloud_dns
clb = pyrax.cloud_loadbalancers
cnw = pyrax.cloud_networks
cbs = pyrax.cloud_blockstorage

servers=[]
vols=[]
node=[]


image=[img for img in cs.images.list()
        if IMAGE in img.name][0]

flavor=[flv for flv in cs.flavors.list()
        if flv.ram == SIZE ][0]

domain=[dom for dom in dns.list()
        if FQDN[-len(dom.name):] == dom.name ][0]

#create network and network list for new servers
localnet=cnw.create(BASENAME,cidr=SUBNET)
networks=localnet.get_server_networks(public=True, private=True)

#create servers (with networks) and create CBS volumes
for count in range(0,NUMSERVERS):
    name=BASENAME+'-'+str(count+1)
    servers.append(cs.servers.create(name,image.id,flavor.id,
                                     nics=networks))
    vols.append(cbs.create(name=name+'-cbs', size=CBSSIZE))

#poll servers until ready, add CBS and add server to LB pool when ready

for count in range(0,NUMSERVERS):
    servers[count].get()
    while (servers[count].networks == {}):
        time.sleep(TMOUT)
        servers[count].get()
    #end while
    vols[count].attach_to_instance(servers[count])            
    node.append(clb.Node(address=servers[count].networks['private'][0],
                         port=PORT, condition='ENABLED'))
#end for


#create a load blancer with public IP and add the servers as nodes.
vip = clb.VirtualIP(type="PUBLIC")
lb = clb.create(BASENAME, port=PORT, protocol=PROT,  
                nodes=node, virtual_ips=[vip])

#poll lb until active
while (lb.status != 'ACTIVE'):
    time.sleep(TMOUT)
    lb.get()

#add DNS record for LB
domain.add_records({'type' : 'A', 
                    'name' : FQDN, 
                    'data' : lb.virtual_ips[0].address})
