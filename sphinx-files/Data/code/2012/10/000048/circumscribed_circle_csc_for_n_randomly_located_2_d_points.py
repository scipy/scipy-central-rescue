# License: Creative Commons Zero (almost public domain) http://scpyce.org/cc0
# similar to: http://www.scipy.org/Cookbook/Finding_Convex_Hull
#***********************
#Nomenclature:
#-------------
#CSC=CircumScribedCircle
#BBox=BoundingBox

#see UNIT TEST (below)
#***********************

from Tkinter import *
import random
import math

#deg2rad:
dr=math.pi/180.0
#==========================================================
def get_MinMax(pList):
    """
    called by: get_CSC(...)
    input: pList--> list of N randomly located points as xy-tuples
    returns: list of tuples for xmin,ymin,xmax,ymax extracted from pList
    """
    N=len(pList)
    minX=999
    minY=999
    maxX=-999
    maxY=-999
    for i in range(N):
        x,y=pList[i]
        if x<=minX:
            minX=x
            minX_Point=(x,y)
        if y<=minY:
            minY=y
            minY_Point=(x,y)
        if x>=maxX:
            maxX=x
            maxX_Point=(x,y)
        if y>=maxY:
            maxY=y
            maxY_Point=(x,y)

    return [minX_Point,minY_Point,maxX_Point,maxY_Point]
#---------------------------------------------------
def get_CSC_Ctr(MinMax_Points):
    """
    called by: get_CSC(...)
    input: list of tuples for xmin,ymin,xmax,ymax (extracted from pList)
    returns: center (tuple) for CSC
    """

    xMin,y=MinMax_Points[0]
    x,yMin=MinMax_Points[1]
    xMax,y=MinMax_Points[2]
    x,yMax=MinMax_Points[3]

    xCtr=0.5*(xMin+xMax)
    yCtr=0.5*(yMin+yMax)

    return (xCtr,yCtr)
#-------------------------------------------------------
def get_CSC_R(CSC_Ctr,MinMax_Points):
    """
    called by: get_CSC(...)
    input: tuple for CSC's center  & tuples for xmin,ymin,xmax,ymax
    returns: max distance associated with xmin,ymin,xmax,ymax
    """
    Rmax=-999
    xmin,y=MinMax_Points[0]
    R=dist(CSC_Ctr[0],CSC_Ctr[1],xmin,y)
    if R>=Rmax: Rmax=R

    x,yMin=MinMax_Points[1]
    R=dist(CSC_Ctr[0],CSC_Ctr[1],x,yMin)
    if R>=Rmax: Rmax=R

    xMax,y=MinMax_Points[2]
    R=dist(CSC_Ctr[0],CSC_Ctr[1],xMax,y)
    if R>=Rmax: Rmax=R

    x,yMax=MinMax_Points[3]
    R=dist(CSC_Ctr[0],CSC_Ctr[1],x,yMax)
    if R>=Rmax: Rmax=R

    return Rmax
#--------------------------------------
def get_CSC_BBox(CSC_Ctr,R):
    """
    returns BBoxcoords for CSC
    """
    x1=CSC_Ctr[0]+R*math.cos(180.0*dr)
    y1=CSC_Ctr[1]+R*math.sin(-90.0*dr)
    x2=CSC_Ctr[0]+R*math.cos(0.0*dr)
    y2=CSC_Ctr[1]+R*math.sin(90.0*dr)

    return [x1,y1,x2,y2]
#--------------------------------------
def get_CSC(pList):
    """
    this function is called by MAIN
    returns: cooords (list) for CSC, displayed by MAIN
    """
    MinMax_Points=get_MinMax(pList)
    CSC_Ctr=get_CSC_Ctr(MinMax_Points)
    R=get_CSC_R(CSC_Ctr,MinMax_Points)
    coords=get_CSC_BBox(CSC_Ctr,R)
    return coords
#===================================================
def dist(x1,y1,x2,y2):
    """distance between two points """
    return ((x1-x2)**2+(y1-y2)**2)**0.5
#=================== MAIN: UNIT TEST ===========================
if __name__ == "__main__":

    """
    display on a canvas the CSC for N randomly located oints
    """

    root=Tk()

    #create a 200x2000 Canvas
    w=200
    h=200
    cv=Canvas(root,width=w,height=w,bg="yellow")
    cv.pack()

    #create a list of N random points within a circular area

    N=60
    pList=[]
    for i in range(N):
        #circular area:
        R=random.randint(0,int(0.25*w))
        a=random.randint(0,360)
        xR=R*math.cos(a*dr)
        yR=R*math.sin(a*dr)
        #shift wrt ctr 0.5*(w,h):
        x=0.5*w+xR
        y=0.5*h+yR

        #display:
        coord=[x-3,y-3,x+3,y+3]
        cv.create_oval(coord,fill="black")

        pList.append((x,y))

    #**********************************************
    #Note:
    #pList could also be read from an external file
    #**********************************************

    coords=get_CSC(pList)
    cv.create_oval(coords,width=1,outline="red")

    root.mainloop()


