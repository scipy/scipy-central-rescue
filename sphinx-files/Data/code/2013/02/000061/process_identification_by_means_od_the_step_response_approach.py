from pylab import *

def steptestingtxt(File, ColTime=0, ColInput=1, ColResponse=2, Summary='off',ExportTxt='off'):
    '''
    STEPTESTINGTXT
    Approximation of a response characterization curve to a FOPDT dynamics.

    Syntax:  steptesting(FILE,COLTIME,COLINPUT,COLRESPONSE,SUMMARY)

    BRIEF DESCRIPTION
    This function loads a file and computes the parameters of a First-Order-Plus-Deat-Time (FOPDT) dynamics 
    approximation for the given response curve (RESPONSE vs TIME) to the given step input function (INPUT vs 
    TIME). Where TIME, INPUT, and RESPONSE corresponds to the columns COLTIME, COLINPUT, and COLRESPONSE, 
    respectively.

    The reported parameters are: the gain (K), the time constant (TAU), and the time delay (t0). 
    These ones correspond to a FOPDT dynamics given by the following transfer function:

                    K.e^(-t0.s)      Y(s)      RESPONSE(s)
           G(s) = --------------- = ------ = ---------------
                    TAU.s + 1        U(s)       INPUT(s)

    where Y(s) and U(s) are the Laplace transforms of the deviation variables:

           U(t) = u(t)-u(0)    , and
           Y(t) = y(t)-y(0)

    which correspond to the INPUT and RESPONSE variables, respectively.

    SUMMARY corresponds to a 'on'/'off' switch for showing or not a summary table
    besides the resulting plots.

    Created by Ospino P.,J. 
    Colombia, 2012.
    '''    
# License: Creative Commons Zero (almost public domain) http://scpyce.org/cc0


    A=loadtxt(File)
       	
    Time=A[:,ColTime][:,newaxis]
    Input=A[:,ColInput][:,newaxis]
    Response=A[:,ColResponse][:,newaxis]

    clf()

    # Data format
    sizet=shape(Time)
    sizeu=shape(Input)
    sizey=shape(Response)

    if sizet[0]>=sizet[1]:
        t=Time
    else:
        t=Time.T

    if sizeu[0]>=sizeu[1]:
        u=Input
    else:
        u=Input.T

    if sizey[0]>=sizey[1]:
        y=Response
    else:
        y=Response.T

    # Gain
    K=(y[-1]-y[0])/(u[-1]-u[0])

    # Y-coordinates of t1 and t2
    yt1=y[0]+0.283*(y[-1]-y[0])
    yt2=y[0]+0.632*(y[-1]-y[0])

    # LINEAR INTERPOLATION
    for j in range(2,size(t)): #j=2:length(t)
        if (y[j-1]<=yt1) and (y[j]>=yt1): 
            a1=y[j-1]
            ta1=t[j-1]
            b1=y[j]
            tb1=t[j]

        if (y[j-1]<=yt2) and (y[j]>=yt2): 
            a2=y[j-1]
            ta2=t[j-1]
            b2=y[j]
            tb2=t[j]

    # Values of t1 and t2
    t1=((yt1-a1)/(b1-a1))*(tb1-ta1)+ta1
    t2=((yt2-a2)/(b2-a2))*(tb2-ta2)+ta2

    # Time constant
    Tau=3.0*(t2-t1)/2.0

    # Time delay
    t0=t2-Tau

    # FOPDT plot
    u2 = empty_like(t)
    ystar = empty_like(t)
    for j in range(size(t)):    # for j=1:length(t)
        if t[j]<(1+t0):
            u2[j]=0
        else:
            u2[j]=1            
        ystar[j]=K*(u[-1]-u[0])*u2[j]*(1-exp(-(t[j]-t0)/Tau))+y[0]

    # Error and deviation
    Deviation=ystar-y
    Error = empty(size(t)) 
    for j in range(size(t)):    # for j=1:length(t)
        if Deviation[j]==0:
            if y[j]>0:
                Error[j]=100*abs(Deviation[j])/y[j]
            else:
                Error[j]=0
        else:
            if y[j]>0:
                Error[j]=100*abs(Deviation[j])/y[j]
            else:
                Error[j]=0

    StdDeviation=sqrt(sum((ystar-y)**2)/(size(t)-1));

    subplot(2,3,1)
    plot(t,u,'b-')
    xlabel('Time'), ylabel('Step input, u') 
    xlim(t[0],t[-1]), ylim(0.95*min(u),1.05*max(u))  
    grid()

    subplot(2,3,2)
    plot(t,y,'k.')
    xlabel('Time'), ylabel('Original response, y') 
    #xlim(t[0],t[-1]), ylim(0.95*min(y),1.05*max(y))   
    grid()

    subplot(2,3,3)
    plot(t,ystar,'r-')
    xlabel('Time'), ylabel('FOPDT response, y*') 
    #xlim(t[0],t[-1]), ylim(0.95*min(ystar),1.05*max(ystar))   
    grid()

    subplot(2,3,4)
    plot(t,y,'k.',t,ystar,'r-')
    xlabel('Time'), ylabel('Response curve')
    #xlim(t[0],t[-1]), ylim(0.95*min(min(y),min(ystar)),1.05*max(max(y),max(ystar))) 
    legend(('Original','FOPDT'),loc='lower right')
    grid()

    subplot(2,3,5)  
    plot(t,Deviation,'b-')
    xlabel('Time'), ylabel('Deviation = y*(t)-y(t)') 
    #xlim(t[0],t[-1]), ylim(0.95*min(Deviation),1.05*max(Deviation))
    grid()

    subplot(2,3,6)  
    plot(t,Error,'r-')
    xlabel('Time'), ylabel('Deviation Error (%)') 
    #xlim(t[0],t[-1]), ylim(0.95*min(Error), 1.05*max(Error))
    grid()
    show()
      
    print('RESULTS')
    print(' ')  
    print('    Parameters of the FOPDT approximation')
    print(' ')
    print '   K = ', K
    print '   Tau = ', Tau
    print '   t0 = ', t0
    print(' ')
    print(' ')
    
    tu = concatenate((t,u),axis=1)   #[t u y ystar Deviation]
    tuy = concatenate((tu,y),axis=1)
    tuyystar = concatenate((tuy,ystar),axis=1)
    summarytable = concatenate((tuyystar,Deviation),axis=1)
    
    if Summary == 'on':
        print('     Summary Table')
        print('    ----------------------------------------------------')
        print('       t       u           y         y*       Deviation')
        print('    ------   ------     ------     ------     ----------')        
        print summarytable
        print('    ----------------------------------------------------')    
        print '   Standard deviation = ', StdDeviation
        print(' ')
        print(' ')
        return summarytable
    if Summary == 'off':
        pass
    
    if ExportTxt == 'on': 
        archive = open('Summary Table.txt','w')
        archive.write('#Result Summary Table \n')
        archive.write('#----------------------------------------------------\n')
        archive.write('#  t       u           y         y*       Deviation \n')
        archive.write('#------   ------     ------     ------     ----------\n')
        for row in summarytable:
            textline = '%f    %f    %f    %f    %f \n' %(row[0],row[1],row[2],row[3],row[4])
            archive.write(textline)
        archive.write('----------------------------------------------------\n')
        archive.write(  '#Standard Deviation = %f' %StdDeviation)
        archive.write(' ')
        archive.close()

    print('     Final dynamic equation')
    print(' ')
    print '    ', Tau, '*(dy[t]/dt)+ y[t]= ', K, '*u[t-', t0, ']'
    print(' ')