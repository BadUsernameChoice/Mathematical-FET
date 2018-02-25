# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 20:18:34 2018

@author: Flachdenker
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm 


R = 6730

def rhoFK(x, y): 
    return np.sqrt(x**2 + y**2)
def phiFK(x, y): 
    phi0 = np.arctan(y/x)
    s = np.sign(x)
    return phi0 + (np.ones_like(s) + s)*(np.pi/2)

def rhoNewFP(rhoOld, rhoA, phiOld, phiA):
    a = np.sin(rhoOld/R)*np.sin(rhoA/R)*np.cos(phiOld-phiA)
    b = np.cos(rhoOld/R)*np.cos(rhoA/R)
    return R*np.arccos(a+b)
def phiNewFK(xOld, yOld, aX, aY):
    return phiFK(xOld-aX, yOld-aY)

def rhoNewFK(xOld, yOld, aX, aY):
    return rhoNewFP(rhoFK(xOld,yOld), rhoFK(aX,aY), phiFK(xOld,yOld), phiFK(aX,aY))
def phiNewFP(rhoOld, rhoA, phiOld, phiA):
    return abs(phiOld-phiA)%np.pi


def colorPlot3(nCount, func, x0=0, y0=0, label=None):
    x = np.linspace(x0-R*np.pi, x0+R*np.pi, nCount)
    y = np.linspace(y0-R*np.pi, y0+R*np.pi, nCount)
    X, Y = np.meshgrid(x, y) 
    Z = func(X, Y)#%1
    plt.pcolormesh(X, Y, Z, cmap=cm.hot, label=label)
    plt.colorbar(label=label)
    plt.axes().set_aspect('equal', 'datalim')

def getFunc(aX, aY):
    aRho, aPhi = rhoFK(aX, aY), phiFK(aX, aY)
    def func(x, y):
        rho, phi = rhoFK(x, y), phiFK(x, y)
        return rhoNewFP(rho, aRho, phi, aPhi)
    return func

def plotFieldFromA(a = (-R, .8*R), res=400):
    def pointToStr(p): 
        s0 = '$(%.f, %.f)$' if rhoFK(p[0], p[1])>2 else '$(%.3g, %.3g)$'
        return s0 % (p[0], p[1])
    D = R*np.pi
    colorPlot3(res, getFunc(a[0], a[1]), label='distance')
    plt.plot([a[0]], [a[1]], 'rx', label='origin\n'+pointToStr(a))
    if(rhoFK(a[0], a[1]) > D):
        bX, bY = (a[0]+D)%(2*D) - D, (a[1]+D)%(2*D) - D
        plt.plot([bX], [bY], 'rx', alpha=.666, label='false origin\n'+pointToStr((bX, bY)))
    t = np.linspace(0, 2*np.pi, 100)
    plt.title('Distance from orgin in different\nCoordinatesystem on spherical surface\nwith Radius $R=%g$' % R)
    plt.plot(D*np.cos(t), D*np.sin(t), 'g--', label='edge')
    plt.xlim(-D, D)
    plt.ylim(-D, D)
    plt.legend()

plotFieldFromA(res=200)
