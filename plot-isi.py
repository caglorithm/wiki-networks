#!/usr/bin/python

#import np 
import sys
import matplotlib
matplotlib.use('Agg')
from pylab import *
from numpy import ma

#print "args: " + sys.argv[1]

tList = [] # leere Liste
List1 = []
List2 = []
List3 = []
List4 = []
List5 = []

v = {}
ax = {'ymin' : 0}

f = open(sys.argv[1])

for line in f:
    line = line.rstrip() 
    parts = line.split()
    tList.append(float(parts[0]))
    List1.append(float(parts[1]))
#    List2.append(float(parts[4]))

figure(num=None, figsize=(20, 10), dpi=500, facecolor='w', edgecolor='k')
#subplot(211)
plot(tList,List1,'r')

#axis([25,700,0,50])
plt.xlabel(r'Nodes',fontsize=30)
plt.ylabel(r'Links',labelpad=10,fontsize=30)
#xticks(arange(0,5,0.1),fontsize='x-large')
yticks(fontsize='x-large')
grid()

#axis([0,1,0,5.2])
#axis(*v,**ax)
#subplot(212)
#plot(tList,List2,'bo')
#axis(*v,**ax)


savefig(sys.argv[1]+'-output.png')
#show()
