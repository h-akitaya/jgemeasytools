#!/usr/bin/env python3
#
#
#     J-GEM obs-id, group definition
#
#    Ver 1.0  2018/11/29  H. Akitaya
#

import os, sys
import re

class JgemIdGrp(object):
   def __init__():
      pass

   @staticmethod
   def getDefinedGroupids():
      grps = set([])
      for grpid in JgemIdGrp.table:
         grps.add(JgemIdGrp.table[grpid])
         # print(JgemIdGrp.table[grpid]) #Debug
      return grps

   @staticmethod
   def getDefinedObsids():
       return JgemIdGrp.table.keys()

   @staticmethod
   def isDefinedGroupid(grps):
      for grp in grps:
         for grpid in JgemIdGrp.table:
            if grp == JgemIdGrp.table[grpid]:
               return True
      return False

   @staticmethod
   def isMatchGroups(line, grp_comp):
      grp_match = grp_comp.intersection(JgemIdGrp.checkGroups(line))
      # print(len(grp_match), grp_comp, (JgemIdGrp.checkGroups(line))) #Debug
      if len(grp_match) == 0:
         return False
      return True

   @staticmethod
   def checkGroups(line):
       groups = set([])
       for obsid in JgemIdGrp.table:
           pattern = re.compile(obsid)
           if pattern.search(line):
               groups.add(JgemIdGrp.table[obsid])
       return groups

JgemIdGrp.table = {'Kanata-HONIR-OPT': 'A',
                   'Kanata-HONIR-IRA': 'A',
                   'Kanata': 'A',
                   'Kanata-HONIR': 'A',
                   'Kanata-HOWPol': 'A',
                   'MITSuME-Akeno': 'B',
                   'MITSuME-Okayama': 'B',
                   'OAOWFC': 'C',
                   'SaCRA-MuSaSHI': 'B',
                   'BandC-Tripol': 'B',
                   'HSC': 'A',
                   'Undef': 'X'
                   }

if __name__ == '__main__':
    line = sys.argv[1]
#    print(JgemIdGrp.table)
    print(JgemIdGrp.checkGroups(line))



