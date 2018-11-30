#!/usr/bin/env python2
#
#    jgem astronomical coordinate processor
#
#         Ver 1.0  2019/11/29  H. Akitaya

from astropy.coordinates import SkyCoord
import astropy.units as u
import re

class JgemCoord(object):
    def __init__(self):
        self.skycoord=None
    def setDegDeg(self, ra, dec):
        self.skycoord = SkyCoord(ra, dec, unit='deg')
    def getHex(self):
        coordstr = re.sub('[hmd]', ':', self.skycoord.to_string(style='hmsdms'))
        coordstr = re.sub('[s]', '', coordstr)
        return(coordstr)
    def showHex(self):
        print(self.getHex())
    
