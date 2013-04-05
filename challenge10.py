#!/usr/bin/python

# Challenge 10: Write an application that will:
# - Create 2 servers, supplying a ssh key to be 
#   installed at /root/.ssh/authorized_keys.
# - Create a load balancer
# - Add the 2 new servers to the LB
# - Set up LB monitor and custom error page. 
# - Create a DNS record based on a FQDN for the LB VIP. 
# - Write the error page html to a file in cloud files for backup.
# Whew! That one is worth 8 points!

import pyrax
import time
import os

FQDN="challenge10.hendersonacademy.com"
BASENAME=FQDN[:FQDN.index('.')]
IMAGE="Gentoo"   
PORT=80
PROT='HTTP'
NUMSERVERS=2
TMOUT=5
SIZE=512

ERROR={
    'name':'error.html',
    'data':'''<html>
              <head>
               <title>DANGER!!</title>
              </head>
              <body>
              <p> UH OH somethings wrong! </p>
              </body>
              </html>''',
    'content_type':'text/html'}


CREDENTIALS=os.path.expanduser('~/.rackspace_cloud_credentials')
ID=os.path.expanduser('~/.ssh/id_rsa.pub')

idfile={"/root/.ssh/authorized_keys": open(ID,'r')}

pyrax.set_credential_file(CREDENTIALS)
cs = pyrax.cloudservers
cf = pyrax.cloudfiles
dns = pyrax.cloud_dns
clb= pyrax.cloud_loadbalancers


servers=[]
node=[]


image=[img for img in cs.images.list()
        if IMAGE in img.name][0]

flavor=[flv for flv in cs.flavors.list()
        if flv.ram == SIZE ][0]

domain=[dom for dom in dns.list()
        if FQDN[-len(dom.name):] == dom.name ][0]

cont=cf.create_container(BASENAME) #assume it doesn't exist.

cont.store_object(ERROR['name'],ERROR['data'],
                  content_type=ERROR['content_type'])

for count in range(0,NUMSERVERS):
    name=BASENAME+'-'+str(count+1)
    servers.append(cs.servers.create(name,image.id,flavor.id,
                                     files=idfile))

for count in range(0,NUMSERVERS):
    servers[count].get()
    while (servers[count].networks == {}):
        time.sleep(TMOUT)
        servers[count].get()
    #end while
    node.append(clb.Node(address=servers[count].networks['private'][0],
                         port=PORT, condition='ENABLED'))
#end for

vip = clb.VirtualIP(type="PUBLIC")

lb = clb.create(BASENAME, port=PORT, protocol=PROT,  
                nodes=node, virtual_ips=[vip])

while (lb.status != 'ACTIVE'):
    time.sleep(TMOUT)
    lb.get()

lb.set_error_page(ERROR['data'])

domain.add_records({'type' : 'A', 
                    'name' : FQDN, 
                    'data' : lb.virtual_ips[0].address})
