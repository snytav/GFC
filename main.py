from sympy import *
from mpmath import *
import numpy as np
import matplotlib.pyplot as plt
import re


def read_gfc():
    file1 = open('eigen-5s.gfc', 'r')
    count = 0

    while True:
        count += 1

        # Get next line from file
        line = file1.readline()

        fnd = line.find('end_of_head')
        if line.find('max_degree') >= 0:
            nums = line.split(' ')
            nums =[i for i in nums if i != '']
            max_degree = int(nums[1])
        # n  = int(nums[1])
        # if line is empty
        # end of file is reached
        if not line or fnd >= 0:
            break
        print("Line{}: {}".format(count, line.strip()))

    #file2 = open('geo.csv', 'w')
    #file2.write(key_string)
    koef = np.zeros((max_degree+1,max_degree+1))
    n = 0
    m = 0
    while m < max_degree and m < max_degree:
        count += 1

        # Get next line from file
        line = file1.readline()
        nums = line.split(' ')
        nums = [i for i in nums if i != '']
        n  = int(nums[1])
        m  = int(nums[2])
        cc = float(nums[3])
        ss = float(nums[4])
        if nums[0] != 'gfc' and nums[0] != 'gfct':
            continue
        koef[n][m] = cc
        koef[m-1][n] = ss

    file1.close()
    return koef

# parameters for harmonic evaluation at point
# mean radius    6378136.46
mr = 6378136.46
# fi             -1.5707963267949                 latitude
fi = -1.5707963267949
# al              0.020943951023932         WTF ? longitude
al = 0.188495559215388
# gamT            0

#       fi,                 al                      b_vbv
#       -1.5707963267949    0.0418879020478639      17.1071326611507





def sum_harmonics_at_point(fi,lb,mr,max_degree,koef):
    xp = fi
    xr = mr
    f = 0.0
    for m in range(max_degree):
        for n in range(max_degree):
            a = koef[n][m]
            b = koef[m-1][n]
            f += (a * np.cos(m * xp) + b*np.sin(m * xp)) * Float(legendre(n, xr))
    return f

from scipy .special import lpmn

def single_harmonics_at_point(fi,lb,mr,m,n,koef):

    if m == 0:
        b = 0
        a = 0
    else:
        a = koef[n][m]
        b = koef[m - 1][n]
    leg = lpmn(m,n,np.sin(fi))
    f = (a * np.cos(m * al) + b*np.sin(m * al)) * leg[0][0]
    return f


if __name__ == '__main__':
    #       fi,                 al                      b_vbv
    #       -1.5707963267949    0.0418879020478639      17.1071326611507
    fi = -1.5707963267949
    lb = 0.0

    koef = read_gfc()
    max_degree = koef.shape[0]-1

    # sungle harmonic impact
    m = 0
    n = 0
    fi  = -1.5707963267949
    al  = 0.0
    mr  = 6378136.46
    h = single_harmonics_at_point(fi, al, mr, m, n, koef)

    t =  sum_harmonics_at_point(fi,lb,mr,max_degree,koef)

    # reading grid file
    grid = np.loadtxt('testgrid.grid')
    latitude  = grid[0,:]
    longitude = grid[1,:]
    koef = read_gfc()
    max_degree = koef.shape[0]

    xr = mr
    for fi in latitude:
        for lb in longitude:
               xp = fi
               f = 0.0
               for m in range(max_degree):
                   for l in range(max_degree):
                       f += (a * np.cos(m * xp) + np.sin(m * xp)) * Float(legendre(l, xr))

    qq = 0

