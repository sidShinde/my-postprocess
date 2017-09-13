import numpy as np
import os, math
from tqdm import tqdm
from scipy.interpolate import griddata
from vgAnalysis.readers.reader_support_functions import *
from vgAnalysis.readers.reader import *

__all__ = ['get_two_point_corr']

def get_two_point_corr(filePath, arrName, timeDirs, delta, yw, nPts, periodic):

    for i in tqdm( range( len(timeDirs) ), ncols=100 ):
        fpath  = filePath + '/' + timeDirs[i] + '/' + arrName

        points = get_data( fpath + '/faceCentres', skiprows=3 )
        U      = get_data( fpath + '/vectorField/U', skiprows=3)
        UMean  = get_data( fpath + '/vectorField/UMean', skiprows=3)
        UPrime = U - UMean

        # interpolate data:
        points = points / delta
        zcoord = np.unique( points[:, 2] )
        nz     = zcoord.shape[0]

        if periodic == 'true':
            nz = math.floor( nz/ 2 )
            zcoord = zcoord[nz:]

        zcoord[0]  = (zcoord[0] + zcoord[1])/2
        zcoord[-1] = (zcoord[-1] + zcoord[-2])/2

        ymin       = np.min( points[:, 1] )
        ycoord     = np.linspace( ymin, yw, nPts )
        ycoord[0]  = (ycoord[0] + ycoord[1])/2
        ycoord[-1] = (ycoord[-1] + ycoord[-2])/2

        zGrid, yGrid = np.meshgrid( zcoord, ycoord )

        upx = griddata( (points[:, 2], points[:, 1]), UPrime[:, 0],
                      (zGrid, yGrid), method='cubic' )
        upy = griddata( (points[:, 2], points[:, 1]), UPrime[:, 1],
                      (zGrid, yGrid), method='cubic')
        upz = griddata( (points[:, 2], points[:, 1]), UPrime[:, 2],
                      (zGrid, yGrid), method='cubic')

        # number of points in y:
        ny = nPts

        if i == 0:
            tpcX = np.zeros([ny, nz])
            tpcY = np.zeros([ny, nz])
            tpcZ = np.zeros([ny, nz])

            tpcX = two_point_corr_eval(upx, ny, nz, periodic)
            tpcY = two_point_corr_eval(upy, ny, nz, periodic)
            tpcZ = two_point_corr_eval(upz, ny, nz, periodic)

        else:
            tpcX += two_point_corr_eval(upx, ny, nz, periodic)
            tpcY += two_point_corr_eval(upy, ny, nz, periodic)
            tpcZ += two_point_corr_eval(upz, ny, nz, periodic)

    tpcX = tpcX/(i+1)
    tpcY = tpcY/(i+1)
    tpcZ = tpcZ/(i+1)

    if periodic == 'true':
        zcoord = zcoord - zcoord[0]

    return tpcX, tpcY, tpcZ, ycoord, zcoord


def two_point_corr_eval(up, ny, nz, periodic):
    tpc = np.zeros([ny, nz])

    for i in range(ny):
        for j in range(nz):
            for k in range(0, nz-j):
                counter = k + j
                tpc[i, j]  = tpc[i, j] + up[i, k] * up[i, counter]

        tpc[i, :] = tpc[i, :]/tpc[i, 0]

    return tpc
