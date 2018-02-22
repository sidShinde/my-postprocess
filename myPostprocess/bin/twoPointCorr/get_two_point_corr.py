import numpy as np
import os, math
from tqdm import tqdm
from scipy.interpolate import griddata
from myPostprocess.readers.reader_support_functions import *
from myPostprocess.readers.reader import *
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

    #idx    = [0, 1, 2, 3, nz-3, nz-2, nz-1, nz]
    rNz    = int( 0.08 * nz )
    idx1   = np.arange( rNz )
    idx2   = (nz-1) - rNz - np.arange( rNz )
    zcoord = np.delete(zcoord, idx1)
    zcoord = np.delete(zcoord, idx2)
    
    minZ   = zcoord.min()
    maxZ   = zcoord.max()
    nDelta = (maxZ - minZ)
    nz     = int( nDelta * 60 )  

    zcoord = np.linspace( minZ, maxZ, nz )
    
    if periodic == 'true':
        nz = math.floor( nz/ 2 )
        zcoord = zcoord[nz:]

    tempY      = np.unique( points[:, 1] )
    ymin       = tempY[2]
    ycoord     = np.linspace( ymin, ymin+yw, nPts )
    
    zGrid, yGrid = np.meshgrid( zcoord, ycoord )

    if periodic == 'true':
        zcoord = zcoord - zcoord[0]

    return yGrid, zGrid, ycoord, zcoord


def get_two_point_corr(filePath, arrName, timeDirs, 
                       delta, yGrid, zGrid,
                       periodic, rank, localN):

    if rank == 0:
        minT = int(0)
    else:
        minT = int( np.sum( localN[:rank] ) )

    maxT = int( minT + localN[rank] )
    skippedFiles = 0

    for i in range( minT, maxT ):
        fpath  = filePath + '/' + timeDirs[i] + '/' + arrName

        # interpolate velocity field:
        try:
            points = get_data( fpath + '/faceCentres', skiprows=3 )
            U     = get_data( fpath + '/vectorField/U', skiprows=3)
            UMean = get_data( fpath + '/vectorField/UMean', skiprows=3)
        except:
            skippedFiles += 1
            continue

        points /= delta
        UPrime = U - UMean

        upx = griddata( (points[:, 2], points[:, 1]), UPrime[:, 0],
                      (zGrid, yGrid), method='linear' )

        # check if Nan's are present:
        nanInd = np.isnan( upx )==True
        nNan   = upx[nanInd].size
        if nNan > 0:
            #print('\n   upx = \n', upx[:2, :], '\n', upx[-2:, :])

            raise ValueError('\n   Nan PRESENT ...')
            break

        upy = griddata( (points[:, 2], points[:, 1]), UPrime[:, 1],
                      (zGrid, yGrid), method='linear')

        upz = griddata( (points[:, 2], points[:, 1]), UPrime[:, 2],
                      (zGrid, yGrid), method='linear')

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
