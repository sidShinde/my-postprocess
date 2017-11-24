import numpy as np
import os
from tqdm import tqdm
from myPostprocess.readers.reader_support_functions import *
from myPostprocess.readers.reader import *

__all__=["track_vorticity_center", "vorticity_tracker"]

def track_vorticity_center(configFile):
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
    nonDimT   = h/ubar

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
    coordPlane    = np.zeros(nPlanes)
    vorCenter     = np.zeros((nPlanes, 2))
    vorCenterDist = np.zeros(nPlanes)

    print('\n calculating vorticity centers ...')
    for i in tqdm( range(nPlanes), ncols=100 ):
        dataPath = filePath + '/vorticityMean_' + patchName + str(i+1) + '.raw'

        coordCols, normalCol = get_columns(dir1, dir2)
        data   = get_data(dataPath, skiprows=2)

        # coordinate data:
        coords        = data[:, coordCols]
        coords        = coords/h
        indices, nPts = get_indices_npts(coords, minX, maxX)
        x1, x2        = coords[indices, 0], coords[indices, 1]
        coordPlane[i] = data[0, normalCol]/h

        # vorticity data:
        vor = data[indices, normalCol+3]
        vor = vor * nonDimT

        # get the center of the vortex:
        vorCenter[i, :] = vorticity_tracker(x1, x2, vor)

        # calculate the distance of the center from the center of 1st plane:
        if i == 0:
            vorCenterDist[i] = 0
        else:
            vorCenterDist[i] = np.linalg.norm(vorCenter[i, :] - vorCenter[0, :])
    
    return coordPlane, vorCenter, vorCenterDist


def vorticity_tracker(x1, x2, vor):
    '''
    Input
    -----
        x1, x2: coordinates of the points in the AOI
        vor: vorticity magnitude of the normal component
    Output
    ------
        vorCenter: center of the vortex
    '''

    # replace negative values with zero:
    vor[vor < 0] = 0

    # coords of the centroid:
    vorCenter = np.zeros(2)
    vorCenter[0] = np.dot(vor, x1)/np.sum(vor)
    vorCenter[1] = np.dot(vor, x2)/np.sum(vor)

    return vorCenter
    










