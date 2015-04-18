#/usr/bin/python3
import numpy as np

def intgl_trapz(f,a,b,steps=-1,h=1):
    if steps>0:
        xis = np.linspace(a,b,steps+1)
        h  = xs[1]-xs[0]
    fxis = f(xs)
    wis = h*np.array([0.5]+[1.0]*(len(xs)-2)+[0.5])
    fapprox = lambda x: np.interp(x,xis,fxis)
    return (sum(fxs*ws),xis,fxis,wis,fapprox) # h/2 * sum(np.array([f(x) for x in xs]) * np.array([1]+[2]*(len(xs)-2)+[1]))

