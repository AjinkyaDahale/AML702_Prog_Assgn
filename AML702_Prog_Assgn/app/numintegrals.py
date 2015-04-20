#/usr/bin/python3
from __future__ import division
import numpy as np
import scipy.integrate as spintegrate
from scipy.interpolate import lagrange

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
    pcs = []; fpcs = []
    for i in xrange(0,steps-1,2):
        wis[i:i+3] += [1,4,1]
        pcs.append(xis[i:i+3])
        fpcs.append(fxis[i:i+3])
    wis *= h/3
    if steps%2:
        wis[-2:] += [h/2.0,h/2.0]
        pcs.append(xis[-2:])
        fpcs.append(fxis[-2:])
    # print(wis)
    fapprox = lambda x: np.piecewise(x,
                                     [np.logical_and(p[0]<=x,x<=p[-1]) for p in pcs],
                                     [lagrange(pcs[i],fpcs[i]) for i in xrange(len(pcs))])# np.interp(x,xis,fxis)
    return (sum(fxis*wis),xis,fxis,wis,fapprox) # h/2 * sum(np.array([f(x) for x in xs]) * np.array([1]+[2]*(len(xs)-2)+[1]))

def intgl_simp38(f,a,b,steps=-1,h=1):
    if steps>0:
        xis = np.linspace(a,b,steps+1)
        h  = xis[1]-xis[0]
    fxis = f(xis)
    wis = np.zeros(steps+1)
    pcs = []; fpcs = []
    for i in xrange(0,steps-2,3):
        wis[i:i+4] += [1,3,3,1]
        pcs.append(xis[i:i+4])
        fpcs.append(fxis[i:i+4])
    wis *= 3*h/8
    if steps%3==2:
        wis[-3:] += [h/3,4*h/3,h/3]
        pcs.append(xis[-3:])
        fpcs.append(fxis[-3:])
    elif steps%3==1:
        wis[-2:] += [h/2,h/2]
        pcs.append(xis[-2:])
        fpcs.append(fxis[-2:])
    fapprox = lambda x: np.piecewise(x,
                                     [np.logical_and(p[0]<=x,x<=p[-1]) for p in pcs],
                                     [lagrange(pcs[i],fpcs[i]) for i in xrange(len(pcs))])# np.interp(x,xis,fxis)
    # fapprox = lambda x: np.interp(x,xis,fxis)
    return (sum(fxis*wis),xis,fxis,wis,fapprox) # h/2 * sum(np.array([f(x) for x in xs]) * np.array([1]+[2]*(len(xs)-2)+[1]))

def intgl_glquad(f,a,b,n):
    ans = spintegrate.fixed_quad(f,a,b,n=n)
    xis,wis = np.polynomial.legendre.leggauss(n)
    # print(xis,wis)
    xis = (b+a)/2 + (b-a)/2*xis
    fxis = f(xis)
    wis = (b-a)/2*wis
    return (ans[0],xis,fxis,wis,lagrange(xis,fxis))

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
