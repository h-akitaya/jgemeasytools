#!/usr/bin/env python3
#
#
#   Alt, Az, HA calculation
#
#         getaltazha.py
#
#    Ver  1.0   2018/11/29  H. Akitaya
#

# to be defined in jgeminfo.py
#LATITUDE=35.86
#LONGITUDE=139.6
#HEIGHT=0.0
#TZ=+9

import sys
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
import jgeminfo
import datetime

class ObjAltAzHa(object):
    def __init__(self, ra_deg, dec_deg, time):
        self.loc = self.getEarthLocation()
        self.objcoord = SkyCoord(ra_deg, dec_deg, unit=(u.deg,u.deg), frame='icrs')
        self.time = time
        self.time.delta_ut1_utc = 0.
        self.utcoffset = self.getUTCOffset()
        
    def getEarthLocation(self):
        return EarthLocation(lat=jgeminfo.LATITUDE*u.deg,
                             lon=jgeminfo.LONGITUDE*u.deg, 
                             height=jgeminfo.HEIGHT*u.m)
    def getUTCOffset(self):
        return(jgeminfo.TZ*u.hour)

    def getAltAz(self):
        time = self.time - self.utcoffset
#        print(time)
        obj_altaz = self.objcoord.transform_to(AltAz(obstime=self.time, 
                                                     location=self.loc))
        alt = obj_altaz.alt
        alt.wrap_at('180d', inplace=True)
        az = obj_altaz.az
        az.wrap_at('180d', inplace=True)
        return(alt.degree, az.degree)

    def getSiderialTimeHA(self):
        sdr = self.time.sidereal_time('mean', longitude=jgeminfo.LONGITUDE).hourangle
        return sdr

    def getHA(self):
        sdr = self.getSiderialTimeHA()
        objra = self.objcoord.ra.hourangle
        print(objra)
        ha = sdr - objra
        if ha < -12:
            ha+=24
        elif ha > 12:
            ha-=24
        return(ha)

if __name__ == '__main__':
#    if len(sys.args != 3):
#        exit(1)
#    print(sys.argv[1])
    now = Time.now()
    print(now)
    objcoord = SkyCoord(sys.argv[1], sys.argv[2], unit=(u.hourangle,u.deg), frame='icrs')
    altaz=ObjAltAzHa(float(sys.argv[1]), float(sys.argv[2]), now)
#    print(altaz.getSiderialTime(now))
    alt, az = altaz.getAltAz()
    ha = altaz.getHA()
    print("Alt: %6.1f, Az: %6.1f, HA: %6.1f" % (alt, az, ha))

    
    
