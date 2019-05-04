#!/usr/bin/env python3
#
#
#  J-GEM observation tool for SaCRA-MuSaSHI et al.
#
#
#       Ver 1.00   2018/11/22   H. AKitaya
#       Ver 1.10   2018/11/26   H. AKitaya
#       Ver 1.20   2018/11/29   H. AKitaya: tables -> dictionary style
#       Ver 1.30   2019/05/04   H. AKitaya: update for new J-GEM format
#
#         usage: ./jgemobs.py -pi -e S190412m -o 'Name1, Name2'
#                           # for real GW event 
#

import sys, os
import argparse

from jgemplanner import JgemPlanner

VERSION='1.20'

if __name__ == '__main__':
    # option parser
    parser = argparse.ArgumentParser(description='Process some integers.', 
                                     prog='jgemobs.py')
    parser.add_argument('-i', '--interactive', action='store_true',
                        default=False,
                        help='interactive mode')
    parser.add_argument('-a', '--auto', action='store_true',
                        default=False,
                        help='auto mode (not implemented yet)')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.10') 

    # True: useing planner for real events; False: using playground.
    parser.add_argument('-p', '--planner', action='store_true', 
                        default=False,
                        help='use planner for an actual event. (default = playground)')

    parser.add_argument('-o', '--observer', nargs='?', type=str,
                        help='observer(s) (e.g) "Akitaya et al." (to be quoted if space characters are included)')
    parser.add_argument('-e', '--eventid', nargs='?', type=str,
                        help='eventid (e.g.) U12345')
    parser.add_argument('-d', '--obsid', nargs='?', type=str, default=None,
                        help='obsid (e.g) SaCRA-MuSaSHI (=default)')
    parser.add_argument('-b', '--bands', nargs='?', type=str, default=None,
                        help='bands (e.g) R or "r i z" (= default) (to be quoted and spaced for multiple bands)')
    args = parser.parse_args()

    jgp = JgemPlanner(planner=args.planner)
    if args.observer != None:
        jgp.observer = str(args.observers)
    if args.obsid != None:
        jgp.obsid = str(args.obsid)
    if args.bands != None:
        try:
            bands = args.bands.split()
        except:
            sys.stderr.write('Wrong band information. Abort.\n')
            exit(1)
        jgp.bands = args.bands

    jgp.getEvents()
    if args.eventid != None:
        jgp.setCurrentEventid(str(args.eventid))
    else:
        latest_event = jgp.events[0]['eventid']
        jgp.setCurrentEventid(latest_event)
    jgp.getCandidates()

    # interactive (command prompt) mode
    if args.interactive == True:
        jgp.showCandidates(number=True)
        jgp.interactiveModeMainLoop()

    
    #Debug -begin
    #    print(jgp.candidates)
    #    pprint.pprint(jgp.candidates, width=80)
    #    print(type(jgp.candidates))
    exit(1)
