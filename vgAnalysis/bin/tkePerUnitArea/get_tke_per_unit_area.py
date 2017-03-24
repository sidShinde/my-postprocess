import numpy as np
import os
from update_progress import *
from vgAnalysis.readers.reader_support_functions import *
from vgAnalysis.readers.reader import *

__all__=['get_tke_per_unit_area']

def get_tke_per_unit_area(configFile):
    '''
    Input
    -----
        configFile: path of configuration file
    Output
    ------
        coordPlane: coordinate of the plane
        vorCenter: coordinates of the vorticity center
    '''

    configDict = config_to_dict(configFile)

    # read data from configDict:
    # file path details:
    filePath  = os.getcwd()
    filePath  = filePath + '/postProcessing/surfaces'
    tDir      = get_time_dir(filePath, configDict)
    filePath  = filePath + '/' + tDir 

    # non-dim parameters:
    h         = float( configDict["h"] ) 
    ubar      = float( configDict["ubar"] )

    # patch and AOI details:
    patchName = configDict["patchName"]
    nPlanes   = int( configDict["nPlanes"] )
    dir1      = configDict["direction1"]     
    dir2      = configDict["direction2"]     

    minX, maxX = dict(), dict()
    minX['x1'] = float( configDict["x1min"] ) 
    minX['x2'] = float( configDict["x2min"] ) 
    maxX['x1'] = float( configDict["x1max"] ) 
    maxX['x2'] = float( configDict["x2max"] )    

    # area of the plane:
    area = abs( maxX['x1'] - minX['x1'] ) * \
           abs( maxX['x2'] - minX['x2'] )
    
    # get the plane coordinate and the vorticity center:
    coordPlane = np.zeros(nPlanes)
    tkePerArea = np.zeros(nPlanes)

    print('\n calculating tke per unit area ...')
    for i in range(nPlanes):
        dataPath = filePath + '/UPrime2Mean_' + patchName + str(i+1) + '.raw'

        coordCols, normalCol = get_columns(dir1, dir2)
        data   = get_data(dataPath, skiprows=2)

        # coordinate data:
        coords        = data[:, coordCols]
        coords        = coords/h
        indices, nPts = get_indices_npts(coords, minX, maxX)
        x1, x2        = coords[indices, 0], coords[indices, 1]
        coordPlane[i] = data[0, normalCol]/h

        # tke data:
        tke = data[indices, 3] + data[indices, 6] + data[indices, 8]
        tkePerArea[i] = np.sum( tke ) / (area * ubar**2)

        update_progress((i+1)/nPlanes)
    
    return coordPlane, tkePerArea
    
    


    
