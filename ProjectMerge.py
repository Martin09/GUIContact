# -*- coding: utf-8 -*-
"""
Created on Thu Mar 05 18:44:05 2015

@author: Martin Friedl
"""

import numpy as np
import pandas as pd
import os
import tarfile
import pickle as dumper
import StringIO
import autoContact
#import objectexplorer
from IPython.lib import guisupport

version = "0.983"  
    
def merge(cp1, cp2):
    #Merge two projects together, retaining the settings of the first project
    cp3 = cp1
    cp3.paths.extend(cp2.paths) #Add paths
    cp3.settings.extend(cp2.settings) #Add settings
    cp3.fitLogs.extend(cp2.fitLogs) #Add settings
#    cp.paths=[os.path.join(d,p) for p in paths]
    for p in cp2.paths: cp3.imageObjects.append(None) #Append empty images
    return cp3           
    
cp1 = autoContact.ContactProject()
cp1.load('MF-12-ZA_bottom.nwcpr') #Input file

cp2 = autoContact.ContactProject()
cp2.load('MF-12-ZA_top.nwcpr') #Input file

output = merge(cp1, cp2)
#
cp3 = autoContact.ContactProject()
cp3.load('MF-12-ZA-Platelets.nwcpr')
#
output = merge(output, cp3)

#Correct contact/pad layers to all be the same
for i in output.settings:
    i['contactOptions']['padLayer'] = 0
    i['contactOptions']['contLayer'] = 1

# Note: need to use abosolute pathType in ContactProject.save()
output.changePathType("absolute") 
output.save('MF-12-ZA-Merged.nwcpr') #Output file

#execfile("objectexplorer.py")
