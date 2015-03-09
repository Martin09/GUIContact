# -*- coding: utf-8 -*-
"""
Created on Thu Mar 05 18:44:05 2015

@author: Martin Friedl
"""

## Note: need to use abosolute pathType in ContactProject.save()

import numpy as np
import pandas as pd
import os
import tarfile
import pickle as dumper
import StringIO
import autoContact
import objectexplorer
from IPython.lib import guisupport

version = "0.983"

def save(cp,filename):
    cp.version=version
#    p=[os.path.relpath(path,os.path.dirname(filename)) for path in cp.paths] #Relative Paths
    p=[path for path in cp.paths] #Absolute paths
    tar=tarfile.open(filename,mode="w:bz2")
    string1=dumper.dumps(p)
    info1 = tarfile.TarInfo(name="paths")
    info1.size=len(string1)
#        cp.version=version
    tar.addfile(tarinfo=info1, fileobj=StringIO.StringIO(string1))
    for name,obj in [("settings",cp.settings),("descriptor",cp.descriptor),
                     ("exposure",cp.exposureSettings),("fitLogs",cp.fitLogs),("version",cp.version)]:
        string=dumper.dumps(obj)
        info = tarfile.TarInfo(name=name)
        info.size=len(string)
        tar.addfile(tarinfo=info, fileobj=StringIO.StringIO(string))
    tar.close()
    cp.filename=filename
    cp.saved=True

def load(cp,filename):
    tar=tarfile.open(filename,mode="r:bz2")
    cp.filename=filename #Take filename of cp1
    paths=dumper.loads(tar.extractfile("paths").read())
    d=os.path.dirname(filename)
    cp.paths=[os.path.join(d,p) for p in paths] #Merge paths
    cp.settings=dumper.loads(tar.extractfile("settings").read()) #Merge settings
    cp.descriptor=dumper.loads(tar.extractfile("descriptor").read()) #Keep descriptor of cp1
    cp.exposureSettings=dumper.loads(tar.extractfile("exposure").read()) #Keep exposure settings of cp1
    cp.fitLogs=dumper.loads(tar.extractfile("fitLogs").read()) #Keep fitLogs of cp1
    try:
        cp.version=dumper.loads(tar.extractfile("version").read()) #Keep version of cp1
    except KeyError:
        cp.version="<0.970"
    for p in cp.paths: cp.imageObjects.append(None)
    tar.close()
    cp.saved=True
    
    
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
cp1.load('4ptAbs.nwcpr')

cp2 = autoContact.ContactProject()
cp2.load('4ptAbs_1gate.nwcpr')

cp3 = autoContact.ContactProject()
cp3.load('4ptAbs_2Gate_0,1_0,150.nwcpr')

cp4 = autoContact.ContactProject()
cp4.load('4ptAbs_2Gate_0,2_0,150.nwcpr')

tmp1 = merge(cp1, cp2)
tmp2 = merge(cp3, cp4)
output = merge(tmp1,tmp2)
output.save('MF-05-IA_Merged.nwcpr')

#execfile("objectexplorer.py")
