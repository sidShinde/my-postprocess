import numpy as np
import os
from vgAnalysis.readers.reader_support_functions import *
from vgAnalysis.readers.reader import *

__all__=['volume_of_separation_region']

def volume_of_separation_region(configFile):
    '''
    Input
    -----
        configFile: path of configuration file
    Output
    ------
        sepVolume: volume of separation region
    '''

    configDict = config_to_dict(configFile)

    # read data from configDict:
    # file path details:
    filePath  = os.getcwd()
    tDir      = get_time_dir(filePath, configDict)
    filePath  = filePath + '/' + tDir

    # non-dim parameters:
    h         = float( configDict["h"] )

    # region of interest:
    minX, maxX = dict(), dict()
    minX['x1'] = float( configDict["x1min"] )
    minX['x2'] = float( configDict["x2min"] )
    minX['x3'] = float( configDict["x3min"] )

    maxX['x1'] = float( configDict["x1max"] )
    maxX['x2'] = float( configDict["x2max"] )
    maxX['x3'] = float( configDict["x3max"] )

    print('\n reading data from files ...')

    try:
        print('  - ccx')
        coords  = get_internal_field(filePath + '/ccx', skiprows=22)

        print('  - ccy')
        coords  = np.hstack( ( coords, get_internal_field(filePath + '/ccy', skiprows=22) ) )

        print('  - ccz')
        coords  = np.hstack( ( coords, get_internal_field(filePath + '/ccz', skiprows=22) ) )

        print('  - V')
        cellVol = get_internal_field(filePath + '/V', skiprows=22)

        print('  - UMean')
        umean   = get_internal_field(filePath + '/UMean', skiprows=22)

    except FileNotFoundError:
        print('\n one of the following 2 things happened:')
        print(' 1. command not executed in an OpenFOAM case directory')
        print(' 2. OpenFOAM command \"writeCellCenters -latestTime\" not executed in this directory')

    indices, nPts = get_indices_npts(coords/h, minX, maxX)
    umean   = umean[indices, :]
    cellVol = cellVol[indices, :]

    print('\n calculating volume of the separation region ...')
    sepVolume = 0

    for i in range(nPts):
        # if x-component of velocity is negative:
        if umean[i, 0] < 0:
            sepVolume += cellVol[i, 0]
        else:
            continue

    # non-dimensionalze volume:
    sepVolume /= np.power(h, 3)

    return sepVolume
