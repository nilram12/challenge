#!/usr/bin/python

# Challenge 4: Write a script that uses Cloud DNS to create a new A
# record when passed a FQDN and IP address as arguments. Worth 1 Point

import pyrax
import sys
import os

CREDENTIALS=os.path.expanduser('~/.rackspace_cloud_credentials')

def isip(ip):
    ipbool=True

    iplist=ip.split('.')

    if (len(iplist)!=4):
        return False
    for octet in iplist:
        ipbool=ipbool and octet.isdigit() and (int(octet)<256)
    return ipbool

if (len(sys.argv)!=3):
    print "Usage:",sys.argv[0],"FQDN IP" 
    sys.exit(1)

NAME=sys.argv[1]
IP=sys.argv[2]
if (not isip(IP)):
    print IP,"does not appear to be a valid IP address"
    sys.exit(1)


pyrax.set_credential_file(CREDENTIALS)
dns=pyrax.cloud_dns

try:
    domain=[dom for dom in dns.list()
            if NAME[-len(dom.name):] == dom.name ][0]
except IndexError:
    print NAME,"does not appear to be a valid domain name"
    sys.exit(1)

domain.add_records({'type' : 'A', 'name' : NAME, 'data' : IP})

