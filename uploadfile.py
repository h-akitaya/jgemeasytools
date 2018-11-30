#!/usr/bin/env python3

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
