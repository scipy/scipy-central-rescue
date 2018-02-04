# License: Creative Commons Zero (almost public domain) http://scpyce.org/cc0
from __future__ import print_function, division
from pylab import *
import numpy as np
from scipy import stats


'''This script can be used to understand the relationship between the signal
absent and signal present distributions and the ROC curve which they generate.
The distributions are assumed to be Gaussian and of equal variance.
The sliders at the bottom can be used to change the position the mean of each
distribution as well as the threshold.

This code was influenced by the matplotlib slider demo:
matplotlib.sourceforge.net/examples/widgets/slider_demo.html'''

#Generate the x values that the two distributions will be plotted against 
x = linspace(0,25,100) 

#Create the figure and two subplots
fig = figure('ROC curve demonstration')
ax1 = fig.add_subplot(212)
ax2 = fig.add_subplot(211,aspect='equal',title='ROC curve',
        xlabel='1-specificity',ylabel='sensitivity')
subplots_adjust(bottom=0.25)


#Create the axes for the sliders
axthreshold  = axes([0.2, 0.15, 0.65, 0.03])#, axisbg=axcolor)
axmean1 = axes([0.2, 0.1, 0.25, 0.03])#, axisbg=axcolor)
axmean2  = axes([0.2, 0.05, 0.25, 0.03])#, axisbg=axcolor)
axstd1 = axes([0.6, 0.1, 0.25, 0.03])#, axisbg=axcolor)
axstd2 = axes([0.6, 0.05, 0.25, 0.03])#, axisbg=axcolor)

#Plot the signal absent distribution
ax1.plot(x,stats.norm.pdf(x,loc=12)) 
ax1.plot(x,stats.norm.pdf(x,loc=13)) 

#Create sliders, and their initial values
threshold = Slider(axthreshold, 'Threshold', 5, 20.0, valinit=14)
mean1     = Slider(axmean1, 'Mean1', 5, 20.0, valinit=12)
mean2     = Slider(axmean2, 'Mean2', 5, 20.0, valinit=13)
std1 = Slider(axstd1, 'Std1', 0.1, 10, valinit = 1)
std2 = Slider(axstd2, 'Std1', 0.1, 10, valinit = 1)

def roc_curve(threshold_values,mean1,mean2,std1=1,std2=1):
    '''This function returns and an array of sensitivity and 1 - specificity
    values from the given threshold values'''
    sensitivity = zeros(threshold_values.size)
    one_minus_specificity = zeros(threshold_values.size)
    for index, value in enumerate(threshold_values):
        sensitivity[index] = 1 - stats.norm.cdf(value,loc=mean2, scale=std2)
        one_minus_specificity[index] = 1 - stats.norm.cdf(value,loc=mean1, scale=std1)
    return sensitivity, one_minus_specificity

'''
sensitivity, one_minus_specificity = roc_curve(x,12,13)
ax2.plot(one_minus_specificity,sensitivity,'b',linewidth=2)
mean1val = 12
mean2val = 13 
'''
def update(val):
    '''Updates the two distributions, threshold values, and point on the 
    ROC curve when the sliders are changes'''
    global mean1val
    global mean2val
    
    mean1val = mean1.val
    mean2val = mean2.val
    std1val = std1.val
    std2val = std2.val
    
    thresholdval = threshold.val
    
    ax1.cla()

    ax1.plot(x,stats.norm.pdf(x,loc=mean1val, scale=std1val)) 
    ax1.plot(x,stats.norm.pdf(x,loc=mean2val, scale=std2val)) 
    ax1.vlines(thresholdval,0,0.40,color='r')
    ax1.set_ylim(0,0.40)

    ax2.cla()
    sensitivity, one_minus_specificity = roc_curve(x,mean1val,mean2val,std1val, std2val)
    ax2.plot(one_minus_specificity,sensitivity,'b',linewidth=3)
    ax2.plot( 1 - stats.norm.cdf(thresholdval,loc=mean1val,scale=std1val),
            1 - stats.norm.cdf(thresholdval,loc=mean2val,scale=std2val),'ro')
    ax2.set_title('ROC curve')
    #xlabel = 'sensitivity'
    #ylabel = 'specificity'
    
    
    draw()

mean1.on_changed(update)
mean2.on_changed(update)
std1.on_changed(update)
std2.on_changed(update)
threshold.on_changed(update)
update(None)
show()