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

    twoPointCorrX, twoPointCorrY, twoPointCorrZ, ycoord, zcoord = \
    get_two_point_corr(configFile)

    caseDir = os.getcwd()
    caseDir = caseDir + '/postProcessing/vgAnalysis/twoPointCoorData'
    if not os.path.exists(caseDir):
        os.makedirs(caseDir)

    planeNames = list( twoPointCorrX.keys() )

    for name in planeNames:
        fname = caseDir + '/two_point_coor_x_' + name + '.csv'
        np.savetxt(fname, twoPointCorrX[name], fmt='%1.4e', delimiter=', ',
                   newline='\n')

        fname = caseDir + '/two_point_coor_y_' + name + '.csv'
        np.savetxt(fname, twoPointCorrY[name], fmt='%1.4e', delimiter=', ',
                   newline='\n')

        fname = caseDir + '/two_point_coor_z_' + name + '.csv'
        np.savetxt(fname, twoPointCorrZ[name], fmt='%1.4e', delimiter=', ',
                   newline='\n')

        fname = caseDir + '/ycoord_' + name + '.csv'
        np.savetxt(fname, ycoord[name], fmt='%1.4e', delimiter=', ',
                   newline='\n')

        fname = caseDir + '/zcoord_' + name + '.csv'
        np.savetxt(fname, zcoord[name], fmt='%1.4e', delimiter=', ',
                   newline='\n')


if __name__ == '__main__':
    main()
