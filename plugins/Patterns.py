# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 11:17:55 2012

@author: rueffer
"""
import numpy as np
import time
from PatternGenerator import *
from shapely.geometry import Polygon as ShapelyPolygon
import shapely.geometry

# Must always be (self,name,library,..*args,unitFact=1E3,**kwargs)
# Please indicate the name of the pattern and give a dict with name allPatterns

## TODO: "Private" variables to faciLaitate creation

#===============================================================================
# defined for NanoWire object:
# "top":(10,10)
# "bottom":(-10,-10)
#===============================================================================
    
class NanoWire(NanoWireTemplate):
    def __init__(self,name,descriptor=None,**kwargs): 
        self.descriptor=descriptor    # ensures that the default is set, if no descriptor is given   
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "textsize":3.,
        "spacing":5.,
        "width":0.5,
        "text":""
        })
        super(NanoWire,self).__init__(name,descriptor=descriptor,layer=self.descriptor.commentLayer,**kwargs)
    
    def make(self):
        if self.end1[1]>self.end2[1]:
            top=np.array(self.end1)
            bot=np.array(self.end2)
        else:
            top=np.array(self.end2)
            bot=np.array(self.end1)
        center=(top+bot)/2.
        d=(top-bot)
        length=np.sqrt(np.dot(d,d))
        angle=np.mod((-np.arcsin(np.cross(d/length,[0.,1.]))*180./np.pi),180)
        x=-self.spacing
        nw=Structure(self.name+"_cont")
        if self.text == "":
            text = self.name
        else:
            text = self.text
        text=Text(text,height=self.textsize,ha="center",va="bottom")
        nw.insertElement(Rectangle(self.width,length),layer=self.layer)
        nw.insertElement(text,xy=(x,0),angle=270,layer=self.layer)
        self.insertElement(nw,xy=center,angle=angle)
        
        
class Antenna(NanoWireTemplate):
    def __init__(self,name,descriptor=None,**kwargs):
        self.descriptor=descriptor    # ensures that the default is set, if no descriptor is given   
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "thickSquare":50,
        "lates":300,
        "radius":0.2,
        "number":1,
        "vertDistance":0.84,
        "radDistance":0.3,
        "layerDots":self.descriptor.defExposureLayer+1,
        "textHeight":50.
        })
        super(Antenna,self).__init__(name,descriptor=descriptor,**kwargs)
        
    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        t=self.name.split("_")[0]
        contacts.insertElement(Text(t,va="bottom",ha="right",height=self.textHeight),xy=[self.lates/2+self.thickSquare+self.textHeight+20,+self.lates/2+self.thickSquare],layer=self.layer,angle=270)
        contacts.insertElement(Text(t,va="bottom",ha="right",height=20),xy=[90,60],layer=self.layer,angle=270)
		
    def make(self):
        top,bot,center,d,length,angle=self.getCoords()
        center=(top+bot)/2.
        rot=rotMatrix(angle)
        number=int(self.number)
        zero1=np.array([-self.radDistance/2.,-self.vertDistance*(number-1)/2.])
        zero2=np.array([self.radDistance/2.,-self.vertDistance*(number-1)/2.])
        rectangle1=[[-self.lates/2-self.thickSquare,self.lates/2],[self.lates/2+self.thickSquare,self.lates/2],[self.lates/2+self.thickSquare,self.lates/2+self.thickSquare],[-self.lates/2-self.thickSquare,self.lates/2+self.thickSquare]]
      	rectangle2=[[-self.lates/2-self.thickSquare,-self.lates/2],[self.lates/2+self.thickSquare,-self.lates/2],[self.lates/2+self.thickSquare,-self.lates/2-self.thickSquare],[-self.lates/2-self.thickSquare,-self.lates/2-self.thickSquare]]
        rectangle3=[[-self.lates/2-self.thickSquare,self.lates/2],[-self.lates/2,self.lates/2],[-self.lates/2,-self.lates/2],[-self.lates/2-self.thickSquare,-self.lates/2]]
        rectangle4=[[self.lates/2,self.lates/2],[self.lates/2+self.thickSquare,self.lates/2],[self.lates/2+self.thickSquare,-self.lates/2],[self.lates/2,-self.lates/2]]
        recsmall1=[[-60,50],[60,50],[60,60],[-60,60]]
        recsmall2=[[-60,-50],[60,-50],[60,-60],[-60,-60]]
        recsmall3=[[60,50],[60,-50],[50,-50],[50,50]]
        recsmall4=[[-60,50],[-60,-50],[-50,-50],[-50,50]]
        contacts=Structure(self.name+"_contacts")
        for i in range(number):
            p1=zero1+np.array([0.,self.vertDistance*i])
            contacts.insertElement(Circle(self.radius/2.),xy=p1,layer=self.layerDots)
            p2=zero2+np.array([0.,self.vertDistance*i])
            contacts.insertElement(Circle(self.radius/2.),xy=p2,layer=self.layerDots)
        contacts.insertElement(Polygon(recsmall1),layer=self.layer)
        contacts.insertElement(Polygon(recsmall2),layer=self.layer)
        contacts.insertElement(Polygon(recsmall3),layer=self.layer)
        contacts.insertElement(Polygon(recsmall4),layer=self.layer)
        contacts.insertElement(Polygon(rectangle1),layer=self.layer)
        contacts.insertElement(Polygon(rectangle2),layer=self.layer)
        contacts.insertElement(Polygon(rectangle3),layer=self.layer)
        contacts.insertElement(Polygon(rectangle4),layer=self.layer)
        self.createText(contacts)
        self.insertElement(contacts,angle=angle,xy=center)
		
    def getDefLayers(self):
        return super(Antenna,self).getDefLayers().union(set([self.layerDots]))
        
        
class AntennaTriang(NanoWireTemplate):
    def __init__(self,name,descriptor=None,**kwargs):
        self.descriptor=descriptor    # ensures that the default is set, if no descriptor is given   
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "thickSquare":50,
     	"latesSquare":300,
        "number":5,
        "textHeight":50.,
        "lates":0.2,
        "vertDistance":1.13,
        "antennaDist":0.2,
        "layerTriangols":self.descriptor.defExposureLayer+1
        })
        super(AntennaTriang,self).__init__(name,descriptor=descriptor,**kwargs)
        
    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        t=self.name.split("_")[0]
        contacts.insertElement(Text(t,va="bottom",ha="right",height=self.textHeight),xy=[self.latesSquare/2+self.thickSquare+self.textHeight+20,+self.latesSquare/2+self.thickSquare],layer=self.layer,angle=270)
        contacts.insertElement(Text(t,va="bottom",ha="right",height=20),xy=[90,60],layer=self.layer,angle=270)
		
    def make(self):
        top,bot,center,d,length,angle=self.getCoords()
        center=(top+bot)/2.
        rot=rotMatrix(angle)
        number=int(self.number)
        zero1=np.array([self.antennaDist/2.,-self.vertDistance*(number-1)/2.])
        zero2=np.array([-self.antennaDist/2.,-self.vertDistance*(number-1)/2.])
        rectangle1=[[-self.latesSquare/2-self.thickSquare,self.latesSquare/2],[self.latesSquare/2+self.thickSquare,self.latesSquare/2],[self.latesSquare/2+self.thickSquare,self.latesSquare/2+self.thickSquare],[-self.latesSquare/2-self.thickSquare,self.latesSquare/2+self.thickSquare]]
      	rectangle2=[[-self.latesSquare/2-self.thickSquare,-self.latesSquare/2],[self.latesSquare/2+self.thickSquare,-self.latesSquare/2],[self.latesSquare/2+self.thickSquare,-self.latesSquare/2-self.thickSquare],[-self.latesSquare/2-self.thickSquare,-self.latesSquare/2-self.thickSquare]]
        rectangle3=[[-self.latesSquare/2-self.thickSquare,self.latesSquare/2],[-self.latesSquare/2,self.latesSquare/2],[-self.latesSquare/2,-self.latesSquare/2],[-self.latesSquare/2-self.thickSquare,-self.latesSquare/2]]
        rectangle4=[[self.latesSquare/2,self.latesSquare/2],[self.latesSquare/2+self.thickSquare,self.latesSquare/2],[self.latesSquare/2+self.thickSquare,-self.latesSquare/2],[self.latesSquare/2,-self.latesSquare/2]]
        recsmall1=[[-60,50],[60,50],[60,60],[-60,60]]
        recsmall2=[[-60,-50],[60,-50],[60,-60],[-60,-60]]
        recsmall3=[[60,50],[60,-50],[50,-50],[50,50]]
        recsmall4=[[-60,50],[-60,-50],[-50,-50],[-50,50]]
        contacts=Structure(self.name+"_contacts")
        for i in range(number):
            p1=zero1+np.array([0.,self.vertDistance*i])
            t1=[[p1[0],p1[1]],[p1[0]+self.lates*np.sqrt(3)/2,p1[1]-self.lates/2],[p1[0]+self.lates*np.sqrt(3)/2,p1[1]+self.lates/2],[p1[0],p1[1]]]
            tri1=myRotate(np.array(t1),180)
            contacts.insertElement(Polygon(tri1),layer=self.layerTriangols)
            p2=zero2+np.array([0.,self.vertDistance*i])
            t2=[[p2[0],p2[1]],[p2[0]-self.lates*np.sqrt(3)/2,p2[1]-self.lates/2],[p2[0]-self.lates*np.sqrt(3)/2,p2[1]+self.lates/2],[p2[0],p2[1]]]
            tri2=myRotate(np.array(t2),180)
            contacts.insertElement(Polygon(tri2),layer=self.layerTriangols)
        contacts.insertElement(Polygon(recsmall1),layer=self.layer)
        contacts.insertElement(Polygon(recsmall2),layer=self.layer)
        contacts.insertElement(Polygon(recsmall3),layer=self.layer)
        contacts.insertElement(Polygon(recsmall4),layer=self.layer)
        contacts.insertElement(Polygon(rectangle1),layer=self.layer)
        contacts.insertElement(Polygon(rectangle2),layer=self.layer)
        contacts.insertElement(Polygon(rectangle3),layer=self.layer)
        contacts.insertElement(Polygon(rectangle4),layer=self.layer)
        self.createText(contacts)
        self.insertElement(contacts,angle=angle,xy=center)
		
    def getDefLayers(self):
        return super(AntennaTriang,self).getDefLayers().union(set([self.layerTriangols]))
        
        
class DirEmis5(NanoWireTemplate):
    def __init__(self,name,descriptor=None,**kwargs):
        self.descriptor=descriptor    # ensures that the default is set, if no descriptor is given   
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "thickSquare":50,
     	"latesSquare":300,
        "textHeight":50.,
        "vertDistance":3,
        "barDist":0.2,
        "layerBars":self.descriptor.defExposureLayer+1
        })
        super(DirEmis5,self).__init__(name,descriptor=descriptor,**kwargs)
        
    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        t=self.name.split("_")[0]
        contacts.insertElement(Text(t,va="bottom",ha="right",height=self.textHeight),xy=[self.latesSquare/2+self.thickSquare+self.textHeight+20,+self.latesSquare/2+self.thickSquare],layer=self.layer,angle=270)
        contacts.insertElement(Text(t,va="bottom",ha="right",height=20),xy=[90,60],layer=self.layer,angle=270)
		
    def make(self):
        top,bot,center,d,length,angle=self.getCoords()
        center=(top+bot)/2.
        rot=rotMatrix(angle)
        number=5
        rectangle1=[[-self.latesSquare/2-self.thickSquare,self.latesSquare/2],[self.latesSquare/2+self.thickSquare,self.latesSquare/2],[self.latesSquare/2+self.thickSquare,self.latesSquare/2+self.thickSquare],[-self.latesSquare/2-self.thickSquare,self.latesSquare/2+self.thickSquare]]
      	rectangle2=[[-self.latesSquare/2-self.thickSquare,-self.latesSquare/2],[self.latesSquare/2+self.thickSquare,-self.latesSquare/2],[self.latesSquare/2+self.thickSquare,-self.latesSquare/2-self.thickSquare],[-self.latesSquare/2-self.thickSquare,-self.latesSquare/2-self.thickSquare]]
        rectangle3=[[-self.latesSquare/2-self.thickSquare,self.latesSquare/2],[-self.latesSquare/2,self.latesSquare/2],[-self.latesSquare/2,-self.latesSquare/2],[-self.latesSquare/2-self.thickSquare,-self.latesSquare/2]]
        rectangle4=[[self.latesSquare/2,self.latesSquare/2],[self.latesSquare/2+self.thickSquare,self.latesSquare/2],[self.latesSquare/2+self.thickSquare,-self.latesSquare/2],[self.latesSquare/2,-self.latesSquare/2]]
        recsmall1=[[-60,50],[60,50],[60,60],[-60,60]]
        recsmall2=[[-60,-50],[60,-50],[60,-60],[-60,-60]]
        recsmall3=[[60,50],[60,-50],[50,-50],[50,50]]
        recsmall4=[[-60,50],[-60,-50],[-50,-50],[-50,50]]
        contacts=Structure(self.name+"_contacts")
        zero1=np.array([self.barDist/2.,0])
        zero2=np.array([-self.barDist/2.,0])
        b11=[[zero1[0],zero1[1]+self.vertDistance*2],[zero1[0],zero1[1]+0.06+self.vertDistance*2],[zero1[0]+0.05,zero1[1]+0.06+self.vertDistance*2],[zero1[0]+0.05,zero1[1]+self.vertDistance*2]]
        b12=[[zero1[0],zero1[1]+self.vertDistance],[zero1[0],zero1[1]+0.06+self.vertDistance],[zero1[0]+0.25,zero1[1]+0.06+self.vertDistance],[zero1[0]+0.25,zero1[1]+self.vertDistance]]
        b13=[[zero1[0],zero1[1]],[zero1[0],zero1[1]+0.06],[zero1[0]+0.5,zero1[1]+0.06],[zero1[0]+0.5,zero1[1]]]
        b14=[[zero1[0],zero1[1]-self.vertDistance],[zero1[0],zero1[1]-0.06-self.vertDistance],[zero1[0]+0.75,zero1[1]-0.06-self.vertDistance],[zero1[0]+0.75,zero1[1]-self.vertDistance]]
        b15=[[zero1[0],zero1[1]-self.vertDistance*2],[zero1[0],zero1[1]-0.06-self.vertDistance*2],[zero1[0]+1,zero1[1]-0.06-self.vertDistance*2],[zero1[0]+1,zero1[1]-self.vertDistance*2]]
        b21=[[zero2[0],zero2[1]+self.vertDistance*2],[zero2[0],zero2[1]+0.06+self.vertDistance*2],[zero2[0]-0.05,zero2[1]+0.06+self.vertDistance*2],[zero2[0]-0.05,zero2[1]+self.vertDistance*2]]
        b22=[[zero2[0],zero2[1]+self.vertDistance],[zero2[0],zero2[1]+0.06+self.vertDistance],[zero2[0]-0.25,zero2[1]+0.06+self.vertDistance],[zero2[0]-0.25,zero2[1]+self.vertDistance]]
        b23=[[zero2[0],zero2[1]],[zero2[0],zero2[1]+0.06],[zero2[0]-0.5,zero2[1]+0.06],[zero2[0]-0.5,zero2[1]]]
        b24=[[zero2[0],zero2[1]-self.vertDistance],[zero2[0],zero2[1]-0.06-self.vertDistance],[zero2[0]-0.75,zero2[1]-0.06-self.vertDistance],[zero2[0]-0.75,zero2[1]-self.vertDistance]]
        b25=[[zero2[0],zero2[1]-self.vertDistance*2],[zero2[0],zero2[1]-0.06-self.vertDistance*2],[zero2[0]-1,zero2[1]-0.06-self.vertDistance*2],[zero2[0]-1,zero2[1]-self.vertDistance*2]]
        contacts.insertElement(Polygon(recsmall1),layer=self.layer)
        contacts.insertElement(Polygon(recsmall2),layer=self.layer)
        contacts.insertElement(Polygon(recsmall3),layer=self.layer)
        contacts.insertElement(Polygon(recsmall4),layer=self.layer)
        contacts.insertElement(Polygon(rectangle1),layer=self.layer)
        contacts.insertElement(Polygon(rectangle2),layer=self.layer)
        contacts.insertElement(Polygon(rectangle3),layer=self.layer)
        contacts.insertElement(Polygon(rectangle4),layer=self.layer)
        contacts.insertElement(Polygon(b11),layer=self.layerBars)
        contacts.insertElement(Polygon(b12),layer=self.layerBars)
        contacts.insertElement(Polygon(b13),layer=self.layerBars)
        contacts.insertElement(Polygon(b14),layer=self.layerBars)
        contacts.insertElement(Polygon(b15),layer=self.layerBars)
        contacts.insertElement(Polygon(b21),layer=self.layerBars)
        contacts.insertElement(Polygon(b22),layer=self.layerBars)
        contacts.insertElement(Polygon(b23),layer=self.layerBars)
        contacts.insertElement(Polygon(b24),layer=self.layerBars)
        contacts.insertElement(Polygon(b25),layer=self.layerBars)
        self.createText(contacts)
        self.insertElement(contacts,angle=angle,xy=center)
		
    def getDefLayers(self):
        return super(DirEmis5,self).getDefLayers().union(set([self.layerBars]))
        
        
class DirEmis4(NanoWireTemplate):
    def __init__(self,name,descriptor=None,**kwargs):
        self.descriptor=descriptor    # ensures that the default is set, if no descriptor is given   
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "thickSquare":50,
     	"latesSquare":300,
        "textHeight":50.,
        "vertDistance":3,
        "barDist":0.2,
        "layerBars":self.descriptor.defExposureLayer+1
        })
        super(DirEmis4,self).__init__(name,descriptor=descriptor,**kwargs)
        
    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        t=self.name.split("_")[0]
        contacts.insertElement(Text(t,va="bottom",ha="right",height=self.textHeight),xy=[self.latesSquare/2+self.thickSquare+self.textHeight+20,+self.latesSquare/2+self.thickSquare],layer=self.layer,angle=270)
        contacts.insertElement(Text(t,va="bottom",ha="right",height=20),xy=[90,60],layer=self.layer,angle=270)
		
    def make(self):
        top,bot,center,d,length,angle=self.getCoords()
        center=(top+bot)/2.
        rot=rotMatrix(angle)
        number=4
        rectangle1=[[-self.latesSquare/2-self.thickSquare,self.latesSquare/2],[self.latesSquare/2+self.thickSquare,self.latesSquare/2],[self.latesSquare/2+self.thickSquare,self.latesSquare/2+self.thickSquare],[-self.latesSquare/2-self.thickSquare,self.latesSquare/2+self.thickSquare]]
      	rectangle2=[[-self.latesSquare/2-self.thickSquare,-self.latesSquare/2],[self.latesSquare/2+self.thickSquare,-self.latesSquare/2],[self.latesSquare/2+self.thickSquare,-self.latesSquare/2-self.thickSquare],[-self.latesSquare/2-self.thickSquare,-self.latesSquare/2-self.thickSquare]]
        rectangle3=[[-self.latesSquare/2-self.thickSquare,self.latesSquare/2],[-self.latesSquare/2,self.latesSquare/2],[-self.latesSquare/2,-self.latesSquare/2],[-self.latesSquare/2-self.thickSquare,-self.latesSquare/2]]
        rectangle4=[[self.latesSquare/2,self.latesSquare/2],[self.latesSquare/2+self.thickSquare,self.latesSquare/2],[self.latesSquare/2+self.thickSquare,-self.latesSquare/2],[self.latesSquare/2,-self.latesSquare/2]]
        recsmall1=[[-60,50],[60,50],[60,60],[-60,60]]
        recsmall2=[[-60,-50],[60,-50],[60,-60],[-60,-60]]
        recsmall3=[[60,50],[60,-50],[50,-50],[50,50]]
        recsmall4=[[-60,50],[-60,-50],[-50,-50],[-50,50]]
        contacts=Structure(self.name+"_contacts")
        zero1=np.array([self.barDist/2.,-self.vertDistance/2+0.5])
        zero2=np.array([-self.barDist/2.,-self.vertDistance/2+0.5])
        b11=[[zero1[0],zero1[1]+self.vertDistance*2],[zero1[0],zero1[1]+0.06+self.vertDistance*2],[zero1[0]+0.11,zero1[1]+0.06+self.vertDistance*2],[zero1[0]+0.11,zero1[1]+self.vertDistance*2]]
        b12=[[zero1[0],zero1[1]+self.vertDistance],[zero1[0],zero1[1]+0.06+self.vertDistance],[zero1[0]+0.13,zero1[1]+0.06+self.vertDistance],[zero1[0]+0.13,zero1[1]+self.vertDistance]]
        b13=[[zero1[0],zero1[1]],[zero1[0],zero1[1]+0.06],[zero1[0]+0.15,zero1[1]+0.06],[zero1[0]+0.15,zero1[1]]]
        b14=[[zero1[0],zero1[1]-self.vertDistance],[zero1[0],zero1[1]-0.06-self.vertDistance],[zero1[0]+0.17,zero1[1]-0.06-self.vertDistance],[zero1[0]+0.17,zero1[1]-self.vertDistance]]
        b21=[[zero2[0],zero2[1]+self.vertDistance*2],[zero2[0],zero2[1]+0.06+self.vertDistance*2],[zero2[0]-0.11,zero2[1]+0.06+self.vertDistance*2],[zero2[0]-0.11,zero2[1]+self.vertDistance*2]]
        b22=[[zero2[0],zero2[1]+self.vertDistance],[zero2[0],zero2[1]+0.06+self.vertDistance],[zero2[0]-0.13,zero2[1]+0.06+self.vertDistance],[zero2[0]-0.13,zero2[1]+self.vertDistance]]
        b23=[[zero2[0],zero2[1]],[zero2[0],zero2[1]+0.06],[zero2[0]-0.15,zero2[1]+0.06],[zero2[0]-0.15,zero2[1]]]
        b24=[[zero2[0],zero2[1]-self.vertDistance],[zero2[0],zero2[1]-0.06-self.vertDistance],[zero2[0]-0.17,zero2[1]-0.06-self.vertDistance],[zero2[0]-0.17,zero2[1]-self.vertDistance]]
        contacts.insertElement(Polygon(recsmall1),layer=self.layer)
        contacts.insertElement(Polygon(recsmall2),layer=self.layer)
        contacts.insertElement(Polygon(recsmall3),layer=self.layer)
        contacts.insertElement(Polygon(recsmall4),layer=self.layer)
        contacts.insertElement(Polygon(rectangle1),layer=self.layer)
        contacts.insertElement(Polygon(rectangle2),layer=self.layer)
        contacts.insertElement(Polygon(rectangle3),layer=self.layer)
        contacts.insertElement(Polygon(rectangle4),layer=self.layer)
        contacts.insertElement(Polygon(b11),layer=self.layerBars)
        contacts.insertElement(Polygon(b12),layer=self.layerBars)
        contacts.insertElement(Polygon(b13),layer=self.layerBars)
        contacts.insertElement(Polygon(b14),layer=self.layerBars)
        contacts.insertElement(Polygon(b21),layer=self.layerBars)
        contacts.insertElement(Polygon(b22),layer=self.layerBars)
        contacts.insertElement(Polygon(b23),layer=self.layerBars)
        contacts.insertElement(Polygon(b24),layer=self.layerBars)
        self.createText(contacts)
        self.insertElement(contacts,angle=angle,xy=center)
		
    def getDefLayers(self):
        return super(DirEmis4,self).getDefLayers().union(set([self.layerBars]))
        
class YagiUda(NanoWireTemplate):
    def __init__(self,name,descriptor=None,**kwargs):
        self.descriptor=descriptor    # ensures that the default is set, if no descriptor is given   
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "thickSquare":50,
     	"latesSquare":300,
        "textHeight":80.,
        "layerBars":self.descriptor.defExposureLayer+1
        })
        super(YagiUda,self).__init__(name,descriptor=descriptor,**kwargs)
        
    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        t=self.name.split("_")[0]
        contacts.insertElement(Text(t,va="bottom",ha="right",height=self.textHeight),xy=[self.latesSquare/2+self.thickSquare+self.textHeight+20,+self.latesSquare/2+self.thickSquare],layer=self.layer,angle=270)
        contacts.insertElement(Text(t,va="bottom",ha="right",height=20),xy=[90,60],layer=self.layer,angle=270)
		
    def make(self):
        top,bot,center,d,length,angle=self.getCoords()
        center=(top+bot)/2.
        rot=rotMatrix(angle)
        rectangle1=[[-self.latesSquare/2-self.thickSquare,self.latesSquare/2],[self.latesSquare/2+self.thickSquare,self.latesSquare/2],[self.latesSquare/2+self.thickSquare,self.latesSquare/2+self.thickSquare],[-self.latesSquare/2-self.thickSquare,self.latesSquare/2+self.thickSquare]]
      	rectangle2=[[-self.latesSquare/2-self.thickSquare,-self.latesSquare/2],[self.latesSquare/2+self.thickSquare,-self.latesSquare/2],[self.latesSquare/2+self.thickSquare,-self.latesSquare/2-self.thickSquare],[-self.latesSquare/2-self.thickSquare,-self.latesSquare/2-self.thickSquare]]
        rectangle3=[[-self.latesSquare/2-self.thickSquare,self.latesSquare/2],[-self.latesSquare/2,self.latesSquare/2],[-self.latesSquare/2,-self.latesSquare/2],[-self.latesSquare/2-self.thickSquare,-self.latesSquare/2]]
        rectangle4=[[self.latesSquare/2,self.latesSquare/2],[self.latesSquare/2+self.thickSquare,self.latesSquare/2],[self.latesSquare/2+self.thickSquare,-self.latesSquare/2],[self.latesSquare/2,-self.latesSquare/2]]
        recsmall1=[[-60,50],[60,50],[60,60],[-60,60]]
        recsmall2=[[-60,-50],[60,-50],[60,-60],[-60,-60]]
        recsmall3=[[60,50],[60,-50],[50,-50],[50,50]]
        recsmall4=[[-60,50],[-60,-50],[-50,-50],[-50,50]]
        contacts=Structure(self.name+"_contacts")
        zero1=np.array([0,0])
        zero2=np.array([0,0])
        b1=[[zero1[0]-0.03-0.185,zero1[1]-0.174/2],[zero1[0]-0.03-0.185,zero1[1]+0.174/2],[zero1[0]-0.09-0.185,zero1[1]+0.174/2],[zero1[0]-0.09-0.185,zero1[1]-0.174/2]]
        b2=[[zero1[0]+0.03+0.205,zero1[1]-0.13/2],[zero1[0]+0.03+0.205,zero1[1]+0.13/2],[zero1[0]+0.09+0.205,zero1[1]+0.13/2],[zero1[0]+0.09+0.205,zero1[1]-0.13/2]]
        b3=[[zero1[0]+0.5,zero1[1]-0.13/2],[zero1[0]+0.5,zero1[1]+0.13/2],[zero1[0]+0.56,zero1[1]+0.13/2],[zero1[0]+0.56,zero1[1]-0.13/2]]
        b4=[[zero1[0]+0.765,zero1[1]-0.13/2],[zero1[0]+0.765,zero1[1]+0.13/2],[zero1[0]+0.765+0.06,zero1[1]+0.13/2],[zero1[0]+0.765+0.06,zero1[1]-0.13/2]]
        contacts.insertElement(Polygon(recsmall1),layer=self.layer)
        contacts.insertElement(Polygon(recsmall2),layer=self.layer)
        contacts.insertElement(Polygon(recsmall3),layer=self.layer)
        contacts.insertElement(Polygon(recsmall4),layer=self.layer)
        contacts.insertElement(Polygon(rectangle1),layer=self.layer)
        contacts.insertElement(Polygon(rectangle2),layer=self.layer)
        contacts.insertElement(Polygon(rectangle3),layer=self.layer)
        contacts.insertElement(Polygon(rectangle4),layer=self.layer)
        contacts.insertElement(Polygon(b1),layer=self.layerBars)
        contacts.insertElement(Polygon(b2),layer=self.layerBars)
        contacts.insertElement(Polygon(b3),layer=self.layerBars)
        contacts.insertElement(Polygon(b4),layer=self.layerBars)
        self.createText(contacts)
        self.insertElement(contacts,angle=angle,xy=center)
		
    def getDefLayers(self):
        return super(YagiUda,self).getDefLayers().union(set([self.layerBars]))
        
        
class Pt2Contacts(NanoWireTemplate):
    def __init__(self,name,descriptor=None,**kwargs):
        self.descriptor=descriptor    # ensures that the default is set, if no descriptor is given   
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "padSize":150.,
        "overlap":1.,
        "padContact":10.,
        "padSpacing":200.,
        "intLength":5.,
        "widthAtWire":2.,
        "textHeight":80.,
        })
        super(Pt2Contacts,self).__init__(name,descriptor=descriptor,**kwargs)
        
    def make(self):
        if self.end1[1]>self.end2[1]:
            top=np.array(self.end1)
            bot=np.array(self.end2)
        else:
            top=np.array(self.end2)
            bot=np.array(self.end1)
        center=(top+bot)/2.
        d=(top-bot)
        length=np.sqrt(np.dot(d,d))
        angle=np.mod((-np.arcsin(np.cross(d/length,[0.,1.]))*180./np.pi),180)
        space=self.padSpacing
        pad=self.padSize
        pc=self.padContact
        waw=self.widthAtWire
        ol=self.overlap
        iL=self.intLength
        rot=rotMatrix(angle)
        waw=np.dot(rot,np.array([waw,0]))/2.
        ol=np.dot(rot,np.array([0,ol]))
        iL=np.dot(rot,np.array([0,iL]))
        p0=np.array([[space/2.+pc,space/2.],[space/2.+pad,space/2.],
             [space/2.+pad,space/2.+pad],[space/2.,space/2.+pad],[space/2.,space/2.+pc]])
        if top[0]>=center[0]:
            a=+1
            b=-1
            ang1=0
            ang2=180
        else:
            a=-1
            b=+1
            ang1=90
            ang2=270
        points1=np.vstack((np.array(top)+ol*a+waw*b,np.array(top)+iL*b+waw*b,
                           np.dot(rotMatrix(ang1),p0.T).T,
                           np.array(top)+iL*b+waw*a+np.array([waw[1]*a,0.]),np.array(top)+ol*a+waw*a))
        points2=np.vstack((np.array(bot)+ol*b+waw*a,np.array(bot)+iL*a+waw*a,
                           np.dot(rotMatrix(ang2),p0.T).T,
                           np.array(bot)+iL*a+waw*b+np.array([waw[1]*b,0.]),np.array(bot)+ol*b+waw*b))
        self.insertElement(Polygon(points1),layer=self.layer)
        self.insertElement(Polygon(points2),layer=self.layer)
        t=self.name.split("_")[0]
        self.insertElement(Text(t,va="bottom",ha="right",height=self.textHeight),xy=np.array([space/2.+pad,space/2.+pad])*1.1,layer=self.layer,angle=180)
        return rot,p0,ang1,ang2,top,bot,a,b
        

class Pt4Contacts(Pt2Contacts):
    def __init__(self,name,descriptor=None,**kwargs):
        self.descriptor=descriptor    # ensures that the default is set, if no descriptor is given   
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "contactDist":2.,
        "overlap2":1.,
        "intarmLength":5.,
        "widthAtWire2":1.
        })
        super(Pt4Contacts,self).__init__(name,descriptor=descriptor,**kwargs)
        
    def make(self):
        rot,p0,ang1,ang2,top,bot,a,b = super(Pt4Contacts,self).make()
        
        cD=self.contactDist
        cD=np.dot(rot,np.array([0,cD]))
        waw=self.widthAtWire2
        ol=self.overlap2
        iL=self.intarmLength
        waw=np.dot(rot,np.array([waw,0]))/2.
        ol=np.dot(rot,np.array([0,ol]))
        iL=np.dot(rot,np.array([0,iL]))
        rot=rotMatrix(90)
        waw=np.dot(rot,waw)
        ol=np.dot(rot,ol)+cD
        iL=np.dot(rot,iL)-cD
        ang1+=90
        ang2+=90
        points3=np.vstack((np.array(top)+ol*a+waw*b,np.array(top)+iL*b+waw*b+np.array([0.,waw[0]*a]),
                           np.dot(rotMatrix(ang1),p0.T).T,
                           np.array(top)+iL*b+waw*a,np.array(top)+ol*a+waw*a))
        points4=np.vstack((np.array(bot)+ol*b+waw*a,np.array(bot)+iL*a+waw*a+np.array([0.,waw[0]*b]),
                           np.dot(rotMatrix(ang2),p0.T).T,
                           np.array(bot)+iL*a+waw*b,np.array(bot)+ol*b+waw*b))
        self.insertElement(Polygon(points3),layer=self.layer)
        self.insertElement(Polygon(points4),layer=self.layer)
        
        
class Pt2ContactsDots(Pt2Contacts):
    def __init__(self,name,descriptor=None,**kwargs):
        self.descriptor=descriptor    # ensures that the default is set, if no descriptor is given   
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "radius":0.5,
        "number":5,
        "distance":2.,
        "layerDots":self.descriptor.defExposureLayer+1
        })
        super(Pt2ContactsDots,self).__init__(name,descriptor=descriptor,**kwargs)
        
    def getDefLayers(self):
        return super(Pt2ContactsDots,self).getDefLayers().union(set([self.layerDots]))
        
    def make(self):
        rot,p0,ang1,ang2,top,bot,a,b = super(Pt2ContactsDots,self).make()
        center=(top+bot)/2.
        d=(top-bot)
        length=np.sqrt(np.dot(d,d))
        direction=d/length
        number=int(self.number)
        zero=center-direction*self.distance*(number-1)/2.
        for i in range(number):
            p=zero+direction*self.distance*i
            self.insertElement(Circle(self.radius/2.),xy=p,layer=self.layerDots)
        
        
class Simple2Pt(NanoWireTemplate):
    def __init__(self,name,descriptor=None,**kwargs):     
        self.descriptor=descriptor      
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "padSpacing":250.,
        "pad":200.,
        "width":1.,
        "intLength":5.,
        "widthAtPad":10.,
        "overlap":1.,
        "textSpacing":40.,
        "textHeight":40.,
        "padLayer":1,
        "jointOverlap":2.,
        })
        super(Simple2Pt,self).__init__(name,descriptor=descriptor,**kwargs)
    
    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        l=length-2.*self.overlap
        t=self.name.split("_")[0]+" L:"+"%.2f"%l
        contacts.insertElement(Text(t,va="bottom",height=self.textHeight),layer=self.padLayer,xy=[0,(self.padSpacing/2.+self.pad+self.textSpacing)])
        
        
    def make(self):
        top,bot,center,d,length,angle=self.getCoords()
        W=self.width
        D=length/2.-self.overlap
        ps=self.padSpacing
        p=self.pad
        wp=self.widthAtPad
        iL=self.intLength
        jO=self.jointOverlap
        p1a=[[wp/2.,ps/2.],[W/2.,D+iL],[-W/2.,D+iL],[-wp/2.,ps/2.],
            [-p/2.,ps/2.],[-p/2.,ps/2.+p],[p/2.,ps/2.+p],[p/2.,ps/2.]]
        p1b=[[W/2.,D+iL+jO],[W/2.,D],[-W/2.,D],[-W/2.,D+iL+jO]]
        p2a=myRotate(np.array(p1a),180)
        p2b=myRotate(np.array(p1b),180)
        contacts=Structure(self.name+"_contacts")
        contacts.insertElement(Polygon(p1a),layer=self.padLayer)
        contacts.insertElement(Polygon(p1b),layer=self.layer)
        contacts.insertElement(Polygon(p2a),layer=self.padLayer)
        contacts.insertElement(Polygon(p2b),layer=self.layer)
        self.createText(contacts)
        self.insertElement(contacts,angle=angle,xy=center)
        return W,D,p,ps,wp,length,angle,contacts
        
    def getDefLayers(self):
        return super(Simple2Pt,self).getDefLayers().union(set([self.padLayer]))
		
class pn_Junction(NanoWireTemplate):
    def __init__(self,name,descriptor=None,**kwargs):     
        self.descriptor=descriptor      
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "padSpacing":300.,
        "pad":200.,
        "width":1.,
        "intLength":5.,
        "widthAtPad":10.,
        "overlap":1.,
        "textSpacing":50.,
        "textHeight":80.,
        "layer_p":1,
        "layer_n":2,
        "jointOverlap":2.,
        "padLayer":0,
        })
        super(pn_Junction,self).__init__(name,descriptor=descriptor,**kwargs)
    
    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        l=length-2.*self.overlap
        t=self.name.split("_")[0]+" L:"+"%.2f"%l
        contacts.insertElement(Text(t,va="bottom",height=self.textHeight),layer=self.layer,xy=[0,(self.padSpacing/2.+self.pad+self.textSpacing)])
        
        
    def make(self):
        top,bot,center,d,length,angle=self.getCoords()
        W=self.width
        D=length/2.-self.overlap
        ps=self.padSpacing
        p=self.pad
        wp=self.widthAtPad
        iL=self.intLength
        jO=self.jointOverlap
        p1a=[[wp/2.,ps/2.],[W/2.,D+iL],[-W/2.,D+iL],[-wp/2.,ps/2.],
            [-p/2.,ps/2.],[-p/2.,ps/2.+p],[p/2.,ps/2.+p],[p/2.,ps/2.]]
        p1b=[[W/2.,D+iL+jO],[W/2.,D],[-W/2.,D],[-W/2.,D+iL+jO]]
        p2a=myRotate(np.array(p1a),180)
        p2b=myRotate(np.array(p1b),180)
        contacts=Structure(self.name+"_contacts")
        contacts.insertElement(Polygon(p1a),layer=self.padLayer)
        contacts.insertElement(Polygon(p1b),layer=self.layer_n)
        contacts.insertElement(Polygon(p2a),layer=self.padLayer)
        contacts.insertElement(Polygon(p2b),layer=self.layer_p)
        self.createText(contacts)
        self.insertElement(contacts,angle=angle,xy=center)
        return W,D,p,ps,wp,length,angle,contacts
        
    def getDefLayers(self):
        return super(pn_Junction,self).getDefLayers().union(set([self.layer_p,self.layer_n]))

class pn_Antenna(pn_Junction,Simple2Pt):
    def __init__(self,name,descriptor=None,**kwargs):
        self.descriptor=descriptor    # ensures that the default is set, if no descriptor is given   
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "width2":0.25,
        "intarmLength":5.,
        "gap":0.5,
        "lates":0.2,
        "number":5,
        "vertDistance":1.13,
        "antDistance":0.2,
        "layerTriangols":3
        })
        super(pn_Antenna,self).__init__(name,descriptor=descriptor,**kwargs)
        
    def make(self):
        W,D,p,ps,wp,length,angle,contacts=super(pn_Antenna,self).make()
        number=int(self.number)
      	antennaDist= -self.antDistance
        zero1=np.array([-antennaDist/2.,-self.vertDistance*(number-1)/2.])
        zero2=np.array([antennaDist/2.,-self.vertDistance*(number-1)/2.])
        for i in range(number):
            p1=zero1+np.array([0.,self.vertDistance*i])
            t1=[[p1[0],p1[1]],[p1[0]+self.lates*np.sqrt(3)/2,p1[1]-self.lates/2],[p1[0]+self.lates*np.sqrt(3)/2,p1[1]+self.lates/2],[p1[0],p1[1]]]
            tri1=myRotate(np.array(t1),180)
            contacts.insertElement(Polygon(tri1),layer=self.layerTriangols)
            p2=zero2+np.array([0.,self.vertDistance*i])
            t2=[[p2[0],p2[1]],[p2[0]-self.lates*np.sqrt(3)/2,p2[1]-self.lates/2],[p2[0]-self.lates*np.sqrt(3)/2,p2[1]+self.lates/2],[p2[0],p2[1]]]
            tri2=myRotate(np.array(t2),180)
            contacts.insertElement(Polygon(tri2),layer=self.layerTriangols)
            
    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        l=length-2.*self.gap-2.*self.overlap-self.width2
        t=self.name.split("_")[0]+"-%.3fum"%self.antDistance
        contacts.insertElement(Text(t,va="bottom",height=self.textHeight),layer=self.padLayer,xy=[0,(self.padSpacing/2.+self.pad+self.textSpacing)])
        
			
    def getDefLayers(self):
        return super(pn_Antenna,self).getDefLayers().union(set([self.layerTriangols]))
        
        
class Simple4Pt(Simple2Pt):
    def __init__(self,name,descriptor=None,**kwargs):     
        self.descriptor=descriptor        
        self.updateDefaultValue("width2",0.5)
        self.updateDefaultValue("intLength2",5.)
        self.updateDefaultValue("gap",0.5)
        self.updateDefaultValue("makeGuide",False)        
        self.updateDefaultValue("guideWidth",20.)      
        self.updateDefaultValue("guideLength",200.)   
        self.updateDefaultValue("guideDist",50.)
        super(Simple4Pt,self).__init__(name,descriptor=descriptor,**kwargs)
               
    
    def createGuide(self,contacts):
        ps=self.padSpacing
        p=self.pad
        w=self.guideWidth
        l=self.guideLength
        d=self.guideDist
        points=np.array([[w/2.,p+ps+d],[w/2.,p+ps+d+l],[-w/2.,p+ps+d+l],[-w/2.,p+ps+d]])
        contacts.insertElement(Polygon(points),layer=self.layer,xy=[0.,0.])
        contacts.insertElement(Polygon(points*np.array([1.,-1.])),layer=self.layer,xy=[0.,0.])
        
    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        l=length-2.*self.gap-2.*self.overlap-self.width2
        t=self.name.split("_")[0]+" L:"+"%.2f"%l
        contacts.insertElement(Text(t,va="bottom",height=self.textHeight),layer=self.layer,xy=[0,(self.padSpacing/2.+self.pad+self.textSpacing)])
        
    def make(self,oneSide=False):
        W,D,p,ps,wp,length,angle,contacts=super(Simple4Pt,self).make()
        ## HERE THE NEW STUFF GOES IN
        D2=length/2.-self.gap-self.overlap-self.width2/2.
        W2=self.width2
        ol=self.overlap
        iL2=self.intLength2
        jO=self.jointOverlap        
        p1a=[[wp/2+D2,ps/2.],[W2/2.+D2,iL2],[-W2/2.+D2,iL2],[-wp/2.+D2,ps/2.],
            [-p/2.,ps/2.],[-p/2.,ps/2.+p],[p/2.,ps/2.+p],[p/2.,ps/2.]]
        p1b=[[W2/2.+D2,iL2+jO],[W2/2.+D2,-ol],[-W2/2.+D2,-ol],[-W2/2.+D2,iL2+jO]]
        p1a=myRotate(np.array(p1a),90)
        p2a=myRotate(np.array(p1a),180)
        if oneSide:
            p2a[:,0]=-p2a[:,0]
        p1b=myRotate(np.array(p1b),90)
        p2b=myRotate(np.array(p1b),180)
        if oneSide:
            p2b[:,0]=-p2b[:,0]
        contacts.insertElement(Polygon(p1a),layer=self.padLayer)
        contacts.insertElement(Polygon(p2a),layer=self.padLayer)
        contacts.insertElement(Polygon(p1b),layer=self.layer)
        contacts.insertElement(Polygon(p2b),layer=self.layer)
        ## HERE THE NEW STUFF IS DONE
        if self.makeGuide:
            self.createGuide(contacts)
        return W,D,p,ps,wp,length,angle,contacts
        
class Equiv4Pt(Simple2Pt):
    def __init__(self,name,descriptor=None,**kwargs):     
        self.descriptor=descriptor        
#        try:
#            self.kwargs
#        except:
#            self.kwargs={}
#        self.kwargs.update({
#        "width2":0.5,
#        "intLength2":5.,
#        "probelength":4.,
#        "padLayer":0.,
#        })
        self.updateDefaultValue("width2",0.5)
        self.updateDefaultValue("intLength2",5.)
        self.updateDefaultValue("probelength",4.)
        self.updateDefaultValue("padLayer",0)
        super(Equiv4Pt,self).__init__(name,descriptor=descriptor,**kwargs)
    
    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        t=self.name.split("_")[0]
        contacts.insertElement(Text(t,va="bottom",height=self.textHeight),layer=self.layer,xy=[0,(self.padSpacing/2.+self.pad+self.textSpacing)])
        
    def make(self,oneSide=False):
        W,D,p,ps,wp,length,angle,contacts=super(Equiv4Pt,self).make()
        ## HERE THE NEW STUFF GOES IN
        D2=self.probelength
        W2=self.width2
        ol=self.overlap
        iL2=self.intLength2
        jO=self.jointOverlap        
        p1a=[[wp/2+D2,ps/2.],[W2/2.+D2,iL2],[-W2/2.+D2,iL2],[-wp/2.+D2,ps/2.],
            [-p/2.,ps/2.],[-p/2.,ps/2.+p],[p/2.,ps/2.+p],[p/2.,ps/2.]]
        p1b=[[W2/2.+D2,iL2+jO],[W2/2.+D2,-ol],[-W2/2.+D2,-ol],[-W2/2.+D2,iL2+jO]]
        p1a=myRotate(np.array(p1a),90)
        p2a=myRotate(np.array(p1a),180)
        if oneSide:
            p2a[:,0]=-p2a[:,0]
        p1b=myRotate(np.array(p1b),90)
        p2b=myRotate(np.array(p1b),180)
        if oneSide:
            p2b[:,0]=-p2b[:,0]
        contacts.insertElement(Polygon(p1a),layer=self.padLayer)
        contacts.insertElement(Polygon(p2a),layer=self.padLayer)
        contacts.insertElement(Polygon(p1b),layer=self.layer)
        contacts.insertElement(Polygon(p2b),layer=self.layer)
        ## HERE THE NEW STUFF IS DONE
        return W,D,p,ps,wp,length,angle,contacts

class Hall(Simple2Pt):
    def __init__(self,name,descriptor=None,**kwargs):     
        self.descriptor=descriptor        
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "width2":0.5,
        "intarmLength":5.,
        "gap":0.5
        })
        super(Hall,self).__init__(name,descriptor=descriptor,**kwargs)
    
    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        l=length-2.*self.gap-2.*self.overlap-self.width2
        t=self.name.split("_")[0]+" L:"+"%.2f"%l
        contacts.insertElement(Text(t,va="bottom",height=self.textHeight),layer=self.layer,xy=[0,(self.padSpacing/2.+self.pad+self.textSpacing)])
        
    def make(self,oneSide=False):
        W,D,p,ps,wp,length,angle,contacts=super(Hall,self).make()
        top,bot,center,d,length,angle=self.getCoords()
        ## HERE THE NEW STUFF GOES IN
        g=self.gap
        W2=self.width2
        iL2=self.intarmLength
        jO=self.jointOverlap        
        p1a=[[wp/2,ps/2.],[W2/2.,iL2],[-W2/2.,iL2],[-wp/2.,ps/2.],
            [-p/2.,ps/2.],[-p/2.,ps/2.+p],[p/2.,ps/2.+p],[p/2.,ps/2.]]
        p1b=[[W2/2.,iL2+jO],[W2/2.,g/2],[-W2/2.,g/2],[-W2/2.,iL2+jO]]
        p1a=myRotate(np.array(p1a),90)
        p2a=myRotate(np.array(p1a),180)
        if oneSide:
            p2a[:,0]=-p2a[:,0]
        p1b=myRotate(np.array(p1b),90)
        p2b=myRotate(np.array(p1b),180)
        if oneSide:
            p2b[:,0]=-p2b[:,0]
        contacts.insertElement(Polygon(p1a),layer=self.padLayer)
        contacts.insertElement(Polygon(p2a),layer=self.padLayer)
        contacts.insertElement(Polygon(p1b),layer=self.layer)
        contacts.insertElement(Polygon(p2b),layer=self.layer)
        ## HERE THE NEW STUFF IS DONE
        return W,D,p,ps,wp,length,angle,contacts

class Gate2p(Simple2Pt):
    def __init__(self,name,descriptor=None,**kwargs):     
        self.descriptor=descriptor        
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "widthGate":0.5,
        "intLengthGate":5.,
		"gateLayer":2
        })
        super(Gate2p,self).__init__(name,descriptor=descriptor,**kwargs)
    
    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        l=length-2.*self.overlap-self.widthGate
        t=self.name.split("_")[0]+" L:"+"%.2f"%l
        contacts.insertElement(Text(t,va="bottom",height=self.textHeight),layer=self.padLayer,xy=[0,(self.padSpacing/2.+self.pad+self.textSpacing)])
        
    def make(self,oneSide=False):
        W,D,p,ps,wp,length,angle,contacts=super(Gate2p,self).make()
        top,bot,center,d,length,angle=self.getCoords()
        ## HERE THE NEW STUFF GOES IN
        W2=self.widthGate
        iL2=self.intLengthGate
        jO=self.jointOverlap        
        p1a=[[wp/2,ps/2.],[W2/2.,iL2],[-W2/2.,iL2],[-wp/2.,ps/2.],
            [-p/2.,ps/2.],[-p/2.,ps/2.+p],[p/2.,ps/2.+p],[p/2.,ps/2.]]
        p1b=[[W2/2.,iL2+jO],[W2/2.,-1.],[-W2/2.,-1.],[-W2/2.,iL2+jO]]
        p1a=myRotate(np.array(p1a),90)
        p2a=myRotate(np.array(p1a),180)
        if oneSide:
            p2a[:,0]=-p2a[:,0]
        p1b=myRotate(np.array(p1b),90)
        p2b=myRotate(np.array(p1b),180)
        if oneSide:
            p2b[:,0]=-p2b[:,0]
        contacts.insertElement(Polygon(p1a),layer=self.padLayer)
        contacts.insertElement(Polygon(p1b),layer=self.gateLayer)
        ## HERE THE NEW STUFF IS DONE
        return W,D,p,ps,wp,length,angle,contacts
        
class Gate3contacts4(NanoWireTemplate):
    def __init__(self,name,descriptor=None,**kwargs):     
        self.descriptor=descriptor        
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "padSpacing":300.,
        "pad":200.,
        "width":1.,
        "intLength":5.,
        "widthAtPad":10.,
        "overlap":1.,
        "textSpacing":40.,
        "textHeight":40.,
        "padLayer":0,
        "jointOverlap":2.,
        "widthGates":0.5,
        "widthIntCont":0.5,
        "ContLayer":1,
        "spaceCont":0.5,
		"gateLayer":2
        })
        super(Gate3contacts4,self).__init__(name,descriptor=descriptor,**kwargs)
    
    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        l=length-2.*self.overlap-self.widthGates
        t=self.name.split("_")[0]+" L:"+"%.2f"%l
        contacts.insertElement(Text(t,va="bottom",height=self.textHeight),layer=self.padLayer,xy=[0,(self.padSpacing/2.+self.pad+self.textSpacing)])
        
    def make(self,oneSide=False):
        top,bot,center,d,length,angle=self.getCoords()
        W=self.width
        D=length/2.-self.overlap
        ps=self.padSpacing
        p=self.pad
        wp=self.widthAtPad
        iL=self.intLength
        jO=self.jointOverlap
        p1a=[[wp/2.,ps/2.],[W/2.,D+iL],[-W/2.,D+iL],[-wp/2.,ps/2.],
            [-p/2.,ps/2.],[-p/2.,ps/2.+p],[p/2.,ps/2.+p],[p/2.,ps/2.]]
        p2a=myRotate(np.array(p1a),180)
        contacts=Structure(self.name+"_contacts")
        contacts.insertElement(Polygon(p1a),layer=self.padLayer)
        contacts.insertElement(Polygon(p2a),layer=self.padLayer)
        self.createText(contacts)
        self.insertElement(contacts,angle=angle,xy=center)
        
        ## HERE THE NEW STUFF GOES IN
        Wg=self.widthGates
        Wc=self.widthIntCont
        jO=self.jointOverlap  
        S=self.spaceCont   
        cgc=[[0.5,-Wg/2],[0.5,Wg/2],[-5,Wg/2],[-5,-Wg/2]]
        c1s=[[-0.5,-Wg/2-S],[-0.5,-Wg/2-S-Wc],[5,-Wg/2-S-Wc],[5,-Wg/2-S]]
        c1d=[[-0.5,Wg/2+S],[-0.5,Wg/2+S+Wc],[5,Wg/2+S+Wc],[5,Wg/2+S]]    
        cgs=[[0.5,-Wg/2-2*S-Wc],[0.5,-3*Wg/2-2*S-Wc],[-5,-3*Wg/2-2*S-Wc],[-5,-Wg/2-2*S-Wc]]
        cgd=[[0.5,Wg/2+2*S+Wc],[0.5,3*Wg/2+2*S+Wc],[-5,3*Wg/2+2*S+Wc],[-5,Wg/2+2*S+Wc]]   
        c2s=[[W/2,-3*Wg/2-3*S-Wc],[W/2,-3*Wg/2-3*S-Wc-12],[-W/2,-3*Wg/2-3*S-Wc-12],[-W/2,-3*Wg/2-3*S-Wc]]    
        c2d=[[W/2,+3*Wg/2+3*S+Wc],[W/2,+3*Wg/2+3*S+Wc+12],[-W/2,+3*Wg/2+3*S+Wc+12],[-W/2,+3*Wg/2+3*S+Wc]]        
        contacts.insertElement(Polygon(cgc),layer=self.gateLayer)
        contacts.insertElement(Polygon(cgs),layer=self.gateLayer)
        contacts.insertElement(Polygon(cgd),layer=self.gateLayer)
        contacts.insertElement(Polygon(c1s),layer=self.ContLayer)
        contacts.insertElement(Polygon(c1d),layer=self.ContLayer)
        contacts.insertElement(Polygon(c2s),layer=self.ContLayer)
        contacts.insertElement(Polygon(c2d),layer=self.ContLayer)
        p1=[[-4,-Wg/2],[-4,Wg/2],[-200,5],[-200,100],[-400,100],[-400,-100],[-200,-100],[-200,-5]]
        p2=[[-4,Wg/2+2*S+Wc],[-4,3*Wg/2+2*S+Wc],[-150,160],[-150,350],[-350,350],[-350,150],[-150,150],[-5,Wg/2+2*S+Wc]]
        p3=[[-4,-Wg/2-2*S-Wc],[-4,-3*Wg/2-2*S-Wc],[-150,-160],[-150,-350],[-350,-350],[-350,-150],[-150,-150],[-5,-Wg/2-2*S-Wc]]
        p4=[[4,+Wg/2+S],[4,Wg/2+S+Wc],[150,60],[150,250],[350,250],[350,50],[150,50],[5,Wg/2+S]]
        p5=[[4,-Wg/2-S],[4,-Wg/2-S-Wc],[150,-60],[150,-250],[350,-250],[350,-50],[150,-50],[5,-Wg/2-S]]
        contacts.insertElement(Polygon(p1),layer=self.padLayer)
        contacts.insertElement(Polygon(p2),layer=self.padLayer)
        contacts.insertElement(Polygon(p3),layer=self.padLayer)
        contacts.insertElement(Polygon(p4),layer=self.padLayer)
        contacts.insertElement(Polygon(p5),layer=self.padLayer)
        return W,D,p,ps,wp,length,angle,contacts
        
    def getDefLayers(self):
        return super(Gate3contacts4,self).getDefLayers().union(set([self.padLayer,self.gateLayer,self.ContLayer]))
   
        
        
  
        
        
        
class p4_center(NanoWireTemplate):
    def __init__(self,name,descriptor=None,**kwargs):     
        self.descriptor=descriptor        
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "padSpacing":300.,
        "pad":200.,
        "width":1.,
        "intLength":5.,
        "widthAtPad":10.,
        "overlap":1.,
        "textSpacing":40.,
        "textHeight":40.,
        "padLayer":0,
        "jointOverlap":2.,
        "widthGates":0.5,
        "widthIntCont":0.5,
        "ContLayer":1,
        "spaceCont":0.5,
		"gateLayer":2
        })
        super(p4_center,self).__init__(name,descriptor=descriptor,**kwargs)
    
    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        l=length-2.*self.overlap-self.widthGates
        t=self.name.split("_")[0]+" L:"+"%.2f"%l
        contacts.insertElement(Text(t,va="bottom",height=self.textHeight),layer=self.padLayer,xy=[0,(self.padSpacing/2.+self.pad+self.textSpacing)])
        
    def make(self,oneSide=False):
        top,bot,center,d,length,angle=self.getCoords()
        W=self.width
        D=length/2.-self.overlap
        ps=self.padSpacing
        p=self.pad
        wp=self.widthAtPad
        iL=self.intLength
        jO=self.jointOverlap
        p1a=[[wp/2.,ps/2.],[W/2.,D+iL],[-W/2.,D+iL],[-wp/2.,ps/2.],
            [-p/2.,ps/2.],[-p/2.,ps/2.+p],[p/2.,ps/2.+p],[p/2.,ps/2.]]
        p2a=myRotate(np.array(p1a),180)
        contacts=Structure(self.name+"_contacts")
        contacts.insertElement(Polygon(p1a),layer=self.padLayer)
        contacts.insertElement(Polygon(p2a),layer=self.padLayer)
        self.createText(contacts)
        self.insertElement(contacts,angle=angle,xy=center)
        
        ## HERE THE NEW STUFF GOES IN
        Wg=self.widthGates
        Wc=self.widthIntCont
        jO=self.jointOverlap  
        S=self.spaceCont   
        c1s=[[-0.5,-Wg/2-S],[-0.5,-Wg/2-S-Wc],[5,-Wg/2-S-Wc],[5,-Wg/2-S]]
        c1d=[[-0.5,Wg/2+S],[-0.5,Wg/2+S+Wc],[5,Wg/2+S+Wc],[5,Wg/2+S]]    
        c2s=[[W/2,-3*Wg/2-3*S-Wc],[W/2,-3*Wg/2-3*S-Wc-12],[-W/2,-3*Wg/2-3*S-Wc-12],[-W/2,-3*Wg/2-3*S-Wc]]    
        c2d=[[W/2,+3*Wg/2+3*S+Wc],[W/2,+3*Wg/2+3*S+Wc+12],[-W/2,+3*Wg/2+3*S+Wc+12],[-W/2,+3*Wg/2+3*S+Wc]]        
        contacts.insertElement(Polygon(c1s),layer=self.ContLayer)
        contacts.insertElement(Polygon(c1d),layer=self.ContLayer)
        contacts.insertElement(Polygon(c2s),layer=self.ContLayer)
        contacts.insertElement(Polygon(c2d),layer=self.ContLayer)
        p4=[[4,+Wg/2+S],[4,Wg/2+S+Wc],[150,60],[150,250],[350,250],[350,50],[150,50],[5,Wg/2+S]]
        p5=[[4,-Wg/2-S],[4,-Wg/2-S-Wc],[150,-60],[150,-250],[350,-250],[350,-50],[150,-50],[5,-Wg/2-S]]
        contacts.insertElement(Polygon(p4),layer=self.padLayer)
        contacts.insertElement(Polygon(p5),layer=self.padLayer)
        return W,D,p,ps,wp,length,angle,contacts
        
    def getDefLayers(self):
        return super(p4_center,self).getDefLayers().union(set([self.padLayer,self.gateLayer,self.ContLayer]))
   
	
class Dots2Pt(Simple2Pt):
    def __init__(self,name,descriptor=None,**kwargs):
        self.descriptor=descriptor    # ensures that the default is set, if no descriptor is given   
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "radius":0.15,
        "number":1,
        "vertDistance":2.,
        "radDistance":0.2,
        "layerDots":self.descriptor.defExposureLayer+1
        })
        super(Dots2Pt,self).__init__(name,descriptor=descriptor,**kwargs)
        
    def make(self):
        W,D,p,ps,wp,length,angle,contacts=super(Dots2Pt,self).make()
        number=int(self.number)
        zero1=np.array([-self.radDistance/2.,-self.vertDistance*(number-1)/2.])
        zero2=np.array([self.radDistance/2.,-self.vertDistance*(number-1)/2.])
        for i in range(number):
            p1=zero1+np.array([0.,self.vertDistance*i])
            contacts.insertElement(Circle(self.radius/2.),xy=p1,layer=self.layerDots)
            p2=zero2+np.array([0.,self.vertDistance*i])
            contacts.insertElement(Circle(self.radius/2.),xy=p2,layer=self.layerDots)
        
    def getDefLayers(self):
        return super(Dots2Pt,self).getDefLayers().union(set([self.layerDots]))



class RectBowtie(Simple2Pt):
    def __init__(self,name,descriptor=None,**kwargs):
        self.descriptor=descriptor    # ensures that the default is set, if no descriptor is given   
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "lates":0.2,
        "number":5,
        "vertDistance":1.13,
        "antDistance":0.2,
        "layerTriangols":self.descriptor.defExposureLayer+1,
        "lunghezza":2.2,
        "larghezza":0.06,
        })
        super(RectBowtie,self).__init__(name,descriptor=descriptor,**kwargs)
        
    def make(self):
        W,D,p,ps,wp,length,angle,contacts=super(RectBowtie,self).make()
        number=int(self.number)
      	antennaDist= -self.antDistance
        lin1=[[-antennaDist/2+self.lates*np.sqrt(3)/2+self.lunghezza,10],[-antennaDist/2+self.lates*np.sqrt(3)/2+self.lunghezza,-10],[-antennaDist/2+self.lates*np.sqrt(3)/2+self.lunghezza+0.5,-10],[-antennaDist/2+self.lates*np.sqrt(3)/2+self.lunghezza+0.5,10]]
        contacts.insertElement(Polygon(lin1),layer=self.padLayer)
        lin2=[[antennaDist/2-self.lates*np.sqrt(3)/2-self.lunghezza,10],[antennaDist/2-self.lates*np.sqrt(3)/2-self.lunghezza,-10],[antennaDist/2-self.lates*np.sqrt(3)/2-self.lunghezza-0.5,-10],[antennaDist/2-self.lates*np.sqrt(3)/2-self.lunghezza-0.5,10]]
        contacts.insertElement(Polygon(lin2),layer=self.padLayer)
        cont1=[[-antennaDist/2+self.lates*np.sqrt(3)/2+self.lunghezza+0.5,0.25],[-antennaDist/2+self.lates*np.sqrt(3)/2+self.lunghezza+0.5+100,0.25+10],[-antennaDist/2+self.lates*np.sqrt(3)/2+self.lunghezza+0.5+100,100],[-antennaDist/2+self.lates*np.sqrt(3)/2+self.lunghezza+0.5+300,100],[-antennaDist/2+self.lates*np.sqrt(3)/2+self.lunghezza+0.5+300,-100],[-antennaDist/2+self.lates*np.sqrt(3)/2+self.lunghezza+0.5+100,-100],[-antennaDist/2+self.lates*np.sqrt(3)/2+self.lunghezza+0.5+100,-0.25-10],[-antennaDist/2+self.lates*np.sqrt(3)/2+self.lunghezza+0.5,-0.25]]
        contacts.insertElement(Polygon(cont1),layer=self.padLayer)
        cont2=[[antennaDist/2-self.lates*np.sqrt(3)/2-self.lunghezza-0.5,0.25],[antennaDist/2-self.lates*np.sqrt(3)/2-self.lunghezza-0.5-100,0.25+10],[antennaDist/2-self.lates*np.sqrt(3)/2-self.lunghezza-0.5-100,100],[antennaDist/2-self.lates*np.sqrt(3)/2-self.lunghezza-0.5-300,100],[antennaDist/2-self.lates*np.sqrt(3)/2-self.lunghezza-0.5-300,-100],[antennaDist/2-self.lates*np.sqrt(3)/2-self.lunghezza-0.5-100,-100],[antennaDist/2-self.lates*np.sqrt(3)/2-self.lunghezza-0.5-100,-0.25-10],[antennaDist/2-self.lates*np.sqrt(3)/2-self.lunghezza-0.5,-0.25]]
        contacts.insertElement(Polygon(cont2),layer=self.padLayer)
        zero1=np.array([-antennaDist/2.,-self.vertDistance*(number-1)/2.])
        zero2=np.array([antennaDist/2.,-self.vertDistance*(number-1)/2.])
        for i in range(number):
            p1=zero1+np.array([0.,self.vertDistance*i])
            t1=[[p1[0],p1[1]],[p1[0]+self.lates*np.sqrt(3)/2,p1[1]-self.lates/2],[p1[0]+self.lates*np.sqrt(3)/2,p1[1]+self.lates/2],[p1[0],p1[1]]]
            tri1=myRotate(np.array(t1),180)
            contacts.insertElement(Polygon(tri1),layer=self.layerTriangols)
            quad1=[[p1[0]+self.lates*np.sqrt(3)/2,p1[1]-self.larghezza/2],[p1[0]+self.lates*np.sqrt(3)/2,p1[1]+self.larghezza/2],[p1[0]+self.lates*np.sqrt(3)/2+self.lunghezza,p1[1]+self.larghezza/2],[p1[0]+self.lates*np.sqrt(3)/2+self.lunghezza,p1[1]-self.larghezza/2]]
            contacts.insertElement(Polygon(quad1),layer=self.layerTriangols)
            p2=zero2+np.array([0.,self.vertDistance*i])
            t2=[[p2[0],p2[1]],[p2[0]-self.lates*np.sqrt(3)/2,p2[1]-self.lates/2],[p2[0]-self.lates*np.sqrt(3)/2,p2[1]+self.lates/2],[p2[0],p2[1]]]
            tri2=myRotate(np.array(t2),180)
            contacts.insertElement(Polygon(tri2),layer=self.layerTriangols)
            quad2=[[p2[0]-self.lates*np.sqrt(3)/2,p2[1]-self.larghezza/2],[p2[0]-self.lates*np.sqrt(3)/2,p2[1]+self.larghezza/2],[p2[0]-self.lates*np.sqrt(3)/2-self.lunghezza,p2[1]+self.larghezza/2],[p2[0]-self.lates*np.sqrt(3)/2-self.lunghezza,p2[1]-self.larghezza/2]]
            contacts.insertElement(Polygon(quad2),layer=self.layerTriangols)


    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        l=length-2.*0.5-2.*self.overlap-0.5
        t=self.name.split("_")[0]+"-%.3fum"%self.antDistance
        contacts.insertElement(Text(t,va="bottom",height=self.textHeight),layer=self.padLayer,xy=[0,(self.padSpacing/2.+self.pad+self.textSpacing)])
        
    def getDefLayers(self):
        return super(RectBowtie,self).getDefLayers().union(set([self.layerTriangols]))


class Dots4Pt(Simple4Pt):
    def __init__(self,name,descriptor=None,**kwargs):
        self.descriptor=descriptor    # ensures that the default is set, if no descriptor is given   
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "radius":0.2,
        "number":5,
        "vertDistance":1.13,
        "partDistance":0.2,
        "layerDots":self.descriptor.defExposureLayer+1
        })
        super(Dots4Pt,self).__init__(name,descriptor=descriptor,**kwargs)
        
    def make(self):
        W,D,p,ps,wp,length,angle,contacts=super(Dots4Pt,self).make()
        number=int(self.number)
      	antennaDist= self.partDistance + self.radius
        zero1=np.array([-antennaDist/2.,-self.vertDistance*(number-1)/2.])
        zero2=np.array([antennaDist/2.,-self.vertDistance*(number-1)/2.])
        for i in range(number):
            p1=zero1+np.array([0.,self.vertDistance*i])
            contacts.insertElement(Circle(self.radius/2.),xy=p1,layer=self.layerDots)
            p2=zero2+np.array([0.,self.vertDistance*i])
            contacts.insertElement(Circle(self.radius/2.),xy=p2,layer=self.layerDots)
            
    def getDefLayers(self):
        return super(Dots4Pt,self).getDefLayers().union(set([self.layerDots]))
		
		
class Triangol4Pt(Simple4Pt):
    def __init__(self,name,descriptor=None,**kwargs):
        self.descriptor=descriptor    # ensures that the default is set, if no descriptor is given   
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "lates":0.2,
        "number":5,
        "vertDistance":1.13,
        "antDistance":0.2,
        "layerTriangols":self.descriptor.defExposureLayer+1
        })
        super(Triangol4Pt,self).__init__(name,descriptor=descriptor,**kwargs)
        
    def make(self):
        W,D,p,ps,wp,length,angle,contacts=super(Triangol4Pt,self).make()
        number=int(self.number)
      	antennaDist= -self.antDistance
        zero1=np.array([-antennaDist/2.,-self.vertDistance*(number-1)/2.])
        zero2=np.array([antennaDist/2.,-self.vertDistance*(number-1)/2.])
        for i in range(number):
            p1=zero1+np.array([0.,self.vertDistance*i])
            t1=[[p1[0],p1[1]],[p1[0]+self.lates*np.sqrt(3)/2,p1[1]-self.lates/2],[p1[0]+self.lates*np.sqrt(3)/2,p1[1]+self.lates/2],[p1[0],p1[1]]]
            tri1=myRotate(np.array(t1),180)
            contacts.insertElement(Polygon(tri1),layer=self.layerTriangols)
            p2=zero2+np.array([0.,self.vertDistance*i])
            t2=[[p2[0],p2[1]],[p2[0]-self.lates*np.sqrt(3)/2,p2[1]-self.lates/2],[p2[0]-self.lates*np.sqrt(3)/2,p2[1]+self.lates/2],[p2[0],p2[1]]]
            tri2=myRotate(np.array(t2),180)
            contacts.insertElement(Polygon(tri2),layer=self.layerTriangols)
            
    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        l=length-2.*self.gap-2.*self.overlap-self.width2
        t=self.name.split("_")[0]+"-%.3fum"%self.antDistance
        contacts.insertElement(Text(t,va="bottom",height=self.textHeight),layer=self.padLayer,xy=[0,(self.padSpacing/2.+self.pad+self.textSpacing)])
        
			
    def getDefLayers(self):
        return super(Triangol4Pt,self).getDefLayers().union(set([self.layerTriangols]))
     
class OneSided4Pt(NanoWireTemplate): 
    def __init__(self,name,descriptor=None,**kwargs):     
        self.descriptor=descriptor      
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "padSpacing":100.,
        "pad":150.,
        "width":1.,
        "intLength":5.,
        "widthAtPad":10.,
        "overlap":1.,
        "textSpacing":20.,
        })
        super(OneSided4Pt,self).__init__(name,descriptor=descriptor,**kwargs)
    
    def make(self):
        top,bot,center,d,length,angle=self.getCoords()
        W=self.width
        D=length/2.-self.overlap
        ps=self.padSpacing
        p=self.pad
        wp=self.widthAtPad
        iL=self.intLength
        p1=[[wp/2.,ps/2.],[W/2.,D+iL],[W/2.,D],[-W/2.,D],[-W/2.,D+iL],[-wp/2.,ps/2.],
            [-p/2.,ps/2.],[-p/2.,ps/2.+p],[p/2.,ps/2.+p],[p/2.,ps/2.]]
        p2=myRotate(np.array(p1),180)
        contacts=Structure(self.name+"_contacts")
        contacts.insertElement(Polygon(p1),layer=self.layer)
        contacts.insertElement(Polygon(p2),layer=self.layer)
        t=self.name.split("_")[0]
        contacts.insertElement(Text(t,va="bottom",height=self.textHeight),layer=self.layer,xy=[0,(ps/2.+p+self.textSpacing)])
        self.insertElement(contacts,angle=angle,xy=center)
        
        return W,D,p,ps,wp,length,angle,contacts

     
class CPW(NanoWireTemplate):
    def __init__(self,name,descriptor=None,**kwargs):
        self.descriptor=descriptor    # ensures that the default is set, if no descriptor is given   
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "stripWidth":2.,
        "gapWidth":1.092,
        "groundWidth":80.,
        "stripLength":50.,
        "contactWidth":50.,
        "contactGroundWidth":250.,
        "contactGapWidth":26.55,
        "contactLength":0.,
        "transitionLength":400.,
        "offset":0.0,
        "textHeight":50.,
        "flipped":0,
        })
        super(CPW,self).__init__(name,descriptor=descriptor,**kwargs)
    
    def createStrip(self,contacts):
        points=[
        (-self.contactWidth/2.,self.stripLength/2.+self.transitionLength+self.contactLength),
        (-self.contactWidth/2.,self.stripLength/2.+self.transitionLength),
        (-self.stripWidth/2.,self.stripLength/2.)]
        points.extend([(i[0],i[1]*(-1))for i in points[::-1]])
        points.extend([(i[0]*(-1),i[1])for i in points[::-1]])
        points=[(point[0]+self.stripWidth/2.,point[1]) for point in points]
        if self.flipped:
            a=-1.
            points=[(point[0]*(-1.),point[1]*(-1.)) for point in points]
        else:
            a=1.
        contacts.insertElement(Polygon(points),layer=self.layer,xy=[self.offset*a,0.])
        
    def createGround(self,contacts,xy=[0.,0.],mirrored=False):
        points=[
        (self.stripWidth/2.+self.gapWidth,self.stripLength/2.),
        (self.contactWidth/2.+self.contactGapWidth,self.stripLength/2.+self.transitionLength),
        (self.contactWidth/2.+self.contactGapWidth,self.stripLength/2.+self.transitionLength+self.contactLength),
        (self.contactWidth*3./2.+self.contactGapWidth,self.stripLength/2.+self.transitionLength+self.contactLength),
        (self.contactWidth*3./2.+self.contactGapWidth,self.stripLength/2.+self.transitionLength),
        (self.stripWidth/2.+self.gapWidth+self.groundWidth,self.stripLength/2.)
        ]
        points.extend([(i[0],i[1]*(-1))for i in points[::-1]])
#        points=[(point[0],point[1]) for point in points]
        if mirrored:
            points=[(point[0]*(-1.),point[1]) for point in points]
        if self.flipped:
            a=-1.
            points=[(point[0]*(-1.),point[1]*(-1.)) for point in points]
        else:
            a=1.
#        points=points+[points[0]]
        contacts.insertElement(Polygon(points),layer=self.layer,xy=[self.offset*a,0.])     
    
    def createText(self,contacts):
        t=self.name.split("_")[0]
        contacts.insertElement(Text(t,height=self.textHeight),layer=self.layer,xy=[self.contactWidth/2.+self.contactGapWidth+self.contactGroundWidth,0.],angle=90.)
        
    def make(self):
        top,bot,center,d,length,angle=self.getCoords()
        contacts=Structure(self.name+"_contacts")
        self.createStrip(contacts)
        self.createGround(contacts)
        self.createGround(contacts,mirrored=True)
        self.createText(contacts)
        self.insertElement(contacts,angle=angle,xy=center)
     
class BentCPW(NanoWireTemplate):
    def __init__(self,name,descriptor=None,**kwargs):
        self.descriptor=descriptor    # ensures that the default is set, if no descriptor is given   
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "stripWidth":2.,
        "gapWidth":1.4,
        "groundWidth":20.,
        "stripLength":300.,
        "contactWidth":160.,
        "contactLength":250.,
        "contactGapWidth":87.,
        "transitionLength":300.,
        "offset":1,
        "textHeight":20.,
        "curveRadius":50.,
        "contactDistance":300.,
        "curveInterpolation":20,
        })
        super(BentCPW,self).__init__(name,descriptor=descriptor,**kwargs)
        
    #def getVectors(self,P0,P1,P2,R):
        #"""P0=intersction point"""
        #return P0,P1,P2,o1,o2,v1,v2,dv
        
            
    def getCurvePoints(self,P0,P1,P2,R,n=20):
        t0=time.time()
        P0=np.array(P0)
        P1=np.array(P1)
        P2=np.array(P2)
        o1=(P1-P0)/np.sqrt(np.dot(P1-P0,P1-P0))
        o2=(P2-P0)/np.sqrt(np.dot(P2-P0,P2-P0))
        if np.arcsin(np.cross(o1,o2)) > 0:
            a=1.
            b=-1.
        else:
            a=-1.
            b=1.
        
        v1=R*np.dot(np.array([[0.,b],[a,0.]]),o1)
        v2=R*np.dot(np.array([[0.,a],[b,0.]]),o2)
        dv=v2-v1
        a=np.array([[o1[0],-o2[0]],[o1[1],-o2[1]]])
        b=dv
        x=np.linalg.solve(a,b)
        circleCenter= P0+x[0]*o1+v1
        angle = np.arcsin(np.cross(v2/R,v1/R))
        points=[]
        for i in range(n+1):
            x=-i*angle/n
            rot = np.array([[np.cos(x),-np.sin(x)],
                             [np.sin(x),np.cos(x)]])
            points.append(circleCenter+np.dot(rot,-v1))
        return points
    
    def createStrip(self):
        top,bot,center,d,length,angle=self.getCoords()
        theta=abs(angle/180.*np.pi-np.pi/2.)
           
        # Contacts   
        temp=[
        (self.stripWidth/2.,self.contactDistance/2.),
        (self.contactWidth/2.,self.contactDistance/2.+self.transitionLength),
        (self.contactWidth/2.,self.contactDistance/2.+self.transitionLength+self.contactLength),
        ]
        # Top Contact   
        topContact=temp+[(p[0]*(-1.),p[1]) for p in temp[::-1]]
        topContact=[(p[0]+self.stripLength/2.*np.cos(theta)-self.stripWidth/2.*np.sin(theta),p[1]) for p in topContact]
        # Bottom Contact   
        bottomContact=[(p[0]*(-1.),p[1]*(-1.)) for p in topContact]
        
        #Edges:
        s=np.sin(theta)
        c=np.cos(theta)
        t=np.tan(theta)
        par1=self.stripWidth/2.
        par2=-self.stripWidth/2.
        yU0=c*par1+t*(topContact[-1][0]+s*par1)
        yU1=c*par1+t*(bottomContact[0][0]+s*par1)
        yU2=c*par2+t*(bottomContact[-1][0]+s*par2)
        yU3=c*par2+t*(topContact[0][0]+s*par2)
        edgePoints=[(topContact[-1][0],yU0),(bottomContact[0][0],yU1),(bottomContact[-1][0],yU2),(topContact[0][0],yU3)]
        
        #Curves
        curve1=self.getCurvePoints(edgePoints[0],topContact[-1],edgePoints[1],self.curveRadius,n=self.curveInterpolation)
        curve2=self.getCurvePoints(edgePoints[1],edgePoints[0],bottomContact[0],self.curveRadius+self.stripWidth,n=self.curveInterpolation)
        curve3=self.getCurvePoints(edgePoints[2],bottomContact[-1],edgePoints[3],self.curveRadius,n=self.curveInterpolation)
        curve4=self.getCurvePoints(edgePoints[3],edgePoints[2],topContact[0],self.curveRadius+self.stripWidth,n=self.curveInterpolation)
		#MiddelTop
        middleTop=curve1+curve2
        middleBottom=curve3+curve4
                
        points=topContact+middleTop+bottomContact+middleBottom
        
        offset=(-s*(self.offset+self.stripWidth/2.),c*(self.offset+self.stripWidth/2.))
        points=[(p[0]-offset[0],p[1]-offset[1]) for p in points]
        if top[0]>=center[0]:
            pass
        else:
            points=[(p[0]*(-1.),p[1]) for p in points]
        points=[(p[0]+center[0],p[1]+center[1]) for p in points]
        self.insertElement(Polygon(points),layer=self.layer,xy=[0.,0.])
        
    def createGround(self,xy=[0.,0.],mirrored=False):            
            
        top,bot,center,d,length,angle=self.getCoords()
        theta=abs(angle/180.*np.pi-np.pi/2.)
           
        # Contacts      
        temp=[
        (self.stripWidth/2.+self.gapWidth+self.groundWidth,self.contactDistance/2.),
        (self.contactWidth*3./2.+self.contactGapWidth,self.contactDistance/2.+self.transitionLength),
        (self.contactWidth*3./2.+self.contactGapWidth,self.contactDistance/2.+self.transitionLength+self.contactLength),
        (self.contactWidth*3./2.+self.contactGapWidth,self.contactDistance/2.+self.transitionLength+self.contactLength),
        (self.contactWidth/2.+self.contactGapWidth,self.contactDistance/2.+self.transitionLength+self.contactLength),
        (self.contactWidth/2.+self.contactGapWidth,self.contactDistance/2.+self.transitionLength),
        (self.stripWidth/2.+self.gapWidth,self.contactDistance/2.),
        ]
        # Top Contact   
        topContact=[(p[0]+self.stripLength/2.*np.cos(theta)-self.stripWidth/2.*np.sin(theta),p[1]) for p in temp]
        # Bottom Contact   
        bottomContact=[(p[0]-(self.stripLength/2.*np.cos(theta)-self.stripWidth/2.*np.sin(theta)),p[1]*(-1.)) for p in temp[::-1]]
              
        #Edges:
        s=np.sin(theta)
        c=np.cos(theta)
        t=np.tan(theta)
        delta=-self.groundWidth/2.-self.gapWidth-self.stripWidth/2
        par1=self.groundWidth/2+delta
        par2=-self.groundWidth/2+delta
        yU0=c*par1+t*(topContact[-1][0]+s*par1)
        yU1=c*par1+t*(bottomContact[0][0]+s*par1)
        yU2=c*par2+t*(bottomContact[-1][0]+s*par2)
        yU3=c*par2+t*(topContact[0][0]+s*par2)
        edgePoints=[(topContact[-1][0],yU0),(bottomContact[0][0],yU1),(bottomContact[-1][0],yU2),(topContact[0][0],yU3)]
        
       
        #Curves
        curveRadius1=self.curveRadius+self.stripWidth+self.gapWidth
        curveRadius2=self.curveRadius-self.gapWidth
        curve1=self.getCurvePoints(edgePoints[0],topContact[-1],edgePoints[1],curveRadius1,n=self.curveInterpolation)
        curve2=self.getCurvePoints(edgePoints[1],edgePoints[0],bottomContact[0],curveRadius2,n=self.curveInterpolation)
        curve3=self.getCurvePoints(edgePoints[2],bottomContact[-1],edgePoints[3],curveRadius2-self.groundWidth,n=self.curveInterpolation)
        curve4=self.getCurvePoints(edgePoints[3],edgePoints[2],topContact[0],curveRadius1+self.groundWidth,n=self.curveInterpolation)
		#MiddelTop
        middleTop=curve1+curve2
        middleBottom=curve3+curve4
                
        points=topContact+middleTop+bottomContact+middleBottom
        
        if mirrored:
            s180=np.sin(np.pi)
            c180=np.cos(np.pi)
            points=[(c180*p[0]-s180*p[1],s180*p[0]+c180*p[1])for p in points]
        offset=(-s*(self.offset+self.stripWidth/2.),c*(self.offset+self.stripWidth/2.))
        points=[(p[0]-offset[0],p[1]-offset[1]) for p in points]
        
        if top[0]>=center[0]:
            pass
        else:
            points=[(p[0]*(-1.),p[1]) for p in points]
        points=[(p[0]+center[0],p[1]+center[1]) for p in points]
        
        self.insertElement(Polygon(points),layer=self.layer,xy=[0.,0.])
    
    def createText(self):
        top,bot,center,d,length,angle=self.getCoords()
        t=self.name.split("_")[0]
        self.insertElement(Text(t,height=self.textHeight),layer=self.layer,xy=[0.,self.stripLength/2.+self.transitionLength+self.contactLength*1.5],angle=90.)
        
    def make(self):
        top,bot,center,d,length,angle=self.getCoords()
        self.createStrip()
        self.createGround()
        self.createGround(mirrored=True)
        self.createText()
        
          
        
        
               
class BentCPWContact(BentCPW):
    def __init__(self,name,descriptor=None,**kwargs):
        self.descriptor=descriptor    # ensures that the default is set, if no descriptor is given   
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "padSize":150.,
        "padGap":150.,
        "padDistance":100.,
        "widthAtPad":25.,
        "widthAtInt":10.,
        "widthAtMid":15.,
        "intRadius":5.,
        "padRadius":25.,
        "midRadius":15,
        "midDistance":60.,
        "intDistance":10.,
        "width":0.5,
        "intLength":25.,
        "tipDist":0.5,
        "overlap":0.3,
        "contactDist":1.,
        })
        super(BentCPWContact,self).__init__(name,descriptor=descriptor,**kwargs)
    
    def createContact(self):
        
        top,bot,center,d,length,angle=self.getCoords()
        theta=abs(angle/180.*np.pi-np.pi/2.)
        s=np.sin(theta)
        c=np.cos(theta)
        t=np.tan(theta)
           
        # Contacts      
        contactBase=self.getCurvePoints((0.,self.padSize/2.-self.widthAtPad),(self.widthAtPad,self.padSize/2.-self.widthAtPad),(0.,self.padSize/2.-self.widthAtPad*2.),self.padRadius)+\
                    [(0.,-self.padSize/2.),(-self.padSize,-self.padSize/2.),(-self.padSize,self.padSize/2.),
                     (0.,self.padSize/2.),(self.widthAtPad,self.padSize/2.)]
        
        for i in range(4):                               
            if i in [0,1]:
                a=1.
            else:
                a=-1.
            
            if i in [0,3]:
                m=1.
            else:
                m=0.
                
            
            vec=np.array([-s,c])
            w=np.array([c*self.width/2.,s*self.width/2.])
            o=np.array([-s*self.overlap,c*self.overlap])
            edge=np.array([-(self.contactWidth*3./2.+self.contactGapWidth+self.stripLength/2.*np.cos(theta)-self.stripWidth/2.*np.sin(theta)),0.])
            
            x0=vec*(self.intLength+np.array([0.,self.intDistance])*1.5)+center
            #position /mirror pad
            points =[(p[0]+x0[0]-self.padDistance+edge[0],p[1]*a+x0[1]-self.padGap*3./2.-self.padSize*3./2.+i*(self.padSize+self.padGap)) for p in contactBase]

            if i in [0,1,2,3]:
                if i in [0,1]:
                    dist=np.array([c,s])*(i*self.contactDist+self.tipDist)
                else:
                    dist=np.array([c,s])*(length-np.mod(i+1,2)*self.contactDist-self.tipDist)
                  
                ptemp1=[
                        points[-1],
                        points[-1]+np.array([self.padDistance+m*(self.midDistance+self.widthAtPad),0.]),
                        (points[-1][0]+self.padDistance+m*(self.midDistance+self.widthAtPad),x0[1]-a*self.intDistance-a*m*(self.widthAtMid+self.midDistance)),
                        bot+vec*(self.intLength+self.intDistance*i)+dist+a*w+a*vec*self.width,
                        bot+dist+a*w-o
                        ]
                ptemp2=[
                        bot+dist-a*w-o,
                        bot+vec*(self.intLength+self.intDistance*i)+dist-a*w,
                        (points[-1][0]+self.widthAtMid+self.padDistance+m*(self.midDistance+self.widthAtPad),x0[1]-a*self.intDistance-a*self.widthAtMid-a*m*(self.widthAtMid+self.midDistance)),
                        points[0]+np.array([self.padDistance+self.widthAtMid+m*(self.midDistance+self.widthAtPad),0.]),
                        points[0],
                        ]
                        
                contWire=   self.getCurvePoints(ptemp1[1],ptemp1[0],ptemp1[2],self.padRadius)+\
                            self.getCurvePoints(ptemp1[2],ptemp1[1],ptemp1[3],self.midRadius+self.widthAtInt)+\
                            self.getCurvePoints(ptemp1[3],ptemp1[2],ptemp1[4],self.intRadius)+\
                            [ptemp1[4],ptemp2[0]]+\
                            self.getCurvePoints(ptemp2[1],ptemp2[0],ptemp2[2],self.intRadius+self.width)+\
                            self.getCurvePoints(ptemp2[2],ptemp2[1],ptemp2[3],self.midRadius)+\
                            self.getCurvePoints(ptemp2[3],ptemp2[2],ptemp2[4],self.padRadius+self.widthAtPad)
                            
            
                
                points.extend(contWire)
            
                
            if top[0]>=center[0]:
                pass
            else:
                points=[(p[0]*(-1.),p[1]) for p in points]
                points=[(p[0]+2*bot[0],p[1]) for p in points]
                
            self.insertElement(Polygon(points),layer=self.layer,xy=[0.,0.])
        
         
    def createDummyPad(self,xy=[0.,0.],mirrored=False):        
            
        top,bot,center,d,length,angle=self.getCoords()
        theta=abs(angle/180.*np.pi-np.pi/2.)
        s=np.sin(theta)
        c=np.cos(theta)
        t=np.tan(theta)
           
        # Contacts      
        temp=[
        #(self.stripWidth/2.+self.gapWidth+self.groundWidth,self.contactDistance/2.),
        (self.contactWidth*3./2.+self.contactGapWidth,self.contactDistance/2.+self.transitionLength),
        (self.contactWidth*3./2.+self.contactGapWidth,self.contactDistance/2.+self.transitionLength+self.contactLength),
        (self.contactWidth*3./2.+self.contactGapWidth,self.contactDistance/2.+self.transitionLength+self.contactLength),
        (self.contactWidth/2.+self.contactGapWidth,self.contactDistance/2.+self.transitionLength+self.contactLength),
        (self.contactWidth/2.+self.contactGapWidth,self.contactDistance/2.+self.transitionLength),
        #(self.stripWidth/2.+self.gapWidth,self.contactDistance/2.),
        ]
        # Top Contact   
        topContact=[(p[0]+self.stripLength/2.*np.cos(theta)-self.stripWidth/2.*np.sin(theta),p[1]) for p in temp]
        
        points=topContact
        if mirrored:
            s180=np.sin(np.pi)
            c180=np.cos(np.pi)
            points=[(c180*p[0]-s180*p[1],s180*p[0]+c180*p[1])for p in points]
        else:
            points=[(p[0]-(self.contactWidth*2.+self.contactGapWidth*2.),p[1])for p in points]
        offset=(-s*self.offset,c*self.offset)
        points=[(p[0]+offset[0],p[1]+offset[1]) for p in points]
        
        if top[0]>=center[0]:
            pass
        else:
            points=[(p[0]*(-1.),p[1]) for p in points]
        points=[(p[0]+center[0],p[1]+center[1]) for p in points]
        
        self.insertElement(Polygon(points),layer=self.layer,xy=[0.,0.])
    
    
    def createText(self):
        top,bot,center,d,length,angle=self.getCoords()
        l=length-3.*self.width-2.*self.tipDist-2.*self.contactDist
        t=self.name.split("_")[0]+" L:"+"%.2f"%l
        self.insertElement(Text(t,height=self.textHeight),layer=self.layer,xy=[0.,-(self.stripLength/2.+self.transitionLength+self.contactLength*1.5)])
        
    def make(self):
        top,bot,center,d,length,angle=self.getCoords()
        self.createStrip()
        self.createGround()
        self.createDummyPad(mirrored=False)
        self.createDummyPad(mirrored=True)
        self.createContact()
        self.createText()
        
               
class CPWContact(CPW):
    def __init__(self,name,descriptor=None,**kwargs):
        self.descriptor=descriptor    # ensures that the default is set, if no descriptor is given   
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "padSize":250.,
        "padGap":150.,
        "padDistance":200.,
        "width":1.,
        "intLength":5.,
        "widthAtPad":10.,
        "tipDist":0.5,
        "overlap":0.5,
        "contactDist":0.5,
        })
        super(CPWContact,self).__init__(name,descriptor=descriptor,**kwargs)
    
    def createContact(self,contacts,no=0):
        top,bot,center,d,length,angle=self.getCoords()
        
        if no in [0,3]:
            a=1.5
            b=2.
            c=1.
            d=0.
            e=0.
        elif no in [1,2]:
            a=0.5
            b=1.
            c=0.
            d=self.contactDist+self.width
            e=1.
        
        points=[
        (-self.padDistance,self.padGap*a+self.padSize*b),
        (-self.padDistance-self.padSize,self.padGap*a+self.padSize*b),
        (-self.padDistance-self.padSize,self.padGap*a+self.padSize*c),
        (-self.padDistance,self.padGap*a+self.padSize*c),
        (self.overlap-self.intLength-self.width-e*self.width,length/2.-self.tipDist-self.width-d),
        (self.overlap,length/2.-self.tipDist-self.width-d),
        (self.overlap,length/2.-self.tipDist-d),
        (self.overlap-self.intLength-e*self.width,length/2.-self.tipDist-d),
        (-self.padDistance,self.padGap*a+self.padSize*c+self.widthAtPad*b-d),
        ]
        if no in [2,3]:
            points=[(point[0],point[1]*(-1.)) for point in points]
        if self.flipped:
            points=[(point[0]*(-1.),point[1]*(-1.)) for point in points]
        contacts.insertElement(Polygon(points),layer=self.layer,xy=[0.,0.])
         
    def creatDummyPad(self,contacts,xy=[0.,0.],mirrored=False):
        points=[
        (self.contactWidth/2.+self.contactGapWidth,self.stripLength/2.+self.transitionLength),
        (self.contactWidth/2.+self.contactGapWidth,self.stripLength/2.+self.transitionLength+self.contactLength),
        (self.contactWidth*3./2.+self.contactGapWidth,self.stripLength/2.+self.transitionLength+self.contactLength),
        (self.contactWidth*3./2.+self.contactGapWidth,self.stripLength/2.+self.transitionLength),
        ]
        if mirrored:
            points=[(point[0]*(-1.),point[1]) for point in points]
        points2=[(point[0]+self.stripWidth/2.,point[1]) for point in points]
        contacts.insertElement(Polygon(points2),layer=self.layer,xy=[self.offset,0.])  
        points=[(point[0]+self.stripWidth/2.,point[1]*(-1.)) for point in points]
        if self.flipped:
            points=[(point[0]*(-1.),point[1]*(-1.)) for point in points]
        contacts.insertElement(Polygon(points),layer=self.layer,xy=[self.offset,0.])      
    
    def createContacts(self,contacts):
        for i in range(4):
            self.createContact(contacts,i)
    
    
    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        l=length-3.*self.width-2.*self.tipDist-2.*self.contactDist
        t=self.name.split("_")[0]+" L:"+"%.2f"%l
        if self.flipped:
            a=-1.
        else:
            a=1.
        contacts.insertElement(Text(t,va="bottom",height=self.textHeight),layer=self.layer,xy=[self.contactWidth/2.*a,0],angle=90.)
        
    def make(self):
        top,bot,center,d,length,angle=self.getCoords()
        contacts=Structure(self.name+"_contacts")
        self.createStrip(contacts)
        self.createGround(contacts,mirrored=False)
        self.creatDummyPad(contacts,mirrored=True)
        self.createContacts(contacts)
        self.createText(contacts)
        self.insertElement(contacts,angle=angle,xy=center)

class Bar2Pt(NanoWireTemplate):
    def __init__(self,name,descriptor=None,**kwargs):     
        self.descriptor=descriptor      
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "padSpacing":160.,
        "pad":150.,
        "widthFine":0.25,
        "widthCoarse":1.,
        "contLength":3.,
        "intLength":3.,
        "contSpacing":1.,
        "wireOverlap":1.,
        "widthAtPad":10.,
        "textSpacing":40.,
        "textHeight":40.,
        "padLayer":1,
        "contLayer":0,
        "jointOverlap":1.,
        "jointTWidth":1.5,
        "jointTThickness":1.,
        })
        super(Bar2Pt,self).__init__(name,descriptor=descriptor,**kwargs)
    
    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        l=length
        t=self.name.split("_")[0]+" L:"+"%.2f"%l
        rotatedXY = myRotate(np.array([0,(self.padSpacing/2.+self.pad+self.textSpacing)]),angle)
        contacts.insertElement(Text(t,va="bottom",height=self.textHeight),layer=self.padLayer,angle=angle,xy=rotatedXY)

    def make(self):
        top,bot,center,d,length,angle=self.getCoords()
        W=self.widthFine
        Wc=self.widthCoarse
        D=length/2.
        ps=self.padSpacing
        p=self.pad
        wp=self.widthAtPad
        cL=self.contLength
        jTw=self.jointTWidth
        jTt=self.jointTThickness
        iL=self.intLength
        jO=self.jointOverlap
        cO=self.wireOverlap
        cS=self.contSpacing
        #Making coarse contact
        p1a=[[cL-jO,cS/2.+W/2.-jTw/2.],[cL-jO,cS/2.+W/2.+jTw/2.],[cL-jO+jTt,cS/2.+W/2.+jTw/2.],[cL-jO+jTt,cS/2.+W/2.+Wc/2.],
             [cL-jO+iL,cS/2.+W/2.+Wc/2.],
             [ps/2.,cS/2.+W/2+wp/2.],[ps/2,cS/2.+W/2.+p/2.],[ps/2+p,cS/2.+p/2.],
             [ps/2+p,cS/2.+W/2.-p/2.],[ps/2,cS/2.+W/2.-p/2.],[ps/2.,cS/2.+W/2.-wp/2.],
             [cL-jO+iL,cS/2.+W/2.-Wc/2.],[cL-jO+jTt,cS/2.+W/2.-Wc/2.],[cL-jO+jTt,cS/2.+W/2.-jTw/2.]]
        p2a=myRotate(np.array(p1a),180)

        #Making the fine contacts
        p1b=[[-cO,cS/2.],[-cO,cS/2.+W],[cL,cS/2.+W],[cL,cS/2.]]      
        p2b=myRotate(np.array(p1b),180)
        contacts=Structure(self.name+"_contacts")       
        contacts.insertElement(Polygon(p1a),layer=self.padLayer,angle=angle,xy=center)
        contacts.insertElement(Polygon(p2a),layer=self.padLayer,angle=angle,xy=center)          
        contacts.insertElement(Polygon(p1b),layer=self.contLayer,angle=angle,xy=center)
        contacts.insertElement(Polygon(p2b),layer=self.contLayer,angle=angle,xy=center)     
        self.createText(contacts)
        self.insertElement(contacts,)
        return W,D,p,ps,wp,length,angle,contacts
        
    def getDefLayers(self):
        return super(Bar2Pt,self).getDefLayers().union(set([self.padLayer,self.contLayer]))

class Bar4Pt(Bar2Pt):
    def __init__(self,name,descriptor=None,**kwargs):     
        self.descriptor=descriptor        
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "width2":0.25,
        "outerContSpacing":1.
        })
        super(Bar4Pt,self).__init__(name,descriptor=descriptor,**kwargs)
    
    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        l=length
        t=self.name.split("_")[0]+" L:"+"%.2f"%l
        rotatedXY = myRotate(np.array([0,(self.padSpacing+self.pad+self.textSpacing)]),angle)
        contacts.insertElement(Text(t,va="bottom",height=self.textHeight),layer=self.padLayer,angle=angle,xy=rotatedXY)
        
    def make(self,oneSide=False):
        W,D,p,ps,wp,length,angle,contacts=super(Bar4Pt,self).make()
        top,bot,center,d,length,angle=self.getCoords()
        ## HERE THE NEW STUFF GOES IN
        W2=self.width2
        W=self.widthFine
        Wc=self.widthCoarse
        D=length/2.
        ps=self.padSpacing
        p=self.pad
        wp=self.widthAtPad
        cL=self.contLength
        jTw=self.jointTWidth
        iL=self.intLength
        jO=self.jointOverlap
        cO=self.wireOverlap
        cS=self.contSpacing
        
        #New stuff goes here
        ocS=self.outerContSpacing
        cS=cS+2.*W+2.*ocS

        p1a=[[cL-jO,cS/2.+W2/2.-jTw/2.],
            [cL-jO,cS/2.+W2/2.+iL],
            [cL-jO+Wc/2.-wp/2.,ps/2.],
            [cL-jO+Wc/2.-p/2.,ps/2.],
            [cL-jO+Wc/2.-p/2.,ps/2.+p],
            [cL-jO+Wc/2.+p/2.,ps/2.+p],
            [cL-jO+Wc/2.+p/2.,ps/2.],
            [cL-jO+Wc/2.+wp/2.,ps/2.],
            [cL-jO+Wc,cS/2.+W2/2.+iL],
            [cL-jO+Wc,cS/2.+W2/2.-jTw/2.]]
        p1a=np.array(p1a)*[-1,1]
        
        p2a=myRotate(np.array(p1a),180)          
        
        p1b=[[cO,cS/2.],[cO,cS/2.+W2],[-cL,cS/2.+W2],[-cL,cS/2.]]      
        p2b=myRotate(np.array(p1b),180)     

        contacts.insertElement(Polygon(p1a),layer=self.padLayer,angle=angle,xy=center)
        contacts.insertElement(Polygon(p2a),layer=self.padLayer,angle=angle,xy=center)
        contacts.insertElement(Polygon(p1b),layer=self.contLayer,angle=angle,xy=center)
        contacts.insertElement(Polygon(p2b),layer=self.contLayer,angle=angle,xy=center)
        ## HERE THE NEW STUFF IS DONE
        return W,D,p,ps,wp,length,angle,contacts
        
    def getDefLayers(self):
        return super(Bar4Pt,self).getDefLayers().union(set([self.padLayer,self.contLayer]))

class Bar4PtTestStruct(NanoWireTemplate):
    def __init__(self,name,descriptor=None,**kwargs):     
        self.descriptor=descriptor      
        try:
            self.kwargs
        except:
            self.kwargs={}
        self.kwargs.update({
        "padSpacing":160.,
        "pad":150.,
        "widthFine":0.5,
        "widthCoarse":1.,
        "coarseConnectionLength":3.,
        "contLength":3.,
        "fineConnectionLength":3.5,
        "intLength":3.,
        "contSpacing":3.,
        "wireOverlap":1.,
        "widthAtPad":10.,
        "textSpacing":40.,
        "textHeight":40.,
        "padLayer":1,
        "contLayer":0,
        "jointOverlap":1.,
        "jointTWidth":1.5,
        "jointTThickness":1.,
        "outerContSpacing":1.
        })
        super(Bar4PtTestStruct,self).__init__(name,descriptor=descriptor,**kwargs)
    
    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        l=length
        t=self.name.split("_")[0]+" L:"+"%.2f"%l
        rotatedXY = myRotate(np.array([0,(self.padSpacing+self.pad+self.textSpacing)]),angle)
        contacts.insertElement(Text(t,va="bottom",height=self.textHeight),layer=self.padLayer,angle=angle,xy=rotatedXY)
           
    def make(self):
        top,bot,center,d,length,angle=self.getCoords()
        W=self.widthFine
        Wc=self.widthCoarse
        D=length/2.
        ps=self.padSpacing
        p=self.pad
        wp=self.widthAtPad
        cL=self.contLength
        jTw=self.jointTWidth
        jTt=self.jointTThickness
        iL=self.intLength
        jO=self.jointOverlap
        cO=self.wireOverlap
        cS=self.contSpacing
        
        #Making coarse contact
        p1a=[[cL-jO,cS/2.+W/2.-jTw/2.],
             [cL-jO,cS/2.+W/2.+jTw/2.],
             [cL-jO+jTt,cS/2.+W/2.+jTw/2.],
             [cL-jO+jTt,cS/2.+W/2.+Wc/2.],
             [cL-jO+iL,cS/2.+W/2.+Wc/2.],
             [ps/2.,cS/2.+W/2+wp/2.],
             [ps/2,cS/2.+W/2.+p/2.],
             [ps/2+p,cS/2.+p/2.],
             [ps/2+p,cS/2.+W/2.-p/2.],
             [ps/2,cS/2.+W/2.-p/2.],
             [ps/2.,cS/2.+W/2.-wp/2.],
             [cL-jO+iL,cS/2.+W/2.-Wc/2.],
             [cL-jO+jTt,cS/2.+W/2.-Wc/2.],
             [cL-jO+jTt,cS/2.+W/2.-jTw/2.]]
        p2a=myRotate(np.array(p1a),180)

        #Making the fine contacts
        p1b=[[-cO,cS/2.],[-cO,cS/2.+W],[cL,cS/2.+W],[cL,cS/2.]]      
        p2b=myRotate(np.array(p1b),180)
        contacts=Structure(self.name+"_contacts")
        contacts.insertElement(Polygon(p1a),layer=self.padLayer,angle=angle,xy=center)
        contacts.insertElement(Polygon(p2a),layer=self.padLayer,angle=angle,xy=center)          
        contacts.insertElement(Polygon(p1b),layer=self.contLayer,angle=angle,xy=center)
        contacts.insertElement(Polygon(p2b),layer=self.contLayer,angle=angle,xy=center)     

        #Making coarse contact
        p1a=[[cL-jO,cS/2.+W/2.-jTw/2.],[cL-jO,cS/2.+W/2.+iL],[cL-jO-wp/2.,ps/2.],[cL-jO-p/2.,ps/2.],
             [cL-jO-p/2.,ps/2.+p],[cL-jO+p/2.,ps/2.+p],[cL-jO+p/2.,ps/2.],[cL-jO+wp/2.,ps/2.],
             [cL-jO+Wc,cS/2.+W/2.+iL],[cL-jO+Wc,cS/2.+W/2.-jTw/2.]]
        p1a=np.array(p1a)*[-1,1]
        p2a=myRotate(np.array(p1a),180)          
        #Making fine contact        
        p1b=[[cO,cS/2.],[cO,cS/2.+W],[-cL,cS/2.+W],[-cL,cS/2.]]      
        p2b=myRotate(np.array(p1b),180)     

        contacts.insertElement(Polygon(p1a),layer=self.padLayer,angle=angle,xy=center)
        contacts.insertElement(Polygon(p2a),layer=self.padLayer,angle=angle,xy=center)
        contacts.insertElement(Polygon(p1b),layer=self.contLayer,angle=angle,xy=center)
        contacts.insertElement(Polygon(p2b),layer=self.contLayer,angle=angle,xy=center)

        p1c=[[-W/2.,length/2.],[W/2.,length/2.],[W/2.,-length/2.],[-W/2.,-length/2.]]
        contacts.insertElement(Polygon(p1c),layer=self.contLayer,angle=angle,xy=center)        

        self.createText(contacts)
        self.insertElement(contacts)
        return W,D,p,ps,wp,length,angle,contacts

    def getDefLayers(self):
        return super(Bar4PtTestStruct,self).getDefLayers().union(set([self.padLayer,self.contLayer]))
        
class BarClose2pt(NanoWireTemplate):
    def __init__(self,name,descriptor=None,**kwargs):     
        self.descriptor=descriptor      
        try:
            self.kwargs
        except:
            self.kwargs={}
            self.kwargs.update({
            "padSpacing":160.,
            "pad":150.,
            "widthFine":0.25,
            "widthCoarse":1.,
            "contLength":2.,
            "intLength":3.,
            "contSpacing":0.2,
            "wireOverlap":1.,
            "widthAtPad":10.,
            "textSpacing":40.,
            "textHeight":40.,
            "padLayer":1,
            "contLayer":0,
            "jointOverlap":0.75,
            "jointTWidth":1.5,
            "jointTThickness":1.5,
            "coarseXOffset":1.,
            "coarseYOffset":1.,           
            "radiusFineCorners":0.1,
            "radiusCoarseCorners":0.125,
            "padYOffset":0.,
#            "rotation":0.,
            })
        super(BarClose2pt,self).__init__(name,descriptor=descriptor,**kwargs)
    
    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        l=length
        t=self.name.split("_")[0]+" L:"+"%.2fum"%l
        rotatedXY = myRotate(np.array([0,(self.padSpacing/2.+self.pad+self.textSpacing)]),angle)
        contacts.insertElement(Text(t,va="center",height=self.textHeight),layer=self.padLayer,angle=angle,xy=(rotatedXY+center))        

    def make(self):
        top,bot,center,d,length,angle=self.getCoords()
        W=self.widthFine
        Wc=self.widthCoarse
        D=length/2.
        ps=self.padSpacing
        p=self.pad
        wp=self.widthAtPad
        cL=self.contLength
        jTw=self.jointTWidth
        jTt=self.jointTThickness
        iL=self.intLength
        jO=self.jointOverlap
        cO=self.wireOverlap
        cS=self.contSpacing
        cOX=self.coarseXOffset
        cOY=self.coarseYOffset
        radiusF=self.radiusFineCorners
        radiusC=self.radiusCoarseCorners
        pYO=self.padYOffset
        
        cSft=0 #Apply shift to coarse tracks if they don't line up with the pads      
        if (cS/2.+W/2.-wp/2.) < (-p/2.+pYO):
            cSft=(-p/2.+pYO)-(cS/2.+W/2.-wp/2.)
        elif (cS/2.+W/2+wp/2.) > (p/2.+pYO):
            cSft=(p/2.+pYO)-(cS/2.+W/2.+wp/2.)        
        
        #Making coarse contact
        p1a=[[cL-jO,cS/2.+W/2.-jTw/2.],
        [cL-jO,cS/2.+W/2.+jTw/2.],
        [cL-jO+jTt,cS/2.+W/2.+jTw/2.],
        [cL-jO+jTt,cS/2.+W/2.+Wc/2.],
        [cL-jO+jTt+iL,cS/2.+W/2.+Wc/2.],
        [ps/2.,cS/2.+W/2+wp/2.+cSft],
        [ps/2.,p/2.+pYO],
        [ps/2.+p,p/2.+pYO],
        [ps/2.+p,-p/2.+pYO],
        [ps/2.,-p/2.+pYO],
        [ps/2.,cS/2.+W/2.-wp/2.+cSft],
        [cL-jO+jTt+iL,cS/2.+W/2.-Wc/2.],
        [cL-jO+jTt,cS/2.+W/2.-Wc/2.],
        [cL-jO+jTt,cS/2.+W/2.-jTw/2.]]
        p1a=np.array(p1a)+[cOX,cOY]
        p1a=self.roundCorners(p1a,radiusC,10)      
        p1a=[(pp[0],pp[1]) for pp in p1a] #Convert points to list         
        p2a=myRotate(np.array(p1a),180)

        if (cOX == 0) & (cOY == 0): 
            rotAngle = np.array([0])
        elif cOX == 0:
            if cOY<0:
                rotAngle = np.array([-np.pi/2.])
            else:
                rotAngle = np.array([np.pi/2.])
        elif cOX < 0:
            rotAngle = np.arctan([-cOY/cOX])
            rotAngle = np.pi-rotAngle
        else:
            rotAngle = np.arctan([cOY/cOX])
            

        armLength = np.sqrt(np.power(cOY,2)+np.power(cOX,2))

        #Making the fine contacts
        #Straight Section        
        pts1=[[-cO,cS/2.],  #0-BL
             [-cO,cS/2.+W], #1-TL
             [cL,cS/2.+W],  #2-TR
             [cL,cS/2.]]    #3-BR
        #Rotated Section     
        pts2=[[0,-W/2.],       #0-BL
              [0,W/2.],        #1-TL
              [armLength,W/2.],   #2-TR
              [armLength,-W/2.]]  #3-BR
              
              
        pts2 = myRotate(np.array(pts2),180./np.pi*rotAngle[0])
        pts2 = np.array(pts2)+[cL,cS/2.+W/2.] 
        pts2 = pts2.tolist()            

        if np.abs(rotAngle) == 0: #Avoid division by zero
            points = [pts1[1]]+\
                     [pts2[2]]+\
                     [pts2[3]]+\
                     [pts1[0]]            
        else:
            points = [pts1[1]]+\
                     self.intersectPoint(pts1[1],pts1[2],pts2[1],pts2[2])+\
                     [pts2[2]]+\
                     [pts2[3]]+\
                     self.intersectPoint(pts1[3],pts1[0],pts2[3],pts2[0])+\
                     [pts1[0]]
             
        #p1b=p1b+p1b_2.tolist()[:-1]+self.getCurvePoints(p1b_2.tolist()[-1],[cL+W*np.tan(rotAngle/2.)[0],cS/2.],[cL,cS/2.],radius,5)
        #p1b=p1b+p2b_2.tolist()[:-1]+self.getCurvePoints([cL+W*np.tan(rotAngle/2.)[0],cS/2.],p2b_2.tolist()[-1],[cL,cS/2.],W/2.)
        #p1b=p1b+p1b_2.tolist()+[[cL+W*np.tan(rotAngle/2.)[0],cS/2.]]+[[cL,cS/2.]]
        points=self.roundCorners(points,radiusF,10)
        
        p1b=[(pp[0],pp[1]) for pp in points] #Convert points to list        
        p2b=myRotate(np.array(p1b),180)
        
        contacts=Structure(self.name+"_contacts")       
        contacts.insertElement(Polygon(p1a),layer=self.padLayer,angle=angle,xy=center)
        contacts.insertElement(Polygon(p2a),layer=self.padLayer,angle=angle,xy=center)          
        contacts.insertElement(Polygon(p1b),layer=self.contLayer,angle=angle,xy=center)
        contacts.insertElement(Polygon(p2b),layer=self.contLayer,angle=angle,xy=center)     

        #Annotate the pads
        rotatedXY1=np.array([(ps/2.+p+self.textSpacing/4.),p/2.+self.padYOffset])
        rotatedXY2=rotatedXY1*[-1,1]
        rotatedXY1 = myRotate(rotatedXY1,angle)
        rotatedXY2 = myRotate(rotatedXY2,angle)
        contacts.insertElement(Text("In/Top",va="top",ha="left",height=p/8.),layer=self.padLayer,angle=angle,xy=rotatedXY1+center)        
        contacts.insertElement(Text("In/Bot",va="top",ha="right",height=p/8.),layer=self.padLayer,angle=angle,xy=rotatedXY2+center)
        
        self.createText(contacts)
        self.insertElement(contacts)
        return W,D,p,ps,wp,length,angle,contacts
        
    def getDefLayers(self):
        return super(BarClose2pt,self).getDefLayers().union(set([self.padLayer,self.contLayer]))       

class BarClose4pt(BarClose2pt):
    def __init__(self,name,descriptor=None,**kwargs):     
        self.descriptor=descriptor        
        try:
            self.kwargs
        except:
            self.kwargs={}
            self.kwargs.update({
            "padSpacing":160.,
            "pad":150.,
            "widthFine":0.25,
            "widthCoarse":1.,
            "contLength":2.,
            "intLength":3.,
            "contSpacing":0.2,
            "wireOverlap":1.,
            "widthAtPad":10.,
            "textSpacing":40.,
            "textHeight":40.,
            "padLayer":1,
            "contLayer":0,
            "jointOverlap":0.75,
            "jointTWidth":1.5,
            "jointTThickness":1.5,
            "coarseXOffset":1.,
            "coarseYOffset":1.,
            "radiusFineCorners":0.1,
            "radiusCoarseCorners":0.125,            
            "outerContSpacing":0.2,
            "padYOffset":0., 
            "padXOffset":0.,
#            "rotation":0.,            
            })
        super(BarClose4pt,self).__init__(name,descriptor=descriptor,**kwargs)
    
    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        l=length
        t=self.name.split("_")[0]+" L:"+"%.2fum"%l
        rotatedXY = myRotate(np.array([0,(self.padSpacing/2.+self.pad+self.textSpacing)]),angle)
        contacts.insertElement(Text(t,va="center",height=self.textHeight),layer=self.padLayer,angle=angle,xy=(rotatedXY+center))        
        
    def make(self,oneSide=False):
        W,D,p,ps,wp,length,angle,contacts=super(BarClose4pt,self).make()
        top,bot,center,d,length,angle=self.getCoords()
        ## HERE THE NEW STUFF GOES IN
        W=self.widthFine
        Wc=self.widthCoarse
        D=length/2.
        ps=self.padSpacing
        p=self.pad
        wp=self.widthAtPad
        cL=self.contLength
        jTw=self.jointTWidth
        jTt=self.jointTThickness
        iL=self.intLength
        jO=self.jointOverlap
        cO=self.wireOverlap
        cS=self.contSpacing
        cOX=self.coarseXOffset
        cOY=self.coarseYOffset
        radiusF=self.radiusFineCorners
        radiusC=self.radiusCoarseCorners
        pXO=-self.padXOffset        
        
        #New stuff goes here
        ocS=self.outerContSpacing
        cS=cS+2.*W+2.*ocS

        cSft=0 #Apply shift to coarse tracks if they don't line up with the pads      
        if (cL-jO+jTt/2.-wp/2.) < (-p/2.+pXO):
            cSft=(-p/2.+pXO)-(cL-jO+jTt/2.-wp/2.)
        elif (cL-jO+jTt/2.+wp/2.) > (p/2.+pXO):
            cSft=(p/2.+pXO)-(cL-jO+jTt/2.+wp/2.)
        
        p1a=[[cL-jO,cS/2.+W/2.-jTw/2.],
            [cL-jO,cS/2.+W/2.+jTw/2.],             
            [cL-jO+jTt/2.-Wc/2.,cS/2.+W/2.+jTw/2.],
            [cL-jO+jTt/2.-Wc/2.,cS/2.+W/2.+jTw/2.+iL],
            [cL-jO+jTt/2.-wp/2.+cSft,ps/2.],
            [-p/2.+pXO,ps/2.],
            [-p/2.+pXO,ps/2.+p],
            [p/2.+pXO,ps/2.+p],
            [p/2.+pXO,ps/2.],
            [cL-jO+jTt/2.+wp/2.+cSft,ps/2.],
            [cL-jO+jTt/2.+Wc/2.,cS/2.+W/2.+jTw/2.+iL],
            [cL-jO+jTt/2.+Wc/2.,cS/2.+W/2.+jTw/2.],
            [cL-jO+jTt,cS/2.+W/2.+jTw/2.],
            [cL-jO+jTt,cS/2.+W/2.-jTw/2.]]
        p1a=np.array(p1a)+[cOX,cOY]                
        p1a=np.array(p1a)*[-1,1]

        p1a=self.roundCorners(p1a,radiusC,10)      
        p1a=[(pp[0],pp[1]) for pp in p1a] #Convert points to list 
        p2a=myRotate(np.array(p1a),180)          

        if (cOX == 0) & (cOY == 0): 
            rotAngle = np.array([0])
        elif cOX == 0:
            if cOY<0:
                rotAngle = np.array([-np.pi/2.])
            else:
                rotAngle = np.array([np.pi/2.])
        elif cOX < 0:
            rotAngle = np.arctan([-cOY/cOX])
            rotAngle = np.pi-rotAngle
        else:
            rotAngle = np.arctan([cOY/cOX])
            

        armLength = np.sqrt(np.power(cOY,2)+np.power(cOX,2))

        #Making the fine contacts
        #Straight Section        
        pts1=[[-cO,cS/2.],  #0-BL
             [-cO,cS/2.+W], #1-TL
             [cL,cS/2.+W],  #2-TR
             [cL,cS/2.]]    #3-BR
        #Rotated Section     
        pts2=[[0,-W/2.],       #0-BL
              [0,W/2.],        #1-TL
              [armLength,W/2.],   #2-TR
              [armLength,-W/2.]]  #3-BR
              
              
        pts2 = myRotate(np.array(pts2),180./np.pi*rotAngle[0])
        pts2 = np.array(pts2)+[cL,cS/2.+W/2.] 
        pts2 = pts2.tolist()            

        if np.abs(rotAngle) == 0: #Avoid division by zero
            points = [pts1[1]]+\
                     [pts2[2]]+\
                     [pts2[3]]+\
                     [pts1[0]]            
        else:
            points = [pts1[1]]+\
                     self.intersectPoint(pts1[1],pts1[2],pts2[1],pts2[2])+\
                     [pts2[2]]+\
                     [pts2[3]]+\
                     self.intersectPoint(pts1[3],pts1[0],pts2[3],pts2[0])+\
                     [pts1[0]]
             
        #p1b=p1b+p1b_2.tolist()[:-1]+self.getCurvePoints(p1b_2.tolist()[-1],[cL+W*np.tan(rotAngle/2.)[0],cS/2.],[cL,cS/2.],radius,5)
        #p1b=p1b+p2b_2.tolist()[:-1]+self.getCurvePoints([cL+W*np.tan(rotAngle/2.)[0],cS/2.],p2b_2.tolist()[-1],[cL,cS/2.],W/2.)
        #p1b=p1b+p1b_2.tolist()+[[cL+W*np.tan(rotAngle/2.)[0],cS/2.]]+[[cL,cS/2.]]
        points=self.roundCorners(points,radiusF,10)
        
        points=np.array(points)*[-1,1]       
        p1b=[(pp[0],pp[1]) for pp in points] #Convert points to list        
        p2b=myRotate(np.array(p1b),180)

        contacts.insertElement(Polygon(p1a),layer=self.padLayer,angle=angle,xy=center)
        contacts.insertElement(Polygon(p2a),layer=self.padLayer,angle=angle,xy=center)
        contacts.insertElement(Polygon(p1b),layer=self.contLayer,angle=angle,xy=center)
        contacts.insertElement(Polygon(p2b),layer=self.contLayer,angle=angle,xy=center)

        #Annotate the pads
        rotatedXY1=np.array([p/2.+self.textSpacing/4.+self.padXOffset,(ps/2.+p)])
        rotatedXY2=np.array([-self.padXOffset,-(ps/2.+p+self.textSpacing/4.)])
        rotatedXY1 = myRotate(rotatedXY1,angle)
        rotatedXY2 = myRotate(rotatedXY2,angle)
        contacts.insertElement(Text("Out/Top",va="top",ha="left",height=p/8.),layer=self.padLayer,angle=angle,xy=rotatedXY1+center)        
        contacts.insertElement(Text("Out/Bot",va="top",ha="center",height=p/8.),layer=self.padLayer,angle=angle,xy=rotatedXY2+center)

        return W,D,p,ps,wp,length,angle,contacts  
        
    def getDefLayers(self):
        return super(BarClose4pt,self).getDefLayers().union(set([self.padLayer,self.contLayer]))               

class BarClose4pt_1Gate(BarClose4pt):
    def __init__(self,name,descriptor=None,**kwargs):     
        self.descriptor=descriptor        
        try:
            self.kwargs
        except:
            self.kwargs={}
            self.kwargs.update({
            "padSpacing":160.,
            "pad":150.,
            "widthFine":0.25,
            "widthCoarse":1.,
            "contLength":2.,
            "intLength":3.,
            "wireOverlap":1.,
            "widthAtPad":10.,
            "textSpacing":40.,
            "textHeight":40.,
            "padLayer":1,
            "contLayer":0,
            "jointOverlap":0.75,
            "jointTWidth":1.5,
            "jointTThickness":1.5,
            "coarseXOffset":1.,
            "coarseYOffset":1.,
            "radiusFineCorners":0.1,
            "radiusCoarseCorners":0.125,
            "outerContSpacing":1.250,
            "contSpacing":1.250,
            "padYOffset":0., 
            "padXOffset":80.,        
            "gateXOffset":2.,
            "gateYOffset":0.5,
            "gateWidth":0.5,
            "gateLength":3.,
            "gateLayer":2.            
            })
        super(BarClose4pt_1Gate,self).__init__(name,descriptor=descriptor,**kwargs)
    
    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        l=length
        t=self.name.split("_")[0]+" L:"+"%.2fum"%l
        rotatedXY = myRotate(np.array([0,(self.padSpacing/2.+self.pad+self.textSpacing)]),angle)
        contacts.insertElement(Text(t,va="center",height=self.textHeight),layer=self.padLayer,angle=angle,xy=(rotatedXY+center))        
        
    def make(self,oneSide=False):
        W,D,p,ps,wp,length,angle,contacts=super(BarClose4pt_1Gate,self).make()
        top,bot,center,d,length,angle=self.getCoords()
        ## HERE THE NEW STUFF GOES IN
        W=self.widthFine
        Wc=self.widthCoarse
        D=length/2.
        ps=self.padSpacing
        p=self.pad
        wp=self.widthAtPad
        jTw=self.jointTWidth
        jTt=self.jointTThickness
        iL=self.intLength
        jO=self.jointOverlap
        cO=self.wireOverlap
        cS=self.contSpacing
        radiusF=self.radiusFineCorners
        radiusC=self.radiusCoarseCorners
        pXO=self.padXOffset   
        gXO=self.gateXOffset          
        gYO=self.gateYOffset
        gW=self.gateWidth   
        gL=self.gateLength
        
        #New stuff goes here
        ocS=self.outerContSpacing
        cS=cS+2.*W+2.*ocS

        cSft=0 #Apply shift to coarse tracks if they don't line up with the pads
       
        if (gL-jO+jTt/2.-wp/2.) < (-p/2.+pXO):
            cSft=(-p/2.+pXO)-(gL-jO+jTt/2.-wp/2.)
        elif (gL-jO+jTt/2.+wp/2.) > (p/2.+pXO):
            cSft=(p/2.+pXO)-(gL-jO+jTt/2.+wp/2.)

        p1a=[[gL-jO,-jTw/2.],
            [gL-jO,jTw/2.],             
            [gL-jO+jTt/2.-Wc/2.,jTw/2.],
            [gL-jO+jTt/2.-Wc/2.,jTw/2.+iL],
            [gL-jO+jTt/2.-wp/2.+cSft,ps/2.],
            [-p/2.+pXO,ps/2.],
            [-p/2.+pXO,ps/2.+p],
            [p/2.+pXO,ps/2.+p],
            [p/2.+pXO,ps/2.],
            [gL-jO+jTt/2.+wp/2.+cSft,ps/2.],
            [gL-jO+jTt/2.+Wc/2.,jTw/2.+iL],
            [gL-jO+jTt/2.+Wc/2.,jTw/2.],
            [gL-jO+jTt,jTw/2.],
            [gL-jO+jTt,-jTw/2.]]
        p1a=np.array(p1a)+[gXO,gYO]                
        p1a=np.array(p1a)*[-1,1]

        p1a=self.roundCorners(p1a,radiusC,10)      
        p1a=[(pp[0],pp[1]) for pp in p1a] #Convert points to list 
        #p2a=myRotate(np.array(p1a),180)          

        if (gXO == 0) & (gYO == 0): 
            rotAngle = np.array([0])
        elif gXO == 0:
            if gYO<0:
                rotAngle = np.array([-np.pi/2.])
            else:
                rotAngle = np.array([np.pi/2.])
        elif gXO < 0:
            rotAngle = np.arctan([-gYO/gXO])
            rotAngle = np.pi-rotAngle
        else:
            rotAngle = np.arctan([gYO/gXO])
            

        armLength = np.sqrt(np.power(gYO,2)+np.power(gXO,2))

        #Making the fine contacts
        #Straight Section        
        pts1=[[-cO,-gW/2.],  #0-BL
             [-cO,gW/2.], #1-TL
             [gL,gW/2.],  #2-TR
             [gL,-gW/2.]]    #3-BR
        #Rotated Section     
        pts2=[[0,-gW/2.],       #0-BL
              [0,gW/2.],        #1-TL
              [armLength,gW/2.],   #2-TR
              [armLength,-gW/2.]]  #3-BR
              
              
        pts2 = myRotate(np.array(pts2),180./np.pi*rotAngle[0])
        pts2 = np.array(pts2)+[gL,0] 
        pts2 = pts2.tolist()            
        
        if np.abs(rotAngle) == 0: #Avoid division by zero
            points = [pts1[1]]+\
                     [pts2[2]]+\
                     [pts2[3]]+\
                     [pts1[0]]            
        else:
            points = [pts1[1]]+\
                     self.intersectPoint(pts1[1],pts1[2],pts2[1],pts2[2])+\
                     [pts2[2]]+\
                     [pts2[3]]+\
                     self.intersectPoint(pts1[3],pts1[0],pts2[3],pts2[0])+\
                     [pts1[0]]
             
        points=self.roundCorners(points,radiusF,10)
        
        points=np.array(points)*[-1,1]       
        p1b=[(pp[0],pp[1]) for pp in points] #Convert points to list        
        #p2b=myRotate(np.array(p1b),180)     

        contacts.insertElement(Polygon(p1a),layer=self.padLayer,angle=angle,xy=center)
        contacts.insertElement(Polygon(p1b),layer=self.gateLayer,angle=angle,xy=center)

        #Annotate the pads
        rotatedXY1=np.array([-(p/2.+self.textSpacing/4.+self.padXOffset),(ps/2.+p)])
        rotatedXY1 = myRotate(rotatedXY1,angle)
        contacts.insertElement(Text("Gate",va="top",ha="right",height=p/8.),layer=self.padLayer,angle=angle,xy=rotatedXY1+center)        

        return W,D,p,ps,wp,length,angle,contacts  

    def getDefLayers(self):
        return super(BarClose4pt_1Gate,self).getDefLayers().union(set([self.padLayer,self.contLayer,self.gateLayer]))       

class BarClose4pt_2Gate(BarClose4pt):
    def __init__(self,name,descriptor=None,**kwargs):     
        self.descriptor=descriptor        
        try:
            self.kwargs
        except:
            self.kwargs={}
            self.kwargs.update({
            "padSpacing":160.,
            "pad":150.,
            "widthFine":0.25,
            "widthCoarse":1.,
            "contLength":2.,
            "intLength":3.,
            "wireOverlap":1.,
            "widthAtPad":10.,
            "textSpacing":40.,
            "textHeight":40.,
            "padLayer":1,
            "contLayer":0,
            "jointOverlap":0.75,
            "jointTWidth":1.5,
            "jointTThickness":1.5,
            "coarseXOffset":1.,
            "coarseYOffset":1.,
            "radiusFineCorners":0.1,
            "radiusCoarseCorners":0.125,
            "outerContSpacing":1.25,
            "contSpacing":1.25,
            "padYOffset":0., 
            "padXOffset":80.,        
            "gateXOffset":4.,
            "gateYOffset":0.5,
            "gateWidth":0.15,
            "gateLength":1.,
            "gateSpacing":0.2,
            "gateLayer":2.,
            "gateTaper":0.5,
            "radiusGate":0.05,
            })
        super(BarClose4pt_2Gate,self).__init__(name,descriptor=descriptor,**kwargs)
    
    def createText(self,contacts):
        top,bot,center,d,length,angle=self.getCoords()
        l=length
        t=self.name.split("_")[0]+" L:"+"%.2fum"%l
        rotatedXY = myRotate(np.array([0,(self.padSpacing/2.+self.pad+self.textSpacing)]),angle)
        contacts.insertElement(Text(t,va="center",height=self.textHeight),layer=self.padLayer,angle=angle,xy=(rotatedXY+center))        
        
    def make(self,oneSide=False):
        W,D,p,ps,wp,length,angle,contacts=super(BarClose4pt_2Gate,self).make()
        top,bot,center,d,length,angle=self.getCoords()
        ## HERE THE NEW STUFF GOES IN
        W=self.widthFine
        Wc=self.widthCoarse
        D=length/2.
        ps=self.padSpacing
        p=self.pad
        wp=self.widthAtPad
        jTw=self.jointTWidth
        jTt=self.jointTThickness
        iL=self.intLength
        jO=self.jointOverlap
        cO=self.wireOverlap
        cS=self.contSpacing
        radiusC=self.radiusCoarseCorners
        pXO=self.padXOffset   
        gXO=self.gateXOffset          
        gYO=self.gateYOffset
        gW=self.gateWidth   
        gL=self.gateLength
        gS=self.gateSpacing
        gT=self.gateTaper
        radiusG=self.radiusGate        
        
        #New stuff goes here
        ocS=self.outerContSpacing
        cS=cS+2.*W+2.*ocS

        cSft=0 #Apply shift to coarse tracks if they don't line up with the pads
       
        if (gL-jO+jTt/2.-wp/2.) < (-p/2.+pXO):
            cSft=(-p/2.+pXO)-(gL-jO+jTt/2.-wp/2.)
        elif (gL-jO+jTt/2.+wp/2.) > (p/2.+pXO):
            cSft=(p/2.+pXO)-(gL-jO+jTt/2.+wp/2.)

        p1a=[[gL-jO,-jTw/2.],
            [gL-jO,jTw/2.],             
            [gL-jO+jTt/2.-Wc/2.,jTw/2.],
            [gL-jO+jTt/2.-Wc/2.,jTw/2.+iL],
            [gL-jO+jTt/2.-wp/2.+cSft,ps/2.],
            [-p/2.+pXO,ps/2.],
            [-p/2.+pXO,ps/2.+p],
            [p/2.+pXO,ps/2.+p],
            [p/2.+pXO,ps/2.],
            [gL-jO+jTt/2.+wp/2.+cSft,ps/2.],
            [gL-jO+jTt/2.+Wc/2.,jTw/2.+iL],
            [gL-jO+jTt/2.+Wc/2.,jTw/2.],
            [gL-jO+jTt,jTw/2.],
            [gL-jO+jTt,-jTw/2.]]
        p1a=np.array(p1a)+[gXO,gYO]                
        p1a=np.array(p1a)*[-1,1]

        p1a=self.roundCorners(p1a,radiusC,10)      
        p1a=[(pp[0],pp[1]) for pp in p1a] #Convert points to list 
        p2a=myRotate(np.array(p1a),180)          

        if (gXO == 0) & (gYO == 0): 
            rotAngle = np.array([0])
        elif gXO == 0:
            if gYO<0:
                rotAngle = np.array([-np.pi/2.])
            else:
                rotAngle = np.array([np.pi/2.])
        elif gXO < 0:
            rotAngle = np.arctan([-gYO/gXO])
            rotAngle = np.pi-rotAngle
        else:
            rotAngle = np.arctan([gYO/gXO])
            

        armLength = np.sqrt(np.power(gYO,2)+np.power(gXO,2))

        #Making the fine contacts
        #Straight Section        
        pts1=[[-cO,gS/2.],  #0-BL
             [-cO,gS/2.+gW], #1-TL
             [gL,gS/2.+gW],  #2-TR
             [gL,gS/2.]]    #3-BR
        #Rotated Section     
        pts2=[[0,-gW/2.],       #0-BL
              [0,gW/2.],        #1-TL
              [armLength,gT/2.],   #2-TR
              [armLength,-gT/2.]]  #3-BR
              
              
        pts2 = myRotate(np.array(pts2),180./np.pi*rotAngle[0])
        pts2 = np.array(pts2)+[gL,gS/2] 
        pts2 = pts2.tolist()            
        
        if np.abs(rotAngle) == 0: #Avoid division by zero
            points = [pts1[1]]+\
                     [pts2[2]]+\
                     [pts2[3]]+\
                     [pts1[0]]            
        else:
            points = [pts1[1]]+\
                     self.intersectPoint(pts1[1],pts1[2],pts2[1],pts2[2])+\
                     [pts2[2]]+\
                     [pts2[3]]+\
                     self.intersectPoint(pts1[3],pts1[0],pts2[3],pts2[0])+\
                     [pts1[0]]
             
        points=self.roundCorners(points,radiusG,10)
        
        points=np.array(points)*[-1,1]       
        p1b=[(pp[0],pp[1]) for pp in points] #Convert points to list        
        p2b=myRotate(np.array(p1b),180)     

        contacts.insertElement(Polygon(p1a),layer=self.padLayer,angle=angle,xy=center)
        contacts.insertElement(Polygon(p2a),layer=self.padLayer,angle=angle,xy=center)
        contacts.insertElement(Polygon(p1b),layer=self.gateLayer,angle=angle,xy=center)
        contacts.insertElement(Polygon(p2b),layer=self.gateLayer,angle=angle,xy=center)

        #Annotate the pads
        rotatedXY1=np.array([-(p/2.+self.textSpacing/4.+self.padXOffset),(ps/2.+p)])
        rotatedXY2=np.array([self.padXOffset,-(ps/2.+p+self.textSpacing/4.)])
        rotatedXY1 = myRotate(rotatedXY1,angle)
        rotatedXY2 = myRotate(rotatedXY2,angle)
        contacts.insertElement(Text("Gate/Top",va="top",ha="right",height=p/8.),layer=self.padLayer,angle=angle,xy=rotatedXY1+center)      
        contacts.insertElement(Text("Gate/Bot",va="top",ha="center",height=p/8.),layer=self.padLayer,angle=angle,xy=rotatedXY2+center)        
        
        return W,D,p,ps,wp,length,angle,contacts  
        
    def getDefLayers(self):
        return super(BarClose4pt_2Gate,self).getDefLayers().union(set([self.padLayer,self.contLayer,self.gateLayer]))               

class BarClose2ptAbs(NanoWireTemplate):
    def __init__(self,name,descriptor=None,**kwargs):     
        self.descriptor=descriptor      
        try:
            self.kwargs
        except:
            self.kwargs={}
            self.kwargs.update({
            "padSpacing":160.,
            "pad":150.,
            "widthFine":0.25,
            "widthCoarse":1.5,
            "contLength":2.,
            "intLength":5.,
            "contSpacing":0.2,
            "wireOverlap":1.,
            "widthAtPad":20.,
            "textSpacing":40.,
            "textHeight":40.,
            "padLayer":1,
            "contLayer":0,
            "jointOverlap":1.,
            "jointCircRadius":2.,
            "coarseXOffset":1.25,
            "coarseYOffset":1.25,           
            "radiusFineCorners":0.1,
            "radiusCoarseCorners":0.125,
            "padYOffset":0.,
#            "rotation":0.,
#            "debug":0.,               
            })
        super(BarClose2ptAbs,self).__init__(name,descriptor=descriptor,**kwargs)
    
    def createText(self,contacts,text):
        top,bot,center,d,length,angle=self.getCoords()      
        rotatedXY = myRotate(np.array([0,(self.padSpacing/2.+self.pad+self.textSpacing)]),0) #Don't rotate pads
        contacts.insertElement(Text(text,va="bottom",ha="center",height=self.textHeight),layer=self.padLayer,angle=0,xy=(rotatedXY+center))     

    def shapeUnion(self,list1,list2):
        list1=[(pp[0],pp[1]) for pp in list1] #Convert points to list 
        list2=[(pp[0],pp[1]) for pp in list2] #Convert points to list 
        firstPoly=ShapelyPolygon(list1)
        secondPoly=ShapelyPolygon(list2)
        newPolygon=firstPoly.union(secondPoly)        
        return list(newPolygon.exterior.coords)#newPolygon.exterior

    def createPads(self,contacts,padCenter,contCenter,offsetAngle=0,symm=1):
        top,bot,NWcenter,d,length,angle=self.getCoords()
#        if self.debug:        
#            angle = self.rotation #Debugging 
        if angle > 55: #Find this by trial and error, critical angle is 55 and 55-180
            angle = angle-180                   
        #Make big pad        
        pad=[[-self.pad/2.,-self.pad/2.],
             [-self.pad/2.,self.pad/2.],
             [self.pad/2.,self.pad/2.],
             [self.pad/2.,-self.pad/2.]]
        pad=np.array(pad)+padCenter
        #Make small connection pad
        contPad=Circle(self.jointCircRadius/2.,50).__toPolygon__()
        contPad=np.array(contPad)+contCenter 
        contPad = myRotate(np.array(contPad),angle)   
        #Make radius of connecting arm        
        intLenArm=[[0,self.widthCoarse/2.],
                [0,-self.widthCoarse/2.],
                [self.intLength,-self.widthCoarse/2.],
                [self.intLength,self.widthCoarse/2.]]
        intLenVect=myRotate(np.array([self.intLength,0]),angle) 
        intLenArm=myRotate(np.array(intLenArm),offsetAngle)
        intLenVect=myRotate(np.array(intLenVect),offsetAngle)               
        intLenArm=np.array(intLenArm)+contCenter                  
        intLenArm=myRotate(np.array(intLenArm),angle)
        #Make connecting arm
        contCenter = myRotate(np.array(contCenter),angle)+intLenVect 
        yVal = (padCenter[1]-contCenter[1])
        xVal = (padCenter[0]-contCenter[0])       
        if (xVal == 0) & (yVal == 0): 
            rotAngle = np.array([0])
        elif xVal == 0:
            if yVal<0:
                rotAngle = np.array([-np.pi/2.])
            else:
                rotAngle = np.array([np.pi/2.])
        elif xVal < 0:
            rotAngle = np.arctan([-yVal/xVal])
            rotAngle = np.pi-rotAngle
        else:
            rotAngle = np.arctan([yVal/xVal])            

        armLen=np.sqrt(np.power(padCenter[1]-contCenter[1],2)+np.power((padCenter[0]-contCenter[0]),2))

        connArm = [[armLen,self.widthAtPad/2.],
                    [armLen,-self.widthAtPad/2.],                        
                    [0,-self.widthCoarse/2.],
                    [0,self.widthCoarse/2.]]
                
        connArm = myRotate(np.array(connArm),180./np.pi*rotAngle[0])+contCenter

        corner1 = self.intersectPoint(connArm[0],connArm[3],intLenArm[0],intLenArm[3])
        corner2 = self.intersectPoint(connArm[1],connArm[2],intLenArm[1],intLenArm[2])      
        
        connArmVect1 = [connArm[0]]+\
                        corner1+\
                        [intLenArm[0]]

        connArmVect2 = [connArm[1]]+\
                        corner2+\
                        [intLenArm[1]]

        #Calculate which vector is the inside corner
        armLen1 = shapely.geometry.LineString(connArmVect1).length
        armLen2 = shapely.geometry.LineString(connArmVect2).length
#        radius1 = self.intLength*(2-np.sin(np.radians(2*(rotAngle))))
        ## TODO: WANT TO MAKE THIS MORE SMART
        radius1 = self.intLength 
        radius2 = radius1
        if armLen1 > armLen2: #Adjust radiuses of inner/outer corner accordingly
            radius2 = radius1-self.widthCoarse
        else:
            radius1 = radius2-self.widthCoarse

        corner1=self.getCurvePoints(connArmVect1[0],connArmVect1[1],connArmVect1[2],radius1)
        corner2=self.getCurvePoints(connArmVect2[0],connArmVect2[1],connArmVect2[2],radius2)
        
        connArmVect1=[connArmVect1[0]]+corner1+[connArmVect1[2]]   
        connArmVect2=[connArmVect2[0]]+corner2+[connArmVect2[2]]
        
        connArmVect2=connArmVect2[::-1] #Reverse list
        intLenArm = connArmVect1+connArmVect2

        connArm=[[0,self.widthCoarse/2.],
                [0,-self.widthCoarse/2.],
                [armLen,-self.widthAtPad],
                [armLen,self.widthAtPad]]
        connArm = myRotate(np.array(connArm),180./np.pi*rotAngle[0])+contCenter        

        pad = self.roundCorners(pad,self.radiusCoarseCorners*100,10)   
        pad = self.shapeUnion(pad,intLenArm)   
        pad = self.shapeUnion(self.roundCorners(pad,self.radiusCoarseCorners,10),contPad)

        contacts.insertElement(Polygon(pad),layer=self.padLayer,angle=0,xy=NWcenter) 
#        contacts.insertElement(Polygon(intLenArm),layer=self.padLayer,angle=0,xy=NWcenter) 
#        contacts.insertElement(Polygon(contPad),layer=self.padLayer,angle=0,xy=NWcenter) 

        if symm: #Create second pad at 180 degrees from first pad
            pad = myRotate(np.array(pad),180)
#            contPad = myRotate(np.array(contPad),180)
#            connArm = myRotate(np.array(intLenArm),180)
            contacts.insertElement(Polygon(pad),layer=self.padLayer,angle=0,xy=NWcenter) 
#            contacts.insertElement(Polygon(contPad),layer=self.padLayer,angle=0,xy=NWcenter) 
#            contacts.insertElement(Polygon(intLenArm),layer=self.padLayer,angle=0,xy=NWcenter) 

    def make(self):
        top,bot,center,d,length,angle=self.getCoords()
        W=self.widthFine
        Wc=self.widthCoarse
        D=length/2.
        ps=self.padSpacing
        p=self.pad
        wp=self.widthAtPad
        cL=self.contLength
        jCR=self.jointCircRadius
        iL=self.intLength
        jO=self.jointOverlap
        cO=self.wireOverlap
        cS=self.contSpacing
        cOX=self.coarseXOffset
        cOY=self.coarseYOffset
        radiusF=self.radiusFineCorners
        radiusC=self.radiusCoarseCorners
        pYO=self.padYOffset
#        if self.debug:        
#            angle = self.rotation #Debugging    

        if (cOX == 0) & (cOY == 0): 
            rotAngle = np.array([0])
        elif cOX == 0:
            if cOY<0:
                rotAngle = np.array([-np.pi/2.])
            else:
                rotAngle = np.array([np.pi/2.])
        elif cOX < 0:
            rotAngle = np.arctan([-cOY/cOX])
            rotAngle = np.pi-rotAngle
        else:
            rotAngle = np.arctan([cOY/cOX])
            
        armLength = np.sqrt(np.power(cOY,2)+np.power(cOX,2))
        #Making the fine contacts
        #Straight Section        
        pts1=[[-cO,cS/2.],  #0-BL
             [-cO,cS/2.+W], #1-TL
             [cL,cS/2.+W],  #2-TR
             [cL,cS/2.]]    #3-BR
        #Rotated Section     
        pts2=[[0,-W/2.],       #0-BL
              [0,W/2.],        #1-TL
              [armLength,W/2.],   #2-TR
              [armLength,-W/2.]]  #3-BR
              
        pts2 = myRotate(np.array(pts2),180./np.pi*rotAngle[0])
        pts2 = np.array(pts2)+[cL,cS/2.+W/2.] 
        pts2 = pts2.tolist()            

        if np.abs(rotAngle) == 0: #Avoid division by zero
            points = [pts1[1]]+[pts2[2]]+[pts2[3]]+[pts1[0]]            
        else:
            points = [pts1[1]]+self.intersectPoint(pts1[1],pts1[2],pts2[1],pts2[2])+[pts2[2]]+[pts2[3]]+self.intersectPoint(pts1[3],pts1[0],pts2[3],pts2[0])+[pts1[0]]
             
        points=self.roundCorners(points,radiusF,10)
        p1b=[(pp[0],pp[1]) for pp in points] #Convert points to list        
        p2b=myRotate(np.array(p1b),180)
        
        contacts=Structure(self.name+"_contacts")    
        self.createPads(contacts,(ps/2.+p/2.,0),(cL-jO+jCR/2.+cOX,cS/2.+W/2+cOY-jO+jCR/2.),offsetAngle=45)        
        
        contacts.insertElement(Polygon(p1b),layer=self.contLayer,angle=angle,xy=center)
        contacts.insertElement(Polygon(p2b),layer=self.contLayer,angle=angle,xy=center)     

        #Annotate the pads
        rotatedXY1=np.array([(ps/2.+p+self.textSpacing/4.),p/2.+self.padYOffset])
        rotatedXY2=rotatedXY1*[-1,1]
        rotatedXY1 = myRotate(rotatedXY1,0)
        rotatedXY2 = myRotate(rotatedXY2,0)
        contacts.insertElement(Text("In/Top",va="top",ha="left",height=p/8.),layer=self.padLayer,angle=0,xy=rotatedXY1+center) #Don't rotate pads        
        contacts.insertElement(Text("In/Bot",va="top",ha="right",height=p/8.),layer=self.padLayer,angle=0,xy=rotatedXY2+center) #Don't rotate pads

        text = self.name.split("_")[0]+" L:%.2fum"%(length)+"\n2Pt:"+"%.0fnm Spac"%(self.contSpacing*1000)
        self.createText(contacts,text)
        self.insertElement(contacts)
        return W,D,p,ps,wp,length,angle,contacts
        
    def getDefLayers(self):
        return super(BarClose2ptAbs,self).getDefLayers().union(set([self.padLayer,self.contLayer]))        

class BarClose4ptAbs(BarClose2ptAbs):
    def __init__(self,name,descriptor=None,**kwargs):     
        self.descriptor=descriptor        
        try:
            self.kwargs
        except:
            self.kwargs={}
            self.kwargs.update({
            "padSpacing":160.,
            "pad":150.,
            "widthFine":0.25,
            "widthCoarse":1.5,
            "contLength":2.,
            "intLength":5.,
            "contSpacing":0.2,
            "wireOverlap":1.,
            "widthAtPad":20.,
            "textSpacing":40.,
            "textHeight":40.,
            "padLayer":1,
            "contLayer":0,
            "jointOverlap":1.,
            "jointCircRadius":2.,
            "coarseXOffset":1.25,
            "coarseYOffset":1.25,
            "radiusFineCorners":0.1,
            "radiusCoarseCorners":0.125,            
            "outerContSpacing":0.2,
            "padYOffset":0., 
            "padXOffset":0.,
#            "rotation":0.,
#            "debug":0.,            
            })
        super(BarClose4ptAbs,self).__init__(name,descriptor=descriptor,**kwargs)
            
    def createText(self,contacts,text):
        top,bot,center,d,length,angle=self.getCoords()         
        text = self.name.split("_")[0]+" L:%.2fum"%(length)+"\n4Pt:"+"%.0fnm Spac"%(self.contSpacing*1000)
        super(BarClose4ptAbs,self).createText(contacts,text)
            
    def make(self,oneSide=False):
        W,D,p,ps,wp,length,angle,contacts=super(BarClose4ptAbs,self).make()
        top,bot,center,d,length,angle=self.getCoords()
        ## HERE THE NEW STUFF GOES IN
        W=self.widthFine
        D=length/2.
        ps=self.padSpacing
        p=self.pad
        wp=self.widthAtPad
        cL=self.contLength
        jCR=self.jointCircRadius
        jO=self.jointOverlap
        cO=self.wireOverlap
        cS=self.contSpacing
        cOX=self.coarseXOffset
        cOY=self.coarseYOffset
        radiusF=self.radiusFineCorners
        pXO=-self.padXOffset  
#        if self.debug:        
#            angle = self.rotation #Debugging
        
        #New stuff goes here
        ocS=self.outerContSpacing
        cS=cS+2.*W+2.*ocS

        if (cOX == 0) & (cOY == 0): 
            rotAngle = np.array([0])
        elif cOX == 0:
            if cOY<0:
                rotAngle = np.array([-np.pi/2.])
            else:
                rotAngle = np.array([np.pi/2.])
        elif cOX < 0:
            rotAngle = np.arctan([-cOY/cOX])
            rotAngle = np.pi-rotAngle
        else:
            rotAngle = np.arctan([cOY/cOX])
            
        armLength = np.sqrt(np.power(cOY,2)+np.power(cOX,2))

        #Making the fine contacts
        #Straight Section        
        pts1=[[-cO,cS/2.],  #0-BL
             [-cO,cS/2.+W], #1-TL
             [cL,cS/2.+W],  #2-TR
             [cL,cS/2.]]    #3-BR
        #Rotated Section     
        pts2=[[0,-W/2.],       #0-BL
              [0,W/2.],        #1-TL
              [armLength,W/2.],   #2-TR
              [armLength,-W/2.]]  #3-BR
              
              
        pts2 = myRotate(np.array(pts2),180./np.pi*rotAngle[0])
        pts2 = np.array(pts2)+[cL,cS/2.+W/2.] 
        pts2 = pts2.tolist()            

        if np.abs(rotAngle) == 0: #Avoid division by zero
            points = [pts1[1]]+[pts2[2]]+[pts2[3]]+[pts1[0]]            
        else:
            points = [pts1[1]]+self.intersectPoint(pts1[1],pts1[2],pts2[1],pts2[2])+[pts2[2]]+[pts2[3]]+self.intersectPoint(pts1[3],pts1[0],pts2[3],pts2[0])+[pts1[0]]
             
        points=self.roundCorners(points,radiusF,10)
        points=np.array(points)*[-1,1]       
        p1b=[(pp[0],pp[1]) for pp in points] #Convert points to list        
        p2b=myRotate(np.array(p1b),180)

        self.createPads(contacts,(-pXO,ps/2.+p/2.),(-cL+jO-jCR/2.-cOX,cS/2.+W/2+cOY-jO+jCR/2.),offsetAngle=90)  

        contacts.insertElement(Polygon(p1b),layer=self.contLayer,angle=angle,xy=center)
        contacts.insertElement(Polygon(p2b),layer=self.contLayer,angle=angle,xy=center)

        #Annotate the pads
        rotatedXY1=np.array([p/2.+self.textSpacing/4.+self.padXOffset,(ps/2.+p)])
        rotatedXY2=np.array([-self.padXOffset,-(ps/2.+p+self.textSpacing/4.)])
        rotatedXY1 = myRotate(rotatedXY1,0)
        rotatedXY2 = myRotate(rotatedXY2,0)
        contacts.insertElement(Text("Out/Top",va="top",ha="left",height=p/8.),layer=self.padLayer,angle=0,xy=rotatedXY1+center)        
        contacts.insertElement(Text("Out/Bot",va="top",ha="center",height=p/8.),layer=self.padLayer,angle=0,xy=rotatedXY2+center)

        return W,D,p,ps,wp,length,angle,contacts  

    def getDefLayers(self):
        return super(BarClose4ptAbs,self).getDefLayers().union(set([self.padLayer,self.contLayer]))

class BarClose4ptAbs_1Gate(BarClose4ptAbs):
    def __init__(self,name,descriptor=None,**kwargs):     
        self.descriptor=descriptor        
        try:
            self.kwargs
        except:
            self.kwargs={}
            self.kwargs.update({
            "padSpacing":160.,
            "pad":150.,
            "widthFine":0.25,
            "widthCoarse":1.5,
            "contLength":2.,
            "intLength":5.,
            "wireOverlap":1.,
            "widthAtPad":20.,
            "textSpacing":40.,
            "textHeight":40.,
            "padLayer":1,
            "contLayer":0,
            "jointOverlap":1.,
            "jointCircRadius":2.,
            "coarseXOffset":1.25,
            "coarseYOffset":1.25,
            "radiusFineCorners":0.1,
            "radiusCoarseCorners":0.125,            
            "outerContSpacing":1.,
            "contSpacing":1.25,
            "padYOffset":0., 
            "padXOffset":80.,   
            "gateXOffset":2.,
            "gateYOffset":0.5,
            "gateWidth":0.5,
            "gateLength":3.,
            "gateLayer":2,  
            "rotation":0.,
            "debug":0.,                
            })           
            
        super(BarClose4ptAbs_1Gate,self).__init__(name,descriptor=descriptor,**kwargs)
    
    def createText(self,contacts,text):
        top,bot,center,d,length,angle=self.getCoords()         
        text = self.name.split("_")[0]+" L:%.2fum"%(length)+"\n1Gate:"+"%.0fnm Width"%(self.gateWidth*1000)
        super(BarClose4ptAbs,self).createText(contacts,text)
        
    def make(self,oneSide=False):
        W,D,p,ps,wp,length,angle,contacts=super(BarClose4ptAbs_1Gate,self).make()
        top,bot,center,d,length,angle=self.getCoords()
#        if self.debug:        
#            angle = self.rotation #Debugging        
        ## HERE THE NEW STUFF GOES IN
        W=self.widthFine
        Wc=self.widthCoarse
        D=length/2.
        ps=self.padSpacing
        p=self.pad
        wp=self.widthAtPad
        jCR=self.jointCircRadius
        iL=self.intLength
        jO=self.jointOverlap
        cO=self.wireOverlap
        cS=self.contSpacing
        radiusF=self.radiusFineCorners
        radiusC=self.radiusCoarseCorners
        pXO=self.padXOffset   
        gXO=self.gateXOffset          
        gYO=self.gateYOffset
        gW=self.gateWidth   
        gL=self.gateLength
        
        #New stuff goes here
        ocS=self.outerContSpacing
        cS=cS+2.*W+2.*ocS

        if (gXO == 0) & (gYO == 0): 
            rotAngle = np.array([0])
        elif gXO == 0:
            if gYO<0:
                rotAngle = np.array([-np.pi/2.])
            else:
                rotAngle = np.array([np.pi/2.])
        elif gXO < 0:
            rotAngle = np.arctan([-gYO/gXO])
            rotAngle = np.pi-rotAngle
        else:
            rotAngle = np.arctan([gYO/gXO])
            

        armLength = np.sqrt(np.power(gYO,2)+np.power(gXO,2))

        #Making the fine contacts
        #Straight Section        
        pts1=[[-cO,-gW/2.],  #0-BL
             [-cO,gW/2.], #1-TL
             [gL,gW/2.],  #2-TR
             [gL,-gW/2.]]    #3-BR
        #Rotated Section     
        pts2=[[0,-gW/2.],       #0-BL
              [0,gW/2.],        #1-TL
              [armLength,gW/2.],   #2-TR
              [armLength,-gW/2.]]  #3-BR
              
              
        pts2 = myRotate(np.array(pts2),180./np.pi*rotAngle[0])
        pts2 = np.array(pts2)+[gL,0] 
        pts2 = pts2.tolist()            
        
        if np.abs(rotAngle) == 0: #Avoid division by zero
            points = [pts1[1]]+\
                     [pts2[2]]+\
                     [pts2[3]]+\
                     [pts1[0]]            
        else:
            points = [pts1[1]]+\
                     self.intersectPoint(pts1[1],pts1[2],pts2[1],pts2[2])+\
                     [pts2[2]]+\
                     [pts2[3]]+\
                     self.intersectPoint(pts1[3],pts1[0],pts2[3],pts2[0])+\
                     [pts1[0]]
             
        points=self.roundCorners(points,radiusF,10)
        if angle<=55: #Corresponds to critical angle in Bar2ptAbs.createPads        
            points=np.array(points)*[-1,1]  #Reflect contact to other side of NW  
        else:
            points=np.array(points)*[1,-1]  
        p1b=[(pp[0],pp[1]) for pp in points] #Convert points to list        
        #p2b=myRotate(np.array(p1b),180)     

        self.createPads(contacts,(-pXO,ps/2.+p/2.),np.mean([pts2[2],pts2[3]],0)*[-1,1],offsetAngle=135,symm=0)  
        contacts.insertElement(Polygon(p1b),layer=self.gateLayer,angle=angle,xy=center)

        #Annotate the pads
        rotatedXY1=np.array([-(p/2.+self.textSpacing/4.+self.padXOffset),(ps/2.+p)])
        rotatedXY1 = myRotate(rotatedXY1,0)
        contacts.insertElement(Text("Gate",va="top",ha="right",height=p/8.),layer=self.padLayer,angle=0,xy=rotatedXY1+center)        

        return W,D,p,ps,wp,length,angle,contacts  

    def getDefLayers(self):
        return super(BarClose4ptAbs_1Gate,self).getDefLayers().union(set([self.padLayer,self.contLayer,self.gateLayer]))

class BarClose4ptAbs_2Gate(BarClose4ptAbs):
    def __init__(self,name,descriptor=None,**kwargs):     
        self.descriptor=descriptor        
        try:
            self.kwargs
        except:
            self.kwargs={}
            self.kwargs.update({
            "padSpacing":160.,
            "pad":150.,
            "widthFine":0.25,
            "widthCoarse":1.5,
            "contLength":2.,
            "intLength":5.,
            "contSpacing":0.2,
            "wireOverlap":1.,
            "widthAtPad":20.,
            "textSpacing":40.,
            "textHeight":40.,
            "padLayer":1,
            "contLayer":0,
            "jointOverlap":1.,
            "jointCircRadius":2.,
            "coarseXOffset":1.25,
            "coarseYOffset":1.25,
            "radiusFineCorners":0.1,
            "radiusCoarseCorners":0.125,            
            "outerContSpacing":1.,
            "contSpacing":1.25,
            "padYOffset":0., 
            "padXOffset":80.,       
            "gateXOffset":4.,
            "gateYOffset":0.5,
            "gateWidth":0.15,
            "gateLength":1.,
            "gateSpacing":0.2,
            "gateLayer":2.,
            "gateTaper":0.5,
            "radiusGate":0.05,
#            "rotation":0.,
#            "debug":0.,                
            })
            
        super(BarClose4ptAbs_2Gate,self).__init__(name,descriptor=descriptor,**kwargs)
    
    def createText(self,contacts,text):
        top,bot,center,d,length,angle=self.getCoords()         
        text = self.name.split("_")[0]+" L:%.2fum"%(length)+"\n2Gate:"+"%.0fnm Spac"%(self.gateSpacing*1000)
        super(BarClose4ptAbs,self).createText(contacts,text)
        
    def make(self,oneSide=False):
        W,D,p,ps,wp,length,angle,contacts=super(BarClose4ptAbs_2Gate,self).make()          
        top,bot,center,d,length,angle=self.getCoords()
#        if self.debug:        
#            angle = self.rotation #Debugging         
        ## HERE THE NEW STUFF GOES IN
        W=self.widthFine
        Wc=self.widthCoarse
        D=length/2.
        ps=self.padSpacing
        p=self.pad
        wp=self.widthAtPad
        jCR=self.jointCircRadius
        iL=self.intLength
        jO=self.jointOverlap
        cO=self.wireOverlap
        cS=self.contSpacing
        radiusC=self.radiusCoarseCorners
        pXO=self.padXOffset   
        gXO=self.gateXOffset          
        gYO=self.gateYOffset
        gW=self.gateWidth   
        gL=self.gateLength
        gS=self.gateSpacing
        gT=self.gateTaper
        radiusG=self.radiusGate        
        
        #New stuff goes here
        ocS=self.outerContSpacing
        cS=cS+2.*W+2.*ocS

        if (gXO == 0) & (gYO == 0): 
            rotAngle = np.array([0])
        elif gXO == 0:
            if gYO<0:
                rotAngle = np.array([-np.pi/2.])
            else:
                rotAngle = np.array([np.pi/2.])
        elif gXO < 0:
            rotAngle = np.arctan([-gYO/gXO])
            rotAngle = np.pi-rotAngle
        else:
            rotAngle = np.arctan([gYO/gXO])
            

        armLength = np.sqrt(np.power(gYO,2)+np.power(gXO,2))

        #Making the fine contacts
        #Straight Section        
        pts1=[[-cO,gS/2.],  #0-BL
             [-cO,gS/2.+gW], #1-TL
             [gL,gS/2.+gW],  #2-TR
             [gL,gS/2.]]    #3-BR
        #Rotated Section     
        pts2=[[0,-gW/2.],       #0-BL
              [0,gW/2.],        #1-TL
              [armLength,gT/2.],   #2-TR
              [armLength,-gT/2.]]  #3-BR
              
              
        pts2 = myRotate(np.array(pts2),180./np.pi*rotAngle[0])
        pts2 = np.array(pts2)+[gL,gS/2] 
        pts2 = pts2.tolist()            
        
        if np.abs(rotAngle) == 0: #Avoid division by zero
            points = [pts1[1]]+\
                     [pts2[2]]+\
                     [pts2[3]]+\
                     [pts1[0]]            
        else:
            points = [pts1[1]]+\
                     self.intersectPoint(pts1[1],pts1[2],pts2[1],pts2[2])+\
                     [pts2[2]]+\
                     [pts2[3]]+\
                     self.intersectPoint(pts1[3],pts1[0],pts2[3],pts2[0])+\
                     [pts1[0]]
             
        points=self.roundCorners(points,radiusG,10)
        
        points=np.array(points)*[-1,1]       
        p1b=[(pp[0],pp[1]) for pp in points] #Convert points to list        
        p2b=myRotate(np.array(p1b),180)     

        self.createPads(contacts,(-pXO,ps/2.+p/2.),np.mean([pts2[2],pts2[3]],0)*[-1,1],offsetAngle=135,symm=1)  
        contacts.insertElement(Polygon(p1b),layer=self.gateLayer,angle=angle,xy=center)
        contacts.insertElement(Polygon(p2b),layer=self.gateLayer,angle=angle,xy=center)

        #Annotate the pads
        rotatedXY1=np.array([-(p/2.+self.textSpacing/4.+self.padXOffset),(ps/2.+p)])
        rotatedXY2=np.array([self.padXOffset,-(ps/2.+p+self.textSpacing/4.)])
        rotatedXY1 = myRotate(rotatedXY1,0)
        rotatedXY2 = myRotate(rotatedXY2,0)
        contacts.insertElement(Text("Gate/Top",va="top",ha="right",height=p/8.),layer=self.padLayer,angle=0,xy=rotatedXY1+center)      
        contacts.insertElement(Text("Gate/Bot",va="top",ha="center",height=p/8.),layer=self.padLayer,angle=0,xy=rotatedXY2+center)        
        
        return W,D,p,ps,wp,length,angle,contacts  
    def getDefLayers(self):
        return super(BarClose4ptAbs_2Gate,self).getDefLayers().union(set([self.padLayer,self.contLayer,self.gateLayer]))

allPatterns={"pn_Junction":pn_Junction,"pn_Antenna":pn_Antenna,"2PtContacts":Pt2Contacts,"Antenna":Antenna,"AntennaTriang":AntennaTriang,"4PtContacts":Pt4Contacts,"2Cont&Dots":Pt2ContactsDots,
             "Simple2Pt":Simple2Pt,"Simple4Pt":Simple4Pt,"Dots2Pt":Dots2Pt,"Dots4Pt":Dots4Pt,"Triangol4Pt":Triangol4Pt,
             "CPW":CPW,"CPW Contact":CPWContact,"Bent CPW":BentCPW,"Bent Contact CPW":BentCPWContact,
             "Hall Contact":Hall,"2p+Gate":Gate2p,"RectBowtie":RectBowtie,"DirEmis5":DirEmis5,"DirEmis4":DirEmis4,"YagiUda":YagiUda,"Mod-dop_3gates":Gate3contacts4,"p4_center":p4_center,
             "Bar2Pt":Bar2Pt,"Bar4Pt":Bar4Pt,"Bar4PtTestStruct":Bar4PtTestStruct,
             "BarClose4pt_1Gate":BarClose4pt_1Gate, "BarClose4pt_2Gate":BarClose4pt_2Gate, "BarClose2pt":BarClose2pt, "BarClose4pt":BarClose4pt,
             "BarClose2ptAbs":BarClose2ptAbs, "BarClose4ptAbs":BarClose4ptAbs, "BarClose4ptAbs_1Gate":BarClose4ptAbs_1Gate, "BarClose4ptAbs_2Gate":BarClose4ptAbs_2Gate}
defaultPattern="BarClose4ptAbs_1Gate"



#%%
#from matplotlib import *
#from matplotlib import pylab
#
#nw=CPWContact("absbca",end1=(10.,0),end2=(-10.,0))
#fig=pylab.figure()
#ax=fig.add_subplot(111)
#ax.set_xlim((-50,50))
#ax.set_ylim((-50,50))
#a=Structure("a")
#a.insertElement(nw)
#a.show(ax)
#pylab.show()
#a.save("test2.gds")
