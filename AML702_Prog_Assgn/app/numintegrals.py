#/usr/bin/python3
import numpy as np

def intgl_trapz(f,a,b,steps=-1,h=1):
    if steps>0:
        xis = np.linspace(a,b,steps+1)
        h  = xis[1]-xis[0]
    fxis = f(xis)
    wis = h*np.array([0.5]+[1.0]*(len(xis)-2)+[0.5])
    fapprox = lambda x: np.interp(x,xis,fxis)
    return (sum(fxis*wis),xis,fxis,wis,fapprox) # h/2 * sum(np.array([f(x) for x in xs]) * np.array([1]+[2]*(len(xs)-2)+[1]))

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
