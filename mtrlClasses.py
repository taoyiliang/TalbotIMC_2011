

class Material:
  def __init__(self,mesh='dudmesh',groupData=['name','1 10','10 100']):
    self.mesh=mesh
    self.name=groupData[0].strip() #material name
    self.groups=[] #holds group instances associated with material
    self.g=self.groups #shorthand for lengthy code lines

    groupData=groupData[1:] #chop off name part
    for data in groupData:
      self.groups.append(Group(self.mesh,self,data.split()))
    
  def printAll(self,outFile):
    outFile.writelines('Material: '+self.name+'\n'+\
        '  Number of Groups: '+str(len(self.g))+'\n\n')





class Group:
  def __init__(self,mesh,parent,data):
    self.mesh=mesh
    self.parent=parent
    self.lowE=float(data[0])
    self.highE=float(data[1])
    self.opac=self.getOpac

  def getOpac(self,temp,freq,gamma=1):
    import math
    return gamma/freq**3*(1-math.exp(-freq/temp))
