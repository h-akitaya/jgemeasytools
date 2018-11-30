#!/usr/bin/env python3
#
#
#   J-GEM easy sky map
#
#    Ver  1.0   2018/11/29  H. Akitaya
#

import os, sys

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime

from astropy.time import Time


from objaltazha import ObjAltAzHa
import jgemplanner

class ObsApparentCoords(object):
    def __init__(self, jgp):
        self.jgp = jgp # JgemPlanner instance
        self.obstable = []
        
    def makeTable(self):
        time = Time(datetime.datetime.utcnow(), scale='utc')
        for cnd in self.jgp.candidates:
            alt, az, ha = ObsApparentCoords.getAltAzHa(cnd['ra'], cnd['dec'], time)
#            self.obstable.append([cnd['galid'], cnd['ra'], cnd['dec'], alt, az, ha])
            self.obstable.append([cnd['ra'], cnd['dec'], alt, az, ha])
        self.npobstable=np.array(self.obstable)
        print(self.npobstable)

    def plotSkyMap(self):
        fig, ax = plt.subplots(1,1)
        has = self.npobstable[:,4]
        decs = self.npobstable[:,1]
#        print(x, y)
        plt.title(self.jgp.eventid)
        plt.xlabel('HA')
        plt.ylabel('deg')
        plt.xlim(-12, 12)
        plt.ylim(-20, 90)
#        plt.xticks(np.arange(-12, 12.1, 2))
        plt.plot(has, decs, 'bo', markersize=4)
        i=0
        for ha in has:
            ax.annotate(str(i), xy=(ha, decs[i]), color='black')
            i+=1
        plt.show()
        

    @staticmethod
    def getFlags(cnd):
        flags = {'hastransient':False, 'observed': False, 'category': False}
        pattern = re.compile('[Yy][Ee][Ss]')
        if pattern.match(cnd['hastransient']):
            flags['hastransient'] = True
        if cnd['updated'] != None:
            if cnd['updated'] != 'None':
                flags['observed'] = True
        return(flags)
    
    @staticmethod
    def getAltAzHa(ra_deg, dec_deg, time):
        aah = ObjAltAzHa(ra_deg, dec_deg, time)
        alt, az = aah.getAltAz()
        ha = aah.getHA()
        return(alt, az, ha)
    
if __name__ == '__main__':
    jgp = jgemplanner.JgemPlanner()
    jgp.getEvents()
    latest_event = jgp.events[0]['eventid']
    jgp.setCurrentEventid(latest_event)
    jgp.getCandidates()

    jgp.showCandidates()
    oac = ObsApparentCoords(jgp)
    oac.makeTable()
    oac.plotSkyMap()
