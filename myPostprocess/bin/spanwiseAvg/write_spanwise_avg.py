import numpy as np
import os
import argparse
from tqdm import tqdm
from myPostprocess.readers.reader_support_functions import *
from myPostprocess.readers.reader import *
from .get_spanwise_avg import *

def main():
    parser = argparse.ArgumentParser(description='calculate spanwise \
    average at specific streamwise locations')

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
    filePath = filePath + '/postProcessing/surfaces'
    tDir     = get_time_dir(filePath, configDict)
    filePath = filePath + '/' + tDir

    # list of qauntities to average
    qty = list( )
    for key in configDict.keys():
        if key.startswith('qty'):
            qty.append(configDict[key])
        else:
            continue

    # check if UMean is present in the list:
    checkUMean = False
    if 'UMean' in qty:
        checkUMean = True

    # other parameters:
    h         = float( configDict['h'] )
    nu        = float( configDict['nu'] )
    patchName = configDict['patchName']
    nPlanes   = int( configDict['nPlanes'] )

    caseDir = os.getcwd()
    caseDir = caseDir + '/postProcessing/my-postprocess/spanwiseAvg/' + \
              str(tDir)
    if not os.path.exists(caseDir):
        os.makedirs(caseDir)

    ycoord, yplus, yGrid, zGrid = dict(), dict(), dict(), dict()
    print('\n calculating y+ ...')
    for i in tqdm(range(nPlanes), ncols=100 ):
        pName = patchName + str(i+1)
        fpath = filePath + '/UMean_' + pName + '.raw'
        try:
            umean = get_data(fpath, skiprows=2)
        except:
            raise IOError('UMean file not found ...')

        if checkUMean == True:
            UMean, ycoord[pName], yplus[pName], yGrid[pName], zGrid[pName] = \
            get_yplus(umean, h, nu)

            solution = np.append([ycoord[pName]], [yplus[pName]], axis=0)
            solution = np.append(solution, UMean.T, axis=0)
            solution = solution.T

            fname = caseDir + '/UMean_' + pName + '.csv'
            hLine = 'y/h, y+, UMean_avg_x, UMean_avg_y, UMean_avg_z'
            np.savetxt(fname, solution, fmt='%1.4e', delimiter=', ',
                       newline='\n', header=hLine)

        else:
            _, ycoord[pName], yplus[pName], yGrid[pName], zGrid[pName] = \
            get_yplus(umean, h, nu)

    if checkUMean == True:
        qty.remove('UMean')

    print('\n begin averaging ...')
    for i in range( len(qty) ):
        print('     averaging ' + qty[i] + ' ...')

        for j in tqdm( range(nPlanes), ncols=100 ):
            pName = patchName + str(j+1)
            fpath = filePath + '/' + qty[i] + '_' + pName + '.raw'

            data = get_data(fpath, skiprows=2)
            data[:, :3] /= h
            avg  = get_spanwise_avg(data, yGrid[pName], zGrid[pName], h)

            solution = ycoord[pName]
            solution = np.append([solution], [ yplus[pName] ], axis=0)

            fname = caseDir + '/' + qty[i] + '_' + patchName + \
                    str(j+1) + '.csv'
            if avg.ndim == 1:
                solution = np.append(solution, [avg], axis=0)
                hLine = 'y/h, y+, ' + qty[i] + '_avg'

            elif avg.ndim == 2 and avg.shape[1] == 3:
                solution = np.append(solution, avg.T, axis=0)
                hLine = 'y/h, y+, ' + qty[i] + '_avg_x, ' + \
                        qty[i] + '_avg_y, ' + qty[i] + '_avg_z'

            elif avg.ndim == 2 and avg.shape[1] == 6:
                solution = np.append(solution, avg.T, axis=0)
                hLine = 'y/h, y+, ' + qty[i] + '_avg_xx, ' + \
                        qty[i] + '_avg_xy, ' + qty[i] + '_avg_xz, ' + \
                        qty[i] + '_avg_yy, ' + qty[i] + '_avg_yz, ' + \
                        qty[i] + '_avg_zz'
            else:
                raise ValueError('Oops! Something went wrong in averaging ...')

            solution = solution.T
            np.savetxt(fname, solution, fmt='%1.4e', delimiter=', ',
                       newline='\n', header=hLine)

if __name__=='__main__':
    main()
