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

BASENAME="challenge10"

CREDENTIALS=os.path.expanduser('~/.rackspace_cloud_credentials')

pyrax.set_credential_file(CREDENTIALS)
