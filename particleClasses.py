'''
Defines Monte Carlo particles for use in solving the IMC equations.

Currently only supports 1D.

Paul Talbot, 2011
'''

import random as rd
#rd.seed(11235812213455) #optional, used for getting repeatable results
import numpy as np

class Particle:
  def __init__(self,mesh):
    self.mesh=mesh
    self.freq=0 #frequency \nu
    self.ang=[0,0] #solid angle trajectory; 1D only uses [0]
    self.loc=[0,0,0] #location in 3d space; 1D only uses [0]
    self.wt=1 #particle weight
    self.rgn=None #replace with region instance that particle is in
    self.cell=None #replace will cell instance that particle is in
    self.hist=[] #stores Events in order of occurance

    self.selAngle()
    self.selLocation()

  def selAngle(self):
    rand=rd.random()*2.0-1.0
    self.ang[0]=rand

  def selLocation(self):
    rand=rd.random()*self.mesh.width
    self.loc[0]=rand #leftover distance to travel
    #find region that particle lands in
    for rgn in self.mesh.rgns:
      if rand-rgn.width>0.0: rand-=rgn.width #passes region
      else: #lands here
        self.rgn=rgn
        break
    if self.rgn==None:
      print 'Failed to find region for particle!  Exiting...'
      import sys
      sys.exit()
    #find cell within region that particle lands in
    for cell in self.rgn.subAreas:
      if rand-cell.width>0.0: rand-=cell.width #passes region
      else: #lands here
        self.cell=cell
        break
    if self.cell==None:
      print 'Failed to find cell for particle!  Exiting...'
      import sys
      sys.exit()

  def selEvent(self):
    pass
    #sample distance would travel
    #check distance to boundary
    #if distance closer than boundary, sample interaction
    #else move to cell wall, go again

  def printHistory(self):
    print 'History for Particle:'
    print 'Freq , [Angle] ,[Location] , Interaction'
    for h in self.hist:
      print h.freq,h.ang,h.loc,h.eventType


class Event:
  def __init__(self,particle):
    self.particle=particle
    self.number=len(self.particle.hist)
    
    #take snapshot of particle data
    self.freq=self.particle.freq
    self.ang=self.particle.ang[:]
    self.loc=self.particle.loc[:]

    self.eventType='' #stores the event that occurred
    
