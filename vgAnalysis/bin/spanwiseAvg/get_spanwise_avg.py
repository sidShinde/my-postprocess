import numpy as np
import os
from tqdm import tqdm
from scipy.interpolate import griddata
from vgAnalysis.readers.reader_support_functions import *
from vgAnalysis.readers.reader import *

__all__ = ['get_spanwise_avg']

def get_spanwise_avg(data, h):
    data   = get_data(fpath, skiprows=2)

    ycoord = np.unique( data[:, 1] ) / h
    avg = ycoord
    zcoord = np.unique( data[:, 2] ) / h
    zGrid, yGrid = np.meshgrid( zcoord, ycoord )

    # number of columns in the file
    nCols = data.shape[1]

    # scalar data:
    if nCols == 4:
        qtyX = griddata( (data[:, 2], data[:, 1]), data[:, 3],
                       (zGrid, yGrid), method='linear')
        avg = np.append([avg], [np.mean( qtyX, axis=1 )], axis=0)
    # vector data:
    elif nCols == 6:
        qtyX = griddata( (data[:, 2], data[:, 1]), data[:, 3],
                       (zGrid, yGrid), method='linear')
        avg = np.append([avg], [np.mean( qtyX, axis=1 )], axis=0)
        qtyY = griddata( (data[:, 2], data[:, 1]), data[:, 4],
                       (zGrid, yGrid), method='linear')
        avg = np.append([avg], [np.mean( qtyY, axis=1 )], axis=0)
        qtyZ = griddata( (data[:, 2], data[:, 1]), data[:, 5],
                       (zGrid, yGrid), method='linear')
        avg = np.append([avg], [np.mean( qtyZ, axis=1 )], axis=0)
    elif nCols == 9:
        qtyXX = griddata( (data[:, 2], data[:, 1]), data[:, 3],
                       (zGrid, yGrid), method='linear')
        avg = np.append([avg], [np.mean( qtyX, axis=1 )], axis=0)
        qtyXY = griddata( (data[:, 2], data[:, 1]), data[:, 4],
                       (zGrid, yGrid), method='linear')
        avg = np.append([avg], [np.mean( qtyY, axis=1 )], axis=0)
        qtyXZ = griddata( (data[:, 2], data[:, 1]), data[:, 5],
                       (zGrid, yGrid), method='linear')
        avg = np.append([avg], [np.mean( qtyZ, axis=1 )], axis=0)
        qtyYY = griddata( (data[:, 2], data[:, 1]), data[:, 6],
                       (zGrid, yGrid), method='linear')
        avg = np.append([avg], [np.mean( qtyZ, axis=1 )], axis=0)
        qtyYZ = griddata( (data[:, 2], data[:, 1]), data[:, 7],
                       (zGrid, yGrid), method='linear')
        avg = np.append([avg], [np.mean( qtyZ, axis=1 )], axis=0)
        qtyZZ = griddata( (data[:, 2], data[:, 1]), data[:, 8],
                       (zGrid, yGrid), method='linear')
        avg = np.append([avg], [np.mean( qtyZ, axis=1 )], axis=0)


    return avg.T
