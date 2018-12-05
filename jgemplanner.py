#!/usr/bin/env python3
#
#  J-GEM planner analyser for SaCRA telescope (or other telescope)
#   
#     Ver 1.00   2018/11/22   H. Akitaya
#     Ver 1.01   2018/11/26   H. Akitaya
#     Ver 1.02   2018/11/28   H. Akitaya: Mexpected included in JSON file
#     Ver 1.03   2018/11/29   H. Akitaya: Tables -> dictionary style, etc.
#     Ver 1.04   2018/11/29   H. Akitaya: exception for invalid user/pass
#                                         in readProcessorPy()
#

# to be imported from jgeminfo
# PLANNER_URL = ''
# PLAYGROUND_URL = ''
# DEFAULT_OBSERVER = ''
# DEFAULT_OBSID = ''
# DEFAULT_BANDS = ['', ...]  # as list 
# TargetListFn = ''

import sys, os, re, copy
import subprocess
import json
import urllib
import datetime
import pprint
import argparse

from jgemcoord import JgemCoord
from jgeminfo import *
from jgemidgrp import JgemIdGrp 

class JgemPlanner(object):
    def __init__(self, planner=False):
        self.header_candidates = []
        self.header_events = []
        self.events = []
        self.candidates = []
        self.cndhc = []
        self.obsid = DEFAULT_OBSID
        self.observer = DEFAULT_OBSERVER
        self.eventid = ''
        self.gids = JgemIdGrp.getDefinedGroupids()
        if planner == False:
            self.processor = PLAYGROUND_URL
        else:
            self.processor = PLANNER_URL
        self.imageserver = IMAGESERVER_URL

    def setObsid(self, obsid):
        self.obsid = obsid

    def setObserver(self, observer):
        self.observer = observer
        
    def getEvents(self):
        params = {'eventid': '', 'mode': 'eventid'}
        content = self.readProcessorPy(params)
        events = json.loads(content)
        self.header_events = copy.copy(events[0])
        del events[0] # delete table header
        for event in events:
            self.events.append(dict(zip(self.header_events, event)))

    def getCandidates(self):
        params = {'eventid': self.eventid, 'mode': 'candidate'}
        content = self.readProcessorPy(params)
        candidates = json.loads(content)
        self.header_candidates = copy.copy(candidates[0])
        del candidates[0]  # delete table header
        for cnd in candidates:
            self.candidates.append(dict(zip(self.header_candidates, cnd)))
        self.addRaDecHexToCandiateList()
        #self.showCandidates()

    def addRaDecHexToCandiateList(self):
        n=0
        for cnd in self.candidates:
            hexcoord = self.getRaDec(float(cnd['ra']), float(cnd['dec'])).split()
            self.cndhc.append({'RA': hexcoord[0], 'dec': hexcoord[1]})
            n+=1

    def uploadFileToImageServer(self, fitsfn):
        # https://qiita.com/5zm/items/92cde9e043813e02eb68
        import requests
        import base64

        # read (USER, PASS) from password file and create digestauth object
        basic_user_pass = JgemPlanner.readBasicAuthorizationUserPass()
        authinfo = base64.b64decode(basic_user_pass).decode('utf-8').split(':')
        auth = requests.auth.HTTPDigestAuth(authinfo[0], authinfo[1]) 

        url = self.imageserver
        fileDataBinary = open(fitsfn, 'rb').read()
        files = {'fits': (fitsfn, fileDataBinary)}
        # print(url, auth) # Debug
        
        res = requests.post(url=url, files=files, auth=auth)
        # print(res.status_code) # Debug
        # print(res.text) # Debug
        if (str(res.status_code) == "200"):
            print("File was successfully Uploaded.")
        else:
            sys.stderr.write('Image Server Access error. Check URL or user/passwd file.\n')

    def readProcessorPy(self, params):
        query_string = urllib.parse.urlencode(params)
        url = self.processor + '?' + query_string
#        print(url)
        basic_user_pass = JgemPlanner.readBasicAuthorizationUserPass()
        request = urllib.request.Request(url=url, headers={"Authorization": "Basic " + basic_user_pass.decode('utf-8')})
        try:
            response = urllib.request.urlopen(request)
            content = response.read()
        except:
            sys.stderr.write('Plannaer reading error. Check URL or user/passwd file.\n')
            exit(1)
        return(content)

    def showEventTableHeaders(self):
        print(self.header_events)

    def showCandidateTableHeaders(self):
        print(self.header_candidates)

    def showEvents(self):
        print('#%d events found.' % len(self.events))
        for event in self.events:
            print('%10s %s %s' % (event['eventid'], event['inserted'], event['state']))

    def setCurrentEventid(self, eventid):
#        print(self.events)
        for event in self.events:
            if event['eventid'] == eventid:
                self.eventid = eventid
                return(True)
        print('Eventid %s not found.' % (eventid))
        return(False)
            
    def showCurrentEvent(self):
        print(self.eventid)

    def getRaDec(self, ra_deg, dec_deg):
        jc = JgemCoord()
        jc.setDegDeg(ra_deg, dec_deg)
        hexcoord = jc.getHex()
        return(hexcoord)

    def showCandidates(self, number=False, nonreserved=False, hastransient=False, grep=False, grepstr='', group=False):
        print('#%d events found.' % len(self.candidates))
        n=0
        for cnd in self.candidates:
            showstr = '%20s %10s %10.9f %s %10.4f %10.4f %10.4f %s %s %s %s %s %s %s %s %s' % (cnd['galid'], cnd['eventid'], cnd['prob'], cnd['inserted'], cnd['ra'], cnd['dec'], cnd['dist'], cnd['OptExpected'], cnd['NirExpected'], cnd['state'], cnd['obsids'], cnd['updated'], cnd['filter and depth (5&sigma;AB)'], cnd['hastransient'], self.cndhc[n]['RA'], self.cndhc[n]['dec'] )

            flag_grpmatch = JgemIdGrp.isMatchGroups(cnd['obsids'], self.gids) 
            flag_print = True
            if hastransient == True and (not JgemPlanner.checkHasTransient(cnd['hastransient'])):
                flag_print = True
            elif nonreserved == True and cnd['updated'] != None:
                if group == True and flag_grpmatch == True:
                    flag_print = False
                else:
                    flag_print = True
            elif grep == True:
                pattern = re.compile(grepstr)
                if not pattern.search(showstr):
                    flag_print = False
                elif group == True and flag_grpmatch == False:
                    flag_print = False
            else:
                if group == True and flag_grpmatch == False:
                    flag_print = False
                
            if flag_print == True:
                if number==False:
                    print('%s' % (showstr))
                else:
                    print('%4i %s' % (n, showstr))
            n+=1

    def markReserved(self, candidate, filters, obsdatetime):
        params = {'eventid': self.eventid, 'mode': 'submit', 'obsid': self.obsid,
                  'galid': candidate, 'state': 'Reserved', 'filter': filters,
                  'obsdatetime': obsdatetime, 'observer': self.observer}
        content = self.readProcessorPy(params)

    def markObserved(self, candidate, filters, obsdatetime, depth, hastransient):
        params = {'eventid': self.eventid, 'mode': 'submit', 'obsid': self.obsid,
                  'galid': candidate, 'state': 'Observed', 'filter': filters,
                  'depth': depth, 'obsdatetime': obsdatetime,
                  'observer': self.observer, 'hastransient': hastransient}
        content = self.readProcessorPy(params)

    def eventExists(self):
        for event_in_list in self.events[0]:
            if event_in_list == self.eventid:
                return True
        return False

    def appendObjectOnTargetListSacra(self, num):
        try:
            f = open(TargetListFn, 'a')
        except:
            sys.stderr.write('File open error: %s\n' % (TargetListFn) )
            return(-1)
        cnd = self.candidates[num]
        hexcoord = self.getRaDec(float(cnd['ra']), float(cnd['dec']))
        f.write('#J-GEM target: %s\n' % (datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))
        f.write('%s %s\n' % (cnd['galid'], hexcoord))
        
    def candidateExists(self, candidate):
        for candidate_in_list in self.candidates:
            if candidate_in_list[0] == candidate:
                return True
        return False
    
    def interactiveModeMenu(self):
        print('------ command menu --------------')
        print('(s): show all candidates')
        print('(sg): show all candidates in groups')
        print('(u): update candidate list')
        print('(n): show non-reserved/observed candidates')
        print('(ng): show non-reserved/observed candidates in groups')
        print('(t): show "hastransient" candidates')
        print('(r NUMBER): mark RESERVED for the object with NUMBER')
        print('(p NUMBER): telescope pointing for the object with NUMBER')
        print('(g): show defined groups')
        print('(g group1 group2 ...): set group(s) to be shown')
        print('(e): show all events')
        print('(c EVENTID): change current eventid')
        print('(G STRING): grep candidate list by STRING')
        print('(k): show headers for event and candidate tables')
        print('(h, ?): show this menu')
        print('(q): quit')
        return

    def interactiveModeMainLoop(self):
        self.interactiveModeMenu()
        while(True):
            if self.interactiveWaitKeyInput() == 'quit':
                exit(1)

    # telescope pointing method for SaCRA telescope
    def sacraPointing(self, num):
        target = self.candidates[num]['galid']
        self.appendObjectOnTargetListSacra(num)
        print('%s / %s appended to the tareget list file\n' %
              (target, self.eventid) )
        try:
            subprocess.call(['ltelescope %s' % (target)], shell=True)
        except:
            sys.stderr.write('ltelecope error !\n')
            return(1)

    def showGroupids(self):
        print(self.gids)

    def setGroupids(self, grps):
        tmpset=set([])
        for grp in grps:
            if JgemIdGrp.isDefinedGroupid(grp):
                tmpset.add(grp)
        if len(tmpset) == 0:
            return False
        else:
            self.gids = tmpset.copy()
            return True

    def notImplemented(self):
        print('Not implemented yet. Sorry.')
        return

    def interactiveWaitKeyInput(self):
        IntPattern = re.compile('\d+')
        try:
            com = input('eventid:%s> ' % (self.eventid)).strip()
            obsdatetime = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            try:
                coms=com.split()
            except:
                return('')
            if len(coms) == 0:
                return
            if coms[0] == 'r' and len(coms) >= 2:
                if IntPattern.search(coms[1]):
                    num = int(coms[1])
                    print(num)
                    for band in DEFAULT_BANDS:
                        self.markReserved(self.candidates[num][0], band, obsdatetime)
                        print('%s / %s / %s reserved.' % (self.candidates[num][0], self.eventid, band))
                    self.getCandidates()
            elif coms[0] == 'c' and len(coms) >= 2:
                if self.setCurrentEventid(coms[1]):
                    self.getCandidates()
            elif coms[0] == 'g' and len(coms) >= 2:
                if not self.setGroupids(coms[1:]):
                    print('Error.')
            elif coms[0] == 'g' and len(coms) ==1:
                self.showGroupids()
            elif coms[0] == 'G' and len(coms) >= 2:
                self.showCandidates(number=True, grep=True, grepstr=coms[1])
            elif coms[0] == 's':
                self.showCandidates(number=True)
            elif coms[0] == 'sg':
                self.showCandidates(number=True, group=True)
            elif coms[0] == 'e':
                self.showEvents()
            elif coms[0] == 'u':
                self.notImplemented()
            elif coms[0] == 'n':
                self.showCandidates(number=True, nonreserved=True)
            elif coms[0] == 'ng':
                self.showCandidates(number=True, nonreserved=True, group=True)
            elif coms[0] == 't':
                self.showCandidates(number=True, hastransient=True)
            elif coms[0] == 'k':
                self.showEventTableHeaders()
                self.showCandidateTableHeaders()
            elif coms[0] == 'p' and len(coms) >= 2:
                if IntPattern.search(coms[1]):
                    num = int(coms[1])
                    # change method for each telescope
                    self.sacraPointing(num)
                    return('pointing')
                else:
                    print('Invalid number')
                    return
            elif coms[0] == 'h' or coms[0] == '?':
                self.interactiveModeMenu()
                return 'unmark'
            elif coms[0] == 'q':
                return('quit')
            else:
                return('next')
        except KeyboardInterrupt:
            print('Use "q" to finish the task')
            return ('')

    @staticmethod
    def checkHasTransient(col):
        try:
            colstr = col
        except:
            return(False)
        if colstr == None:
            return(False)
        pattern = re.compile('[Yy][Ee][Ss]')
        if pattern.search(colstr):
            return(True)
        return(False)
    
    @staticmethod
    def getUserPassDir():
        if USERPASSWD_DIR == '':
            try:
                userpasswd_dir = os.environ['HOME']
            except KeyError:
                userpasswd_dir = '.' # useing currentdir
        else:
            userpasswd_dir = USERPASSWD_DIR
        if not os.path.isdir(userpasswd_dir):
            sys.stderr.write('Error. Directory %s not found. Abort.\n')
            raise Exception
        return(userpasswd_dir)
        
    @staticmethod
    def readBasicAuthorizationUserPass():
        userpasswd_fn = '%s/%s' % (JgemPlanner.getUserPassDir(), USERPASSWD_FN)
        try:
            f = open(userpasswd_fn, 'rb')
            userpass = f.read()
        except:
            sys.stderr.write('User-passwd file read error: %s\n' % (userpasswd_fn))
            return(b'')
        return(userpass)
