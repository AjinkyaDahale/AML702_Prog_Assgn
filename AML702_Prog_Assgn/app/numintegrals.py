#/usr/bin/python3
from __future__ import division
import numpy as np
import scipy.integrate as spintegrate

def intgl_trapz(f,a,b,steps=-1,h=1):
    if steps>0:
        xis = np.linspace(a,b,steps+1)
        h  = xis[1]-xis[0]
    fxis = f(xis)
    wis = h*np.array([0.5]+[1.0]*(len(xis)-2)+[0.5])
    fapprox = lambda x: np.interp(x,xis,fxis)
    return (sum(fxis*wis),xis,fxis,wis,fapprox) # h/2 * sum(np.array([f(x) for x in xs]) * np.array([1]+[2]*(len(xs)-2)+[1]))
    
def intgl_simp13(f,a,b,steps=-1,h=1):
    if steps>0:
        xis = np.linspace(a,b,steps+1)
        h  = xis[1]-xis[0]
    fxis = f(xis)
    wis = np.zeros(steps+1)
    for i in xrange(0,steps-1,2): wis[i:i+3] += [1,4,1]
    wis *= h/3
    if steps%2:
        wis[-2:] += [h/2.0,h/2.0]
    # print(wis)
    fapprox = lambda x: np.interp(x,xis,fxis)
    return (sum(fxis*wis),xis,fxis,wis,fapprox) # h/2 * sum(np.array([f(x) for x in xs]) * np.array([1]+[2]*(len(xs)-2)+[1]))

def intgl_simp38(f,a,b,steps=-1,h=1):
    if steps>0:
        xis = np.linspace(a,b,steps+1)
        h  = xis[1]-xis[0]
    fxis = f(xis)
    wis = np.zeros(steps+1)
    for i in xrange(0,steps-2,3): wis[i:i+4] += [1,3,3,1]
    wis *= 3*h/8
    if steps%3==2:
        wis[-3:] += [h/3,4*h/3,h/3]
    elif steps%3==1:
        wis[-2:] += [h/2,h/2]
    fapprox = lambda x: np.interp(x,xis,fxis)
    return (sum(fxis*wis),xis,fxis,wis,fapprox) # h/2 * sum(np.array([f(x) for x in xs]) * np.array([1]+[2]*(len(xs)-2)+[1]))

def intgl_glquad(f,a,b,n):
    ans = spintegrate.fixed_quad(f,a,b,n=n)
    return (ans[0],[],[],[],lambda x: np.zeros(np.shape(x)))

if __name__ == '__main__':
    import pylab as pl
    f = np.sin; a = -np.pi; b = np.pi
    n = 1000
    xs = np.linspace(a, b, n, endpoint=True)
    fxs = f(xs)
    fxexactplot = pl.plot(xs, fxs, color='black', label='f(x)')
    fapprox = intgl_trapz(f,a,b,steps=4)[-1]
    fxapproxplot = pl.plot(xs, fapprox(xs), color='blue', label='Method 1')
    pl.show()
