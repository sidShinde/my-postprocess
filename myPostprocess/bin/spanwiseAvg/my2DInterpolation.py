import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline

__all__ = ['my2DInterpolation']

def my2DInterpolation(x1, x2, data, x1Grid, x2Grid):
    '''
    x1, x2: 2d coordinates of the scattered data
    data:   scalar data on the scattered mesh
    x1Grid, x2Grid: regular mesh for the x1, x2 coordinate
    '''

    [nx1, nx2] = x1Grid.shape
    oneD_x2_grid = x2Grid[:, 0]
    dataGrid = np.zeros((nx1, nx2))

    for i in range( nx1 ):
        x1Point = x1Grid[1, i]

        # get 1D data for x1 = x1Point
        oneD_x2, oneD_data = get1Ddata(x1, x2, data, x1Point)

        # fit a 1D spline through the scattered data
        spline = InterpolatedUnivariateSpline(oneD_x2, oneD_data)
        dataGrid[:, i] = spline( oneD_x2_grid )

    return dataGrid

def get1Ddata(x1, x2, data, x1Point):
    x2, data = list(), list()
    dataMat = np.vstack( (x1, x2) )
    dataMat = np.vstack( (dataMat, data) )
    dataMat = dataMat.T

    # get indicies where x1 = x1Point
    [idx2] = np.where( dataMat[:, 0] == x1Point )
    x2   = dataMat[idx2, 1]
    data = dataMat[idx2, 2]

    # sort x2
    # sort data according to x2
    sortIdx = np.argsort( x2 )
    x2   = x2[ sortIdx ]
    data = data[ sortIdx ]

    return x2, data
