import numpy as np
import os
from tqdm import tqdm
from scipy.interpolate import griddata
from .my2DInterpolation import *

__all__ = ['get_yplus', 'get_spanwise_avg']

def get_yplus(data, h, nu):
    # normalize lengths:
    data[:, :3] /= h

    ycoord = np.unique( data[:, 1] )
    zcoord = np.unique( data[:, 2] )
    zGrid, yGrid = np.meshgrid( zcoord, ycoord )

    tempUMean = my2DInterpolation( data[:, 2], data[:, 1], data[:, 3],
                zGrid, yGrid)
    umean = np.mean(tempUMean, axis=1)

    tempUMean = my2DInterpolation( data[:, 2], data[:, 1], data[:, 4],
                zGrid, yGrid)
    umean = np.append([umean], [np.mean( tempUMean, axis=1 )], axis=0)

    tempUMean = my2DInterpolation( data[:, 2], data[:, 1], data[:, 5],
                zGrid, yGrid)
    umean = np.append(umean, [np.mean( tempUMean, axis=1 )], axis=0)

    UMean = np.sqrt( np.sum( np.square(umean), axis=0 ) )
    du_dy = UMean[0]/ycoord[0]
    utau  = np.sqrt( nu*du_dy )

    yplus = ycoord*(h*utau/nu)

    return umean.T, ycoord, yplus, yGrid, zGrid


def get_spanwise_avg(data, yGrid, zGrid, h):

    # number of columns in the file
    nCols = data.shape[1]

    # scalar data:
    if nCols == 4:
        qty = my2DInterpolation( data[:, 2], data[:, 1], data[:, 3],
              zGrid, yGrid)
        avg = np.mean( qty, axis=1 )

    # vector data:
    elif nCols == 6:
        qtyX = my2DInterpolation( data[:, 2], data[:, 1], data[:, 3],
               zGrid, yGrid)
        avg = np.mean( qtyX, axis=1 )

        qtyY = my2DInterpolation( data[:, 2], data[:, 1], data[:, 4],
               zGrid, yGrid)
        avg = np.append([avg], [np.mean( qtyY, axis=1 )], axis=0)

        qty = my2DInterpolation( data[:, 2], data[:, 1], data[:, 5],
              zGrid, yGrid)
        avg = np.append(avg, [np.mean( qtyZ, axis=1 )], axis=0)

    # tensor data:
    elif nCols == 9:
        qtyXX = my2DInterpolation( data[:, 2], data[:, 1], data[:, 3],
                zGrid, yGrid)
        avg = np.mean( qtyXX, axis=1 )

        qtyXY = my2DInterpolation( data[:, 2], data[:, 1], data[:, 4],
                zGrid, yGrid)
        avg = np.append([avg], [np.mean( qtyXY, axis=1 )], axis=0)

        qtyXZ = my2DInterpolation( data[:, 2], data[:, 1], data[:, 5],
                zGrid, yGrid)
        avg = np.append(avg, [np.mean( qtyXZ, axis=1 )], axis=0)

        qtyYY = my2DInterpolation( data[:, 2], data[:, 1], data[:, 6],
                zGrid, yGrid)
        avg = np.append(avg, [np.mean( qtyYY, axis=1 )], axis=0)

        qtyYZ = my2DInterpolation( data[:, 2], data[:, 1], data[:, 7],
                zGrid, yGrid)
        avg = np.append(avg, [np.mean( qtyYZ, axis=1 )], axis=0)

        qtyZZ = my2DInterpolation( data[:, 2], data[:, 1], data[:, 8],
                zGrid, yGrid)
        avg = np.append(avg, [np.mean( qtyZZ, axis=1 )], axis=0)

    return avg.T
