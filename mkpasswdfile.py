#!/usr/bin/env python3
#
#  create encoded user and passwd file for 
#           J-GEM planner and image server
#
#     Ver 1.0    2018/11/30
#

import os, sys
import base64
from jgeminfo import *
import getpass

from jgemplanner import JgemPlanner

# to be imported from jgeminfo
# USERPASSWD_FN = '.jgemuserpass'
# USERPASSWD_DIR = '' # use $HOME environment variable if empty string

def usage():
    print('Usage: mkpasswdfile.py')
    print('passuser file = %s' % (USERPASSWD_FN))

user = input('User: ')
passwd = getpass.getpass('Password: ')

user_passwd = '%s:%s' % (user, passwd)
basic_user_passwd = base64.b64encode(user_passwd.encode('utf-8'))
# print(basic_user_passwd) # debug

userpasswd_dir = JgemPlanner.getUserPassDir()

userpasswd_full_fn = '%s/%s' % (userpasswd_dir, USERPASSWD_FN)

if os.path.isfile(userpasswd_full_fn):
    print('Override current password file.')
    os.remove(userpasswd_full_fn)

try:
    f = open(userpasswd_full_fn, 'wb')
except:
    sys.stderr.write('File open error.\n')
    exit(1)

print('Encoded user:password written in %s' % (userpasswd_full_fn))
f.write(basic_user_passwd)
f.close()

print(JgemPlanner.readBasicAuthorizationUserPass())
