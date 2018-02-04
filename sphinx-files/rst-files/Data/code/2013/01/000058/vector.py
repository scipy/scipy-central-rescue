"""
Author Hari P Khanal 
Florida Internatinal University 
@2012

This module simply gives the vector algebra
-> adding , multiplying , substracting
-> Vector and Scaler product
-> Angle between two vectors
-> Polar and azimuthal angle of a given vector
-> Vectors interms of spherical coordinate
-> Rotation of vector in given angle
->Some examples 
 In [8]: v1 = Vector3D(1, 2, 3)

In [9]: v2 = Vector3D(2, 3, 5)

In [10]: v = v1+v2

In [11]: print v
(3 , 5, 8)

In [12]: v1.Angle(v2)
Out[12]: 0.028386648404655365

In [13]: v2.Dot(v1)
Out[13]: 37

In [14]: v1.Theta()
Out[14]: 0.6405223126794246

In [15]: v2.Phi()
Out[15]: 1.1071487177940904

In [16]: v1.Cross(v2)
Out[16]: <vector3d.Vector3D instance at 0x2040950>

In [17]: print v1.Cross(v2)
(1 , 2, 3)

In [18]: v1.Mag2()
Out[18]: 14
"""
import numpy as np
import math
class Vector3D:
   def __init__(self, x, y , z):
       self.x = x
       self.y = y
       self.z = z

   def setXYZ(self, x, y, z):
      self.x = x
      self.y =y
      self.z =z

   def getXYZ(self):
      
      return (self.x, self.y, self.z)

   def setX(self, x):
      self.x =x

   def setY(self, y):
      self.y =y

   def setZ(self, z):
      self.z =z

   def getX(self):
      return self.x

   def getY(self):
      return self.y

   def getZ(self):
      return self.z

   def __add__(self, other):      
       return Vector3D(self.x+other.x, self.y+other.y, self.z+other.z) 
 
   """ Substracting two vector"""

   def __sub__(self, other):
       
        return Vector3D(self.x - other.x, self.y- other.y, self.z -other.z)

   """ Vector multiplication by scaler"""
  
   def __mul__(self, c):
        
         return  Vector3D(self.x*c , self.y*c, self.z*c)

  
   """ Cross Product of two vector """
      

   def Cross(self, other):
      
         return Vector3D (self.y*other.z -self.z*other.y, self.z*other.x -self.x*other.z, self.x*other.y -self.y*other.x)

   """ Polar angle of a vector """

   def Theta(self):
        prep = np.sqrt(self.x *self.x +self.y*self.y)
        if(prep ==0 and self.z ==0):
           return 0
        return math.atan2(prep,self.z)

   """ Azimuthal angle of a vector """

   def Phi(self):
      if ( self.x ==0 and self.y ==0):
         return 0
      return math.atan2(self.y, self.x)
      
   """ Scalar Product of a vectors """

   def Dot(self, other):
       return (self.x* other.x + self.y* other.y+ self.z *other.z)   

   """ Angle between two vectors """
    
      
   def Angle(self, other):
       if (self.Dot(other) ==0 and self.Mag() ==0 and other.Mag() ==0):
               return 0
       return math.acos(self.Dot(other)/float(self.Mag()*other.Mag()))
              
   """ Magnitude square of a vector """     
   def Mag2(self):
       
       return (self.x*self.x +self.y*self.y +self.z*self.z)

   """ Magnitude of a vector """
   def Mag(self):
       return np.sqrt(self.Mag2())

   """ Rotation  a vector along X axis"""
   def RotateX (self, angle):
      s = math.sin(angle)
      c = math.cos(angle)
      self.y = self.y*c -self.z*s
      self.z = self.y*s +self.z*c
      return Vector3D(self.x, self.y, self.z)


   """ Rotation a vector along Y axis"""

   def RotateY (self, angle):
      s = math.sin(angle)
      c = math.cos(angle)
      self.x = self.z*s +self.x*c
      self.z = self.z*c - self.x*s
      return Vector3D(self.x, self.y, self.z)

   """ Rotation a vector along Z axis"""

   def RotateZ (self, angle):
      s = math.sin(angle)
      c = math.cos(angle)
      self.x = self.x*c -self.y*s
      self.y = self.x*s +self.y*c
      return Vector3D(self.x, self.y, self.z)

   """ Setting r , theta and phi for spherical coordinate system"""

   
   def setMagThetaPhi(self,mag, theta, phi):
      self.x = mag*math.sin(theta)*math.cos(phi)
      self.y = mag*math.sin(theta)*math.sin(phi)
      self.z = mag*math.cos(theta)
      return self.setXYZ(self.x, self.y, self.z)
      
  
   def setTheta(self, theta):
      # setting theta angle keeping phi and mag constant"
      mag = self.Mag()
      phi = self.Phi()
      self.x = mag*math.sin(theta)*math.cos(phi)
      self.y = mag*math.sin(theta)*math.sin(phi)
      self.z = mag*math.cos(theta)
      return self.setXYZ(self.x, self.y, self.z)
   
   """ Setting mag ,  keeping theta and phi constant"""
   
   def setMag(self, mag):
      phi = self.Phi()
      theta= self.Theta()
      self.x = mag*math.sin(theta)*math.cos(phi)
      self.y = mag*math.sin(theta)*math.sin(phi)
      self.z = mag*math.cos(theta)
      return self.setXYZ(self.x, self.y, self.z)
   """ Setting Phi angle ,  keeping magnitude and angle theta constant"""
   def setPhi(self, phi):
      mag = self.Mag()
      theta =self.Theta()
      self.x = mag*math.sin(theta)*math.cos(phi)
      self.y = mag*math.sin(theta)*math.sin(phi)
      self.z = mag*math.cos(theta)
      return self.setXYZ(self.x, self.y, self.z)      
      
   def __str__(self):
      return ("("+ str(self.x)+" , " +str(self.y) +", "+str(self.z)+")")



   """
   LorentzVector is derived from class Vector3D , which has some algebra but it has four componets , it helps 
   ->to calculate the  Manitude of four vectors 
   ->to Boost vector with certain velocity 
   ->to Caculat Energy and Momentum of given praticles ( E = sqrt( p*p +m*m))
   -> to Calculat the velocity and gamma from momentum and energy  beta = p/E
   gamma = sqrt(1.0/(1 -beta*beta))
   Examples:
   In [2]: v2 =LorentzVector(2, 3, 5, 1)

   In [3]: v2.Mag()
   Out[3]: 6.082762530298219

   In [4]: v2.M()
   Out[4]: 6.082762530298219

   In [5]: v2.BoostMat(0.91, 0.0, 0.0)
   Out[5]: 
   matrix([[ 2.19484297,  2.41191535,  0.        ,  0.        ],
        [ 0.        ,  0.        ,  1.        ,  0.        ],
        [ 0.        ,  0.        ,  0.        ,  1.        ],
        [ 2.41191535,  2.19484297,  0.        ,  0.        ]])

        In [6]: v2.Boost(0.91, 0.0, 0.0)

        In [7]: print v2
        (7.01867367134 , 3.0, 5.0,6.80160128975)

    """

class LorentzVector(Vector3D):
   
   def __init__(self, x, y, z, t):
      Vector3D.__init__(self, x, y, z)
      self.t = t

   def __add__(self, other):
      
      return  LorentzVector( self.x +other.x, self.y +other.y, self.z +other.z, self.t +other.t )

   def __sub__(self, other):
      
      return  LorentzVector(self.x -other.x, self.y -other.y, self.z -other.z, self.t -other.t )

   def setXYZT(self, x ,y,z, t):
      self.x = x
      self.y = y
      self.z = z
      self.t = t
   def setT(self, t):
      self.t = t
   def getXYZT(self):
      return LorentzVector(self.x, self.y, self.z, self.t)
   
   def setPxPyPzE(self, px, py, pz, E):
      self.x = px
      self.y = py
      self.z = pz
      self.t = E
   def getPxPyPzE(self):
      
      return LorentzVector(self.x, self.y, self.z, self.t)
   def setXYZM(self , x, y, z, m):
       # for particles 
      if m >= 0:
         self.setXYZT(x, y, z, math.sqrt(x*x +y*y +z*z +m*m))
      else:
         self.setXYZT(x, y, z, math.sqrt(x*x +y*y +z*z -m*m))
 
   def getT(self):
      return self.t
   def getPx(self):
      return self.x
   def getPy(self):
      return self.y

   def getPz(self):
      return self.z
   
   def getP(self):
      px = self.getPx()
      py = self.getPy()
      pz = self.getPz()
      return np.sqrt(px*px +py*py+pz*pz)
   def getE(self):
       return math.sqrt(self.getP()*self.getP() +self.M()*self.M())
   def Beta(self):
      P = self.getP()
      E = self.getE()
      if P ==0 and E ==0:
         return 0
      return float(P)/float(E)
   def Gama(self):
      return float(1.0/(1 -float(self.Beta()*self.Beta())))
   
   def ScalerProduct(self, other):
      ds = self.t*other.t - (self.x*other.x + self.y*other.y +self.x*other.y)
      return math.sqrt(ds)

   """ Using J.D.Jackson 11.19 """

   def Boost(self, bx, by , bz): 
       b = Vector3D(bx, by, bz)
       b2 =float(b.Mag2())
       gamma = float(1.0/(math.sqrt(1 -b2)))
       gamma2 = float((gamma -1)/b2)
       bp = self.getX() *bx + self.getY() *by +self.getZ()*bz
       self.setX(self.getX() + gamma2*bp*bx + gamma*bx*self.getT())
       self.setY(self.getY() + gamma2*bp*by + gamma*by*self.getT())
       self.setZ(self.getZ() + gamma2*bp*bz + gamma*bz*self.getT())
       self.setT(gamma*(self.getT() + bp));

   def BoostVector(self):
      return Vector3D(self.getX()/self.getT() , self.getY()/self.getT(),self.getZ()/self.getT())
   
   def Vect(self):   
      return Vector3D(self.getX() , self.getY(),self.getZ())

   def Mag2(self):
      vect = self.Vect()

      m2 = self.getT()*self.getT() -vect.Mag2()
      return m2
      
   def Mag(self):
      return math.sqrt(-self.Mag2())

   def M2(self):
      return self.Mag2()
   def M(self):
      return self.Mag()
   
   def BoostMat(self, bx, by, bz): # boost matrix or Lorentz matrix
       b = Vector3D(bx, by, bz)
       b2 =float(b.Mag2())
       gamma = float(1.0/(math.sqrt(1 -b2)))
       gamma2 = float((gamma -1)/b2)
       t_com = [gamma , gamma*bx, gamma*by, gamma*bz]
       x_com = [gamma*bx , 1+gamma2*bx*bx, gamma2*bx*by, gamma2*bx*bz]
       y_com = [gamma*by , gamma2*bx*by, 1+gamma2*by*by, gamma2*by*bz]
       z_com = [gamma*bz , gamma2*bz*bx, gamma2*bz*by, 1+gamma2*bz*bz] 
       X = np.array([x_com, y_com, z_com, t_com])
       Mat = np.mat(X)
       return Mat 
   def __str__(self):
        return ("("+ str(self.x)+" , " +str(self.y) +", "+str(self.z)+ "," + str(self.t) +")")
       




   



   
   
    
