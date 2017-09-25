import numpy as np
import os
from tqdm import tqdm
from scipy.interpolate import griddata
from vgAnalysis.readers.reader_support_functions import *
from vgAnalysis.readers.reader import *

__all__ = ['get_yplus', 'get_spanwise_avg']

def get_yplus(data, h, nu):
    # normalize lengths:
    data[:, :3] /= h

    ycoord = np.unique( data[:, 1] )
    ycoord[0] = (ycoord[0] + ycoord[1])/2
    ycoord[-1] = (ycoord[-1] + ycoord[-2])/2

    zcoord = np.unique( data[:, 2] )
    zcoord[0] = (zcoord[0] + zcoord[1])/2
    zcoord[-1] = (zcoord[-1] + zcoord[-2])/2
    zGrid, yGrid = np.meshgrid( zcoord, ycoord )

    tempUMean = griddata( (data[:, 2], data[:, 1]), data[:, 3],
                   (zGrid, yGrid), method='cubic')
    umean = np.mean(tempUMean, axis=1)
    tempUMean = griddata( (data[:, 2], data[:, 1]), data[:, 4],
                   (zGrid, yGrid), method='cubic')
    umean = np.append([umean], [np.mean( tempUMean, axis=1 )], axis=0)
    tempUMean = griddata( (data[:, 2], data[:, 1]), data[:, 5],
                   (zGrid, yGrid), method='cubic')
    umean = np.append(umean, [np.mean( tempUMean, axis=1 )], axis=0)

    UMean = np.sqrt( np.sum( np.square(umean), axis=0 ) )
    du_dy = UMean[0]/ycoord[0]
    utau  = np.sqrt( nu*du_dy )

    yplus = ycoord*(utau/nu)

    return umean.T, ycoord, yplus, yGrid, zGrid


def get_spanwise_avg(data, yGrid, zGrid, h):

    # number of columns in the file
    nCols = data.shape[1]

    # scalar data:
    if nCols == 4:
        qty = griddata( (data[:, 2], data[:, 1]), data[:, 3],
                       (zGrid, yGrid), method='cubic')
        avg = np.mean( qty, axis=1 )

    # vector data:
    elif nCols == 6:
        qtyX = griddata( (data[:, 2], data[:, 1]), data[:, 3],
                       (zGrid, yGrid), method='cubic')
        avg = np.mean( qtyX, axis=1 )
        qtyY = griddata( (data[:, 2], data[:, 1]), data[:, 4],
                       (zGrid, yGrid), method='cubic')
        avg = np.append([avg], [np.mean( qtyY, axis=1 )], axis=0)
        qtyZ = griddata( (data[:, 2], data[:, 1]), data[:, 5],
                       (zGrid, yGrid), method='cubic')
        avg = np.append(avg, [np.mean( qtyZ, axis=1 )], axis=0)

    # tensor data:
    elif nCols == 9:
        qtyXX = griddata( (data[:, 2], data[:, 1]), data[:, 3],
                       (zGrid, yGrid), method='cubic')
        avg = np.mean( qtyXX, axis=1 )
        qtyXY = griddata( (data[:, 2], data[:, 1]), data[:, 4],
                       (zGrid, yGrid), method='cubic')
        avg = np.append([avg], [np.mean( qtyXY, axis=1 )], axis=0)
        qtyXZ = griddata( (data[:, 2], data[:, 1]), data[:, 5],
                       (zGrid, yGrid), method='cubic')
        avg = np.append(avg, [np.mean( qtyXZ, axis=1 )], axis=0)
        qtyYY = griddata( (data[:, 2], data[:, 1]), data[:, 6],
                       (zGrid, yGrid), method='cubic')
        avg = np.append(avg, [np.mean( qtyYY, axis=1 )], axis=0)
        qtyYZ = griddata( (data[:, 2], data[:, 1]), data[:, 7],
                       (zGrid, yGrid), method='cubic')
        avg = np.append(avg, [np.mean( qtyYZ, axis=1 )], axis=0)
        qtyZZ = griddata( (data[:, 2], data[:, 1]), data[:, 8],
                       (zGrid, yGrid), method='cubic')
        avg = np.append(avg, [np.mean( qtyZZ, axis=1 )], axis=0)


    return avg.T
