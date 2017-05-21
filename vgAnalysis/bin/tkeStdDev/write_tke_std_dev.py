import numpy as np
import os
import argparse
from vgAnalysis.readers.reader_support_functions import *
from vgAnalysis.readers.reader import *
from .get_tke_std_dev import *

def main():
    parser = argparse.ArgumentParser(description='calculate the turbulent KE \
    per unit area in the separation region')
    
    parser.add_argument('-config',
                        type=str,
                        help='file with the essential inputs',
                        required=True)

    args = parser.parse_args()

    # parse the config:
    configFile = open(args.config, mode='r')

    coordPlane, tkeStdDev = get_tke_std_dev(configFile)
    solution = np.vstack((coordPlane, tkeStdDev))

    caseDir = os.getcwd()
    caseDir = caseDir + '/postProcessing/vgAnalysis'
    if not os.path.exists(caseDir):
        os.mkdir(caseDir)

    fname = caseDir + '/tke_std_dev.csv'
    np.savetxt(fname, solution.T, fmt='%.1f, %1.2e', 
               delimiter=', ', newline='\n', header='x/h, tke-std-dev')


if __name__=='__main__':
    main()
