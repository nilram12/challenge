#!/usr/bin/python

# Challenge 8: Write a script that will create a static webpage served
# out of Cloud Files. The script must create a new container, cdn enable
# it, enable it to serve an index file, create an index file object,
# upload the object to the container, and create a CNAME record pointing
# to the CDN URL of the container. Worth 3 Points

import pyrax
import os

CREDENTIALS=os.path.expanduser('~/.rackspace_cloud_credentials')
CONTAINER="challenge8"
CNAME="challenge8.hendersonacademy.com"
INDEX={
    'name':'index.txt',
    'data':"Hello World!",
    'content_type': 'text/plain'}


pyrax.set_credential_file(CREDENTIALS)
cf=pyrax.cloudfiles
dns=pyrax.cloud_dns

domain=[dom for dom in dns.list()
        if CNAME[-len(dom.name):] == dom.name ][0]

cont = cf.create_container(CONTAINER)

cont.make_public();
cont.store_object(INDEX['name'],INDEX['data'],
                  content_type=INDEX['content_type'])
cont.set_web_index_page(INDEX['name'])

domain.add_records({'type' : 'CNAME', 'name' : CNAME, 
                    'data' : cont.cdn_uri[7:]})
