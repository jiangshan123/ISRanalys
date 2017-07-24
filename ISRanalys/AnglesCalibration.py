
# coding: utf-8

# # Calibrate the angles using STO peak position
import h5py
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.optimize import fsolve


def wavelenth(energy): #energy unit: keV
    h = 4.135667662 * 10**(-18) #keV*s Planck constant
    c = 2.99792458 * 10**18 #A speed of light
    return h*c/energy

def degtoarc (deg):
    """converts degree to arcs
    deg: float
    returns: float
    """
    return deg/180*np.pi

def arctodeg (arc):
    """converts arcs to degree
    arc: float
    returns: float
    """
    return arc*180/np.pi

def AnglesToQ(lamda, th, zeta, delta, nu): # angles should be numpy arrays.
    #convert all degrees to arc.
    th_a = degtoarc(th)
    zeta_a = degtoarc(zeta)
    delta_a = degtoarc(delta)
    nu_a = degtoarc(nu)
    Qx = 2.0 * np.pi / lamda * (np.cos(th_a)*np.sin(delta_a)-np.sin(th_a)*((np.cos(zeta_a)*(np.cos(nu_a)*np.cos(delta_a)-1)+np.sin(zeta_a)*np.sin(nu_a)*np.cos(delta_a))))
    Qy = 2.0 * np.pi / lamda * (np.sin(th_a)*np.sin(delta_a)+np.cos(th_a)*((np.cos(zeta_a)*(np.cos(nu_a)*np.cos(delta_a)-1)+np.sin(zeta_a)*np.sin(nu_a)*np.cos(delta_a))))
    Qz = 2.0 * np.pi / lamda * (-np.sin(zeta_a)*(np.cos(nu_a)*np.cos(delta_a)-1) + np.cos(zeta_a)*np.sin(nu_a)*np.cos(delta_a)) + th * 0.0
    return Qx, Qy, Qz
lamda = wavelenth(11.3001)



def QTohkl(a, Qx, Qy, Qz): # a is the lattice prameter of STO
    return a / (2.0 * np.pi) * Qx, a / (2.0 * np.pi) * Qy, a /(2.0 * np.pi) * Qz #return h, k, l

def QToCA (Qx, Qz): ##converting Qx and Qz to a and c
    return (2.0 * np.pi)/Qx, (2.0 * np.pi)/Qz ##returns a, c

dtheta = (75.0*10**(-6))/(35.0*10**(-2))*180.0/np.pi # angle per pixel


def STOcalibration(lamda,a,x,y,zeta):
    def equations(i):
        lamda = wavelenth(11.3001)
        a = 3.9066
        th, delta, nu = i[0], i[1], i[2]
        Qx, Qy, Qz = AnglesToQ(lamda, th, zeta, delta, nu)
        h, k, l = QTohkl(a, Qx, Qy, Qz)
        return(h-1.0, k ,l-1.0)
    s = fsolve(equations,[1, 1, 1])
    for i in range(3):
        while s[i]>180.0:
            s[i] -= 360.0
        while s[i]<-180.0:
            s[i] += 360.0
    th, delta, nu = s[0], s[1], s[2]

    return th, float(x)-delta/dtheta, float(y)+nu/dtheta #return th, (x_offset, y_offset)

zeta = 12
th, x_offset, y_offset = STOcalibration(lamda,3.9066,748,299,zeta)
def PixelsToAngles(x,y): # x and y are numpy arrays.
    return dtheta * (x - x_offset), -dtheta * (y - y_offset) #return delta, nu