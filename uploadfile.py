#!/usr/bin/env python
#
#   Ver 1.1 2019/02/24    H. Akitaya
#        python3 -> python in shebang
#

import sys

from jgemplanner import JgemPlanner

def usage_exit():
    print("Usage: jgemreserve.py event_id candidate_name")
    exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 1:
        usage_exit()
    fitsfn = sys.argv[1]
    
    jgp = JgemPlanner()
    jgp.uploadFileToImageServer(fitsfn)
