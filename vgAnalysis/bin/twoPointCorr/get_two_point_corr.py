import numpy as np
import os
from tqdm import tqdm
from scipy.interpolate import griddata
from vgAnalysis.readers.reader_support_functions import *
from vgAnalysis.readers.reader import *

__all__ = ['get_two_point_corr']

def get_two_point_corr(configFile):
    configDict = config_to_dict(configFile)

    # read data from configFile
    filePath = os.getcwd()
    filePath = filePath + '/postProcessing/cuttingPlane'

    patchName = configDict['patchName']
    nPlanes   = int( configDict['nPlanes'] )
    delta     = float( configDict['delta'] )
    yw        = float( configDict['yw'] )
    nPts      = int( configDict['nPts'] )

    # get list of time-dirs
    nTimeDirs = int( configDict['nTimeDirs'] )
    timeDirs  = np.sort( os.listdir(filePath) )
    try:
        timeDirs  = timeDirs[timeDirs.size - nTimeDirs:]
    except:
        ValueError('\n insufficient time directories for averaging ...')

    # dict to store two point correlation data
    twoPointCorrX, twoPointCorrY, twoPointCorrZ = dict(), dict(), dict()
    ycoord, zcoord = dict(), dict()

    for i in range( nPlanes ):
        print('     working on plane ' + str(i+1) + ' ...')

        arrName = patchName + str(i+1)
        twoPointCorrX[arrName], twoPointCorrY[arrName], twoPointCorrZ[arrName], \
        ycoord[arrName], zcoord[arrName] = \
        two_point_corr_matrix(filePath, arrName, timeDirs, delta, yw, nPts)

    return twoPointCorrX, twoPointCorrY, twoPointCorrZ, ycoord, zcoord


def two_point_corr_matrix(filePath, arrName, timeDirs, delta, yw, nPts):

    for i in tqdm( range( len(timeDirs) ), ncols=100 ):
        fpath  = filePath + '/' + timeDirs[i] + '/' + arrName

        points = get_data( fpath + '/faceCentres', skiprows=3 )
        U      = get_data( fpath + '/vectorField/U', skiprows=3)
        UMean  = get_data( fpath + '/vectorField/UMean', skiprows=3)
        UPrime = U - UMean

        # interpolate data:
        points[:, :3] /= delta
        zcoord = np.unique( points[:, 2] )
        zcoord[0] = (zcoord[0] + zcoord[1])/2
        zcoord[-1] = (zcoord[-1] + zcoord[-2])/2

        ymin   = np.min( points[:, 1] )
        ycoord = np.linspace( ymin, yw, nPts )
        ycoord[0] = (ycoord[0] + ycoord[1])/2
        ycoord[-1] = (ycoord[-1] + ycoord[-2])/2

        zGrid, yGrid = np.meshgrid( zcoord, ycoord )

        upx = griddata( (points[:, 2], points[:, 1]), UPrime[:, 0],
                      (zGrid, yGrid), method='linear' )
        upy = griddata( (points[:, 2], points[:, 1]), UPrime[:, 1],
                      (zGrid, yGrid), method='linear')
        upz = griddata( (points[:, 2], points[:, 1]), UPrime[:, 2],
                      (zGrid, yGrid), method='linear')

        # number of points in y and z:
        [ny, nz] = upx.shape

        if i == 0:
            tpcX = np.zeros([ny, nz-1])
            tpcY = np.zeros([ny, nz-1])
            tpcZ = np.zeros([ny, nz-1])

            tpcX = two_point_corr_eval(upx, ny, nz)
            tpcY = two_point_corr_eval(upy, ny, nz)
            tpcZ = two_point_corr_eval(upz, ny, nz)

        else:
            tpcX += two_point_corr_eval(upx, ny, nz)
            tpcY += two_point_corr_eval(upy, ny, nz)
            tpcZ += two_point_corr_eval(upz, ny, nz)

    tpcX = tpcX/(i+1)
    tpcY = tpcY/(i+1)
    tpcZ = tpcZ/(i+1)

    return tpcX, tpcY, tpcZ, ycoord, zcoord


def two_point_corr_eval(up, ny, nz):
    tpc     = np.zeros([ny, nz-1])
    counter = np.zeros(nz-1)

    for i in range(ny):
        for j in range(nz):
            # points on the left:
            for lpts in range(0, j):
                val = up[i, j] * up[i, lpts]
                val /= np.square( up[i, j] )
                tpc[i, abs(lpts-j)-1] += val
                counter[ abs(lpts-j)-1 ] += 1

            # points on the right:
            for rpts in range(j+1, nz):
                val = up[i, j] * up[i, rpts]
                val /= np.square( up[i, j] )
                tpc[i, abs(j-rpts)-1] += val
                counter[ abs(j-rpts)-1 ] += 1

            # normalization:
            tpc[i, :] /= counter

    return tpc
