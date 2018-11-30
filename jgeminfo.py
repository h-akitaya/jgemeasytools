#!/usr/bin/env python3
#
#  Information file for J-GEM planner analyser
#   
#     Ver 1.00   2018/11/29   H. Akitaya
#

# General Parameters 
USERPASSWD_FN = '.jgemuserpass'
USERPASSWD_DIR = '' # environment variable $HOME is used if empty

# Sub-general parameters of J-GEM project
# processor URL
PLANNER_URL = 'http://hinotori.hiroshima-u.ac.jp/GW/planner/processor.py'
# playground URL
PLAYGROUND_URL = 'http://hinotori.hiroshima-u.ac.jp/GW/playground/processor.py'
# imageserver URL
IMAGESERVER_URL = 'http://www.growth-host.phys.sci.titech.ac.jp:8888/jgem/upload.py'

# Arbitrary parameters for each telescope/instrument
DEFAULT_OBSERVER = 'SaitamaUnivObserver'
DEFAULT_OBSID = 'SaCRA-MuSaSHI'
DEFAULT_BANDS = ['r', 'i', 'z']  # list stle only (even if with one element)

LATITUDE=35.86
LONGITUDE=139.6
HEIGHT=0.0
TZ=+9

# parameters for SaCRA only
TargetListFn = "/home/Student13/objectlist/obj_default.txt"

