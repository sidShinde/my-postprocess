import numpy as np
import os, math
from tqdm import tqdm
from scipy.interpolate import griddata
from vgAnalysis.readers.reader_support_functions import *
from vgAnalysis.readers.reader import *
from .update_progress import *

__all__ = ['get_two_point_corr', 'get_grid']

def get_grid(filePath, arrName, timeDirs, delta, yw, nPts, periodic):
    readFile = False
    count    = int( 0 )

    while (readFile == False):
        try:
            fpath = filePath + '/' + timeDirs[ count ] + '/' + arrName
            points = get_data( fpath + '/faceCentres', skiprows=3 )
            readFile = True
        except:
            count = count + 1

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

    if periodic == 'true':
        zcoord = zcoord - zcoord[0]

    return points, yGrid, zGrid, ycoord, zcoord


def get_two_point_corr(filePath, arrName, timeDirs, points, yGrid, zGrid,
                       periodic, rank, localN):

    if rank == 0:
        minT = int(0)
    else:
        minT = int( np.sum( localN[:rank] ) )

    maxT = int( np.sum( localN[:rank+1] ) )
    skippedFiles = 0

    for i in range( minT, maxT ):
        fpath  = filePath + '/' + timeDirs[i] + '/' + arrName

        # interpolate velocity field:
        try:
            U     = get_data( fpath + '/vectorField/U', skiprows=3)
            UMean = get_data( fpath + '/vectorField/UMean', skiprows=3)
        except:
            skippedFiles += 1
            continue

        UPrime = U - UMean

        upx = griddata( (points[:, 2], points[:, 1]), UPrime[:, 0],
                      (zGrid, yGrid), method='cubic' )

        upy = griddata( (points[:, 2], points[:, 1]), UPrime[:, 1],
                      (zGrid, yGrid), method='cubic')

        upz = griddata( (points[:, 2], points[:, 1]), UPrime[:, 2],
                      (zGrid, yGrid), method='cubic')

        # number of points in y:
        [ny, nz] = yGrid.shape

        if i == minT:
            tpcX = np.zeros([ny, nz])
            tpcY = np.zeros([ny, nz])
            tpcZ = np.zeros([ny, nz])

            tpcX = two_point_corr_eval(upx, ny, nz)
            tpcY = two_point_corr_eval(upy, ny, nz)
            tpcZ = two_point_corr_eval(upz, ny, nz)

        else:
            tpcX += two_point_corr_eval(upx, ny, nz)
            tpcY += two_point_corr_eval(upy, ny, nz)
            tpcZ += two_point_corr_eval(upz, ny, nz)

        if rank == 0:
            update_progress( (i+1) / (maxT) )

    tpcX = tpcX/(maxT - minT - skippedFiles)
    tpcY = tpcY/(maxT - minT - skippedFiles)
    tpcZ = tpcZ/(maxT - minT - skippedFiles)

    return tpcX, tpcY, tpcZ


def two_point_corr_eval(up, ny, nz):
    tpc = np.zeros([ny, nz])

    for i in range(ny):
        for j in range(nz):
            for k in range(0, nz-j):
                counter = k + j
                tpc[i, j]  = tpc[i, j] + up[i, k] * up[i, counter]

        tpc[i, :] = tpc[i, :]/tpc[i, 0]

    return tpc
