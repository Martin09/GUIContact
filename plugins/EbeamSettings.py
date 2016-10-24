# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 16:13:43 2013

@author: rueffer

EXAMPLE:
-------------------------------------------------------------------
defExposureSettings={"beam":"150nA","dose":1100,"res":0.025,
                  "alpha":0,"beta":31.,"eta":0.65,"ignoreHeightError":False,
                  "doPEC":True,"camps":0}
beams={
    "100nA":"100na_300um.beam_100",
    "150nA":"150na_300um.beam_100"
    }

beamsizes={
    "150nA":0.075,
    "100nA":0.050,
    }
minRes=0.001
maxRes=0.050
-------------------------------------------------------------------
"""

defExposureSettings={"beam":"200nA","dose":1000.,"res":0.075,"mPEC_beamsize":0.1,
                  "alpha":0,"beta":31.,"eta":0.65,"ignoreHeightError":False,
                  "doPEC":False,"camps":0,"multiPEC":False,"negativeMarker":False}
beams={
    "100nA":"100na_300um.beam_100",
    "100pA":"100pa_300um.beam_100",
    "10nA":"10na_300um.beam_100",
    "150nA":"150na_300um.beam_100",
    "15nA":"15na_300um.beam_100",
    "1nA":"1na_300um.beam_100",
    "200nA":"200na_300um.beam_100",
    "200pA":"200pa_300um.beam_100",
    "20nA":"20na_300um.beam_100",
    "2nA":"2na_300um.beam_100",
    "30nA":"30na_300um.beam_100",
    "3nA":"3na_300um.beam_100",
    "40nA":"40na_300um.beam_100",
    "500pA":"500pa_300um.beam_100",
    "50nA":"50na_300um.beam_100",
    "5nA":"5na_300um.beam_100",
    "700pA":"700pa_300um.beam_100",
    "70nA":"70na_300um.beam_100",
    "7.5nA":"7na5_300um.beam_100"
    }

beamsizes={
    "200nA":0.101752,
    "150nA":0.077352,
    "100nA":0.052952,
    "70nA":0.038312,
    "50nA":0.028552,
    "40nA":0.023672,
    "30nA":0.018792,
    "20nA":0.013912,
    "15nA":0.011472,
    "10nA":0.009032,
    "7.5nA":0.007812,
    "5nA":0.006592,
    "3nA":0.005616,
    "2nA":0.005128,
    "1nA":0.004640,
    }
defExposureSettings.update({"beamsize":beamsizes[defExposureSettings["beam"]]}) 
    
#MSF for LB: not sure what this is, but it has to be specified correctly
#Martin: MSF = Multiple Stepping Factor,
#See EPFL THÈSE NO 4809 (2010) for more details
MSF={
    0.1:(13,205),
    0.075:(10,154),
    0.05:(7,103),
    0.025:(4,52),
    0.020:(3,41),
    0.015:(2,31),
    0.010:(2,21),
    0.005:(1,11),  #Added by Martin
    0.0025:(1,6),  #Added by Martin
    0.00125:(1,3), #Added by Martin
    }
defExposureSettings.update({"MSF":MSF[defExposureSettings["res"]]}) 

minRes=0.00125
maxRes=0.100

defExposureSettings.update({"PECLayers":[0]}) 