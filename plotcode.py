#Plotcode

#Siehe Kommentare zum Bifurkationscode
#Code dient der Darstellung von bestimmten Trajektorien 

from scipy.integrate import odeint
import numpy as np
import pylab as pl
from math import *
from numpy import *

k = 1.0
w0 = 1.0
a = 0.1 

# van der pol oszillatorgleichungen
def F(X,t):
    y1, y2 = X
    return [y2, -k*(y1**2 -a)*y2 -y1*w0**2]

t1 = np.linspace(0, 150, 1501)

def traj(y10, y20):
    erg, info = odeint(F, (y10, y20), t1, full_output=True)
    y1, y2 = erg.transpose() 
    pl.plot(y1,y2)

y10s = np.linspace(-1, 1, 3)
for y10 in y10s:
    y20s = np.linspace(-1, 1, 3)
    for y20 in y20s:
            traj(y10, y20)

## fps
pl.plot(0, 0, 'ko')

pl.xlim(-2,2)
pl.xlabel('y1')
pl.ylabel('y2')
pl.title('Phasenraumplot')
pl.show()

