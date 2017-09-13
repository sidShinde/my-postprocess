import numpy as np
import os
import argparse
from vgAnalysis.readers.reader_support_functions import *
from vgAnalysis.readers.reader import *
from .get_two_point_corr import *

def main():
    parser = argparse.ArgumentParser(description='calculate spanwise two point \
    correlation at specific streamwise locations')

    parser.add_argument('-config',
                        type=str,
                        help='file with essential inputs',
                        required=True)

    args = parser.parse_args()

    # parse the config:
    configFile = open(args.config, mode='r')

    caseDir = os.getcwd()
    filePath = caseDir + '/postProcessing/cuttingPlane'

    patchName = configDict['patchName']
    nPlanes   = int( configDict['nPlanes'] )
    delta     = float( configDict['delta'] )
    yw        = float( configDict['yw'] )
    nPts      = int( configDict['nPts'] )
    periodic  = configDict['periodic']

    configFile.close()

    # get list of time-dirs
    nTimeDirs = int( configDict['nTimeDirs'] )
    timeDirs  = np.sort( os.listdir(filePath) )
    try:
        timeDirs  = timeDirs[timeDirs.size - nTimeDirs:]
    except:
        ValueError('\n insufficient time directories for averaging ...')

    caseDir = caseDir + '/postProcessing/my-postprocess/twoPointCorrData'
    if not os.path.exists(caseDir):
        os.makedirs(caseDir)

    for i in range( nPlanes ):
        print('     working on plane ' + str(i+1) + ' ...')

        arrName = patchName + str(i+1)

        Ruu, Rvv, Rzz, ycoord, zcoord = two_point_corr_matrix(filePath, arrName,
                                        timeDirs, delta, yw, nPts, periodic)

        fname = caseDir + '/Ruu_' + arrName + '.csv'
        np.savetxt(fname, Ruu, fmt='%1.4e', delimiter=', ', newline='\n')

        fname = caseDir + '/Rvv_' + arrName + '.csv'
        np.savetxt(fname, Rvv, fmt='%1.4e', delimiter=', ', newline='\n')

        fname = caseDir + '/Rww_' + arrName + '.csv'
        np.savetxt(fname, Rww, fmt='%1.4e', delimiter=', ', newline='\n')

        fname = caseDir + '/ycoord_' + name + '.csv'
        np.savetxt(fname, ycoord, fmt='%1.4e', delimiter=', ', newline='\n')

        fname = caseDir + '/zcoord_' + name + '.csv'
        np.savetxt(fname, zcoord, fmt='%1.4e', delimiter=', ', newline='\n')


if __name__ == '__main__':
    main()
