import numpy as np
import os
from tqdm import tqdm
from myPostprocess.readers.reader_support_functions import *
from myPostprocess.readers.reader import *

__all__=['get_tke_std_dev']

def get_tke_std_dev(configFile):
    '''
    Input
    -----
        configFile: path of configuration file
    Output
    ------
        tkeStdDev: file containing y/h, z/h, tkeStdDev of
                   the plane
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
    
    # get the plane coordinate and the vorticity center:
    coordPlane = np.zeros(nPlanes)
    tkeStdDev  = np.zeros(nPlanes)

    print('\n calculating tke standard deviation ...')
    for i in tqdm( range(nPlanes), ncols=100 ):
        dataPath = filePath + '/UPrime2Mean_' + patchName + str(i+1) + '.raw'

        coordCols, normalCol = get_columns(dir1, dir2)
        data   = get_data(dataPath, skiprows=2)

        # coordinate data:
        coords        = data[:, coordCols]
        coords        = coords/h
        indices, nPts = get_indices_npts(coords, minX, maxX)
        #x1, x2        = coords[indices, 0], coords[indices, 1]
        coordPlane[i] = data[0, normalCol]/h

        # calculate area of the plane:
        #area = abs( x1.max() - x1.min() ) * abs( x2.max() - x2.min() )

        # tke data:
        tke = data[indices, 3] + data[indices, 6] + data[indices, 8]
        #tkePerArea[i] = np.sum( tke ) / (area * ubar**2)
        tkeStdDev[i] = np.std( tke )
        
    return coordPlane, tkeStdDev
    
    


    

