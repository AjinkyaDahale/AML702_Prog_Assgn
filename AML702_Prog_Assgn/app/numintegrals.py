#/usr/bin/python3
import numpy as np

def intgl_trapz(f,a,b,steps=-1,h=1):
    if steps>0:
        xs = np.linspace(a,b,steps)
        h  = xs[1]-xs[0]
    return h/2 * sum(np.array([f(x) for x in xs]) *
           np.array([1]+[2]*(len(xs)-2)+[1]))

