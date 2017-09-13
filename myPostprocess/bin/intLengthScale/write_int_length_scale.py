import numpy as np
import os
import argparse
from tqdm import tqdm
from vgAnalysis.readers.reader_support_functions import *
from vgAnalysis.readers.reader import *
from .get_int_length_scale import *

def main():
    parser = argparse.ArgumentParser(description='calculate the integral \
    length at specific streamwise locations given the two point correlation')

    parser.add_argument('-config',
                        type=str,
                        help='file with essential inputs',
                        required=True)

    args = parser.parse_args()

    # parse the config:
    configFile = open(args.config, mode='r')
    configDict = config_to_dict(configFile)

    # read data from configFile
    filePath = os.getcwd()
    filePath = filePath + '/postProcessing/vgAnalysis' \
               '/twoPointCorrData'

    patchName = configDict['patchName']
    nPlanes   = int( configDict['nPlanes'] )
    tValue    = float( configDict['tValue'] )

    caseDir = os.getcwd()
    caseDir = caseDir + '/postProcessing/my-postprocess/intLengthScale'
    if not os.path.exists(caseDir):
        os.makedirs(caseDir)

    for i in range( nPlanes ):
        print('     working on plane ' + str(i+1) + '...')

        fname = filePath + '/ycoord_' + patchName + str(i+1) + '.csv'
        iLArr = np.loadtxt(fname)

        fname = filePath + '/zcoord_' + patchName + str(i+1) + '.csv'
        zcoord = np.loadtxt(fname)

        fname = filePath + '/Ruu' + \
                    '_' + patchName + str(i+1) + '.csv'
        data  = np.loadtxt(fname, delimiter=', ')
        tempVect = get_int_length_scale(data, zcoord, tValue)
        iLArr = np.append([iLArr], [tempVect], axis=0)

        fname = filePath + '/Rvv' + \
                    '_' + patchName + str(i+1) + '.csv'
        data  = np.loadtxt(fname, delimiter=', ')
        tempVect = get_int_length_scale(data, zcoord, tValue)
        iLArr = np.append(iLArr, [tempVect], axis=0)

        fname = filePath + '/Rww' + \
                    '_' + patchName + str(i+1) + '.csv'
        data  = np.loadtxt(fname, delimiter=', ')
        tempVect = get_int_length_scale(data, zcoord, tValue)
        iLArr = np.append(iLArr, [tempVect], axis=0)

        iLArr = iLArr.T
        fname = caseDir + '/' + patchName + str(i+1) + '.csv'
        hLine = 'y/h, iL_x, iLy, iLz'
        np.savetxt(fname, iLArr, fmt='%1.4e', delimiter=', ',
                   newline='\n', header=hLine)

if __name__ == '__main__':
    main()
