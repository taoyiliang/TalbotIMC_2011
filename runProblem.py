'''
Using a mesh module such as mesh1d.py, which in turn makes use of modules 
gridClasses.py and mtrlClasses.py, this script generates Particles from module 
particleClasses.py and performs an IMC solve based on an input file.

Paul Talbot, 2011
'''
#import custom modules
import mesh1d as msh
import particleClasses as pc
import gridClasses as gc
import mtrlClasses as mc

#import base modules
import numpy as np
import matplotlib.pyplot as plt
import os

def getCase():
  found=False
  while not found:
    found=True
    case=raw_input('> Enter case name to run: ')
    if case[-3:]=='.in':case=case[:-3]
    if not os.path.exists(case+'.in'):
      found=False
      print 'File',case+'.in','not found in current directory.'
  return case

case=getCase()
myMesh=msh.Mesh(case)
myMesh.printAll()
numParticles=1
particles=[None]*numParticles
for p in range(numParticles):
  particles[p]=pc.Particle(myMesh)
  ptl=particles[-1]
  print ptl.ang,ptl.loc,ptl.rgn.number,ptl.cell.number
