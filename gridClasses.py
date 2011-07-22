'''
This module provides classes for use by the mesh building codes like mesh1d.  
Contains general Location class and specific Region, Boundary, and Cell classes. 
Paul Talbot, 2011
'''

class Area:
  ''' General class which provides inheritables for Region, Boundary, and Cell 
  classes.'''
  def __init__(self,mesh='dudmesh',parent='dudparent',data=[10,100,'dudmater']):
    self.mesh=mesh
    self.parent=parent #the area that this one belongs to
    try:self.number=len(self.parent.subAreas)
    except AttributeError: self.number=len(self.parent.rgns)
    self.subAreas=[] #areas that are subsets of this one
    self.subAreaType=None #to be overwritten by inheritors
    self.width=float(data[0]) #width of area
    self.nSubAreas=int(data[1]) #number of subareas
    if self.nSubAreas!=0:
      self.subAreaWidth=self.width/self.nSubAreas #width of subareas
    else:self.subAreaWidth=None #for smallest-level (cells)
    self.matName=data[2] #material name
    self.mtrl=None #to be overwritten by actual material
    self.locLBound=0 #left boundary location

    # run initialization functions
    self.indSetup()
    self.setMaterial()

    # fill subAreas with subAreaType objects
    if self.subAreas>0:
      for i in range(self.nSubAreas):
        self.subAreas.append(self.subAreaType(self.mesh,self,\
            [self.subAreaWidth,0,self.matName]))
        #TODO: For multiple layers of regions, find a way to 
        #      pass the number of subcells to divide into;
        #      currently defaults to 0 (regions->cells).


  def indSetup(self):
    pass #to be overwritten by individual classes

  def addSubRegion(self,data):
    self.subAreas.append(self.subAreaType(self.mesh,self,data))

  def setMaterial(self):
    if self.mesh=='dudmesh':return #used for debugging
    for mat in self.mesh.mtrls:
      if mat.name==self.matName:
        self.mtrl=mat
        break
    if self.mtrl==None and self.mtrl!='Boundary':
      print 'ERROR: Region material listed as',self.matName,\
          'but not found on material list!  Valid materials include: ',\
          [m.name for m in self.mesh.mtrls],'\n\nEarly termination.\n'
      import sys
      sys.exit()

  def printAll(self,outFile):
    outFile.writelines('Area Type:'+str(self)+'\n'+\
        '  Area Number: '+str(self.number)+'\n'+\
        '  Material: '+self.mtrl.name+'\n'+\
        '  Sub-Area Type: '+str(self.subAreaType)+'\n'+\
        '  Number of Sub-Areas: '+str(self.nSubAreas)+'\n\n')
        
  def findBounds(self):
    if self.parent.subAreas[0]==self:
      self.locLBound=0
    else:


class Region(Area):
  '''The largest subset of mesh, bounded by material properties'''
  def indSetup(self):
    #identify sub area type
    self.subAreaType=Cell
    self.parent.subAreas=self.mesh.rgns



class Cell(Area):
  '''The smallest subset of mesh, individual spatial discretization'''
  def indSetup(self):
    self.subAreaType=None



class Boundary(Area):
  '''Boundary area, just outside of mesh'''
  def __init__(self,mesh,data):
    self.mesh=mesh #mesh which boundary effects
    self.side=data[0] #side of mesh boundary is on
    self.bdyType=data[1] #type of boundary
    self.setTypeData(data[2:]) #set remainder of data by type

  def setTypeData(self,data):
    if self.bdyType=='marshak':
      self.bdyTmp=data[0]
    elif self.bdyType=='vacuum':
      pass #no additional information needed
    elif self.bdyType=='reflect':
      self.reflAmt=data[0]

  def doBoundary(self):
    if self.bdyType=='marshak':
      pass
    elif self.bdyType=='vacuum':
      pass
    elif self.bdyType=='reflect':
      pass
    #TODO Write each one so that it does the appropriate action

  def printAll(self,outFile):
    outFile.writelines('Boundary Side: '+self.side+'\n'+\
        '  Boundary Type: '+self.bdyType+'\n\n')

