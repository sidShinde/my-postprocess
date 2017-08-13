import numpy as np
import os
import argparse
from vgAnalysis.readers.reader_support_functions import *
from vgAnalysis.readers.reader import *
from .get_spanwise_avg import *

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
    configDict = config_to_dict(configFile)

    # read data from configFile
    filePath = os.getcwd()
    filePath = filePath + 'postProcessing/surfaces'
    tDir     = get_time_dir(filePath, configDict)
    filePath = filePath + '/' + tDir

    # list of qauntities to average
    qty = list( )
    for key in configDict.keys():
        if key.startswith('qty'):
            qty.append(configDict[key])
        else:
            continue

    # other parameters:
    h         = float( configDict['h'] )
    patchName = configDict['patchName']
    nPlanes   = int( configDict['nPlanes'] )

    caseDir = os.getcwd()
    caseDir = caseDir + '/postProcessing/vgAnalysis/spanwiseAvg'
    if not os.path.exists(caseDir):
        os.mkdirs(caseDir)

    print('\n begin averaging ...')
    for i in range( len(qty) ):
        print('     averaging ' + qty[i] + ' ...')

        for j in tqdm( range(nPlanes), ncols=100 ):
            fpath = filePath + '/' + qty[i] + '_' + patchName + \
                    str(j+1) + '.raw'

            data = get_data(fpath, skiprows=2)
            avg  = get_spanwise_avg(data, h)

            fname = caseDir + '/' + qty[i] + '_' + patchName + \
                    str(j+1) + '.csv'
            if avg.shape[1] == 2:
                hLine = 'y/h, ' + qty[i] + '_avg'
            elif avg.shape[1] == 4:
                hLine = 'y/h, ' + qty[i] + '_avg_x, ' + \
                        qty[i] + '_avg_y, ' + qty[i] + '_avg_z'
            elif avg.shape[1] == 7:
                hLine = 'y/h, ' + qty[i] + '_avg_xx, ' + \
                        qty[i] + '_avg_xy, ' + qty[i] + '_avg_xz, ' + \
                        qty[i] + '_avg_yy, ' + qty[i] + '_avg_yz, ' + \
                        qty[i] + '_avg_zz'
            else:
                raise ValueError('Oops! Something went wrong in averaging ...')

            np.savetxt(fname, avg, fmt='%.3f', delimiter=', ',
                       newline='\n', header=hLine)

if __name__=='__main__':
    main()
