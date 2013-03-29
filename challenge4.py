#!/usr/bin/python
import pyrax
import os

CREDENTIALS=os.path.expanduser('~/.rackspace_cloud_credentials')
IP='127.0.0.1'
NAME='localhost.hendersonacademy.com'

pyrax.set_credential_file(CREDENTIALS)
dns=pyrax.cloud_dns

domain=[dom for dom in dns.list()
        if NAME[-len(dom.name):] == dom.name ][0]

domain.add_records({'type' : 'A', 'name' : NAME, 'data' : IP})
