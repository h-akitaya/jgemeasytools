#!/usr/bin/env python2

import sys

from jgemplanner import JgemPlanner
import datetime

def usage_exit():
    print("Usage: jgemreserve.py event_id candidate_name")
    exit(1)

def reserved_message(event, candidate, obsfilter, obsdatetime):
    print("Reserved: %s, %s, %s, %s" %
          (event, candidate, obsfilter, obsdatetime))
    
if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage_exit()
    event = sys.argv[2]
    candidate = sys.argv[1]
    obsfilter = sys.argv[3]
    
    jgp = JgemPlanner()
    jgp.setObsid('SaCRA')

    jgp.getEvents()
    if not jgp.eventExists(event):
        print("Event not found. Abort")
        exit(2)
        
    jgp.getCandidates(event)
    if not jgp.candidateExists(candidate):
        print("Candidate not found. Abort")
        exit(2)

    obsdatetime = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    jgp.markReserved(event, candidate, obsfilter, obsdatetime)
    reserved_message(event, candidate, obsfilter, obsdatetime)
