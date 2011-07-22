'''
This module is used for generation of a 1-dimensional mesh on which radiative 
heat transfer calculations can be performed using the IMC equations as 
derived by Fleck and Cummings in 1971.

Paul Talbot, 2011
'''
import gridClasses as gc #contains region, boundary, cell classes
import mtrlClasses as mc #contains material, group classes

class Mesh:
  '''
  An object that holds all of the information about the problem, including: 
  - Region classes, areas with the similar material properties; 
  - Boundary classes, that provide the boundary conditions of the problem; 
  - Material classes, which store material-specific properties
  Functions: #TODO
  '''
  def __init__(self,case):
    self.case=case #run name
    self.width=0 #total width of mesh
    self.mtrls=[] #list of material instances on mesh
    self.rgns=[] #list of region instances on mesh
    self.bounds=[] #list of boundary conditions for mesh

    self.readInput()
    self.findWidth()

  def addRegion(self):
    '''
    Handles adding region instances to the mesh.
    Accepts: None
    Returns: None
    Creates: Region instance
    '''
    pass

  def addMaterial(self):
    '''
    Handles adding a material instance to the mesh.
    Accepts: None
    Returns: None
    Creates: Materian instance
    '''
    pass

  def readInput(self):
    '''
    Reads input file for given case <case>.in and creates associated 
    regions and materials, including cells and material group data.
    Accepts: None
    Returns: None
    Creates: None
    '''
    inFile=file(self.case+'.in')
    #flags for particular entry types
    stGroups=0 #group settings
    stMaterials=0 #materials entries
    stRegions=0 #regions entries
    stBoundary=0 #boundary conditions
    stInitial=0 #initial conditions
    for line in inFile:
      if line[0]=='#' or line=='\n':continue
      #set flags when keyword found
      elif 'Groups:' in line:
        stGroups=True
        stMaterials=stRegions=stBoundary=stInitial=False
        continue
      elif 'Materials:' in line:
        stMaterials=True
        stGroups=stRegions=stBoundary=stInitial=False
        continue
      elif 'Regions:' in line:
        stRegions=True
        stGroups=stMaterials=stBoundary=stInitial=False
        continue
      elif 'Boundary:' in line:
        stBoundary=True
        stGroups=stMaterials=stRegions=stInitial=False
        continue
      elif 'Initial Conditions:' in line:
        stInitial=True
        stGroups=stMaterials=stRegions=stBoundary=False
        continue
      #otherwise, add data to mesh
      elif stGroups:
        groupBounds=line.split()
        for i in range(len(groupBounds)): #format correctly
          groupBounds[i]=float(groupBounds[i])
      elif stMaterials:
        self.mtrls.append(mc.Material(self,line.split(',')))
      elif stRegions:
        self.rgns.append(gc.Region(self,self,data=line.split()))
      elif stBoundary:
        self.bounds.append(gc.Boundary(self,data=line.split()))
      elif stInitial:
        self.applyInitialCond(line.split()) #TODO

  def applyInitialCond(self,data):
    pass

  def printAll(self):
    outFile=file(self.case+'.dat','w')
    outFile.writelines('===========\nMesh Status\n===========\n'+\
        'Width: '+str(self.width)+'\n'+\
        'Number of Regions: '+str(len(self.rgns))+'\n'+\
        'Number of Materials: '+str(len(self.mtrls))+'\n\n'+\
        '===========\nRegion Data\n===========\n')
    for rgn in self.rgns:
      rgn.printAll(outFile)
    outFile.writelines('===============\nMaterial Status\n===============\n')
    for mtrl in self.mtrls:
      mtrl.printAll(outFile)
    outFile.writelines('==========\nBoundaries\n==========\n')
    for bd in self.bounds:
      bd.printAll(outFile)
    outFile.close()
    print '\nCurrent mesh data output to',self.case+'.dat for revew.\n'

  def findWidth(self):
    self.width=0
    for rgn in self.rgns:
      self.width+=rgn.width
