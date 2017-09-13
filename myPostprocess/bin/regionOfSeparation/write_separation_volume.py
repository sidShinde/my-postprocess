import numpy as np
import os
import argparse
from vgAnalysis.readers.reader_support_functions import *
from vgAnalysis.readers.reader import *
from .volume_of_separation_region import *

def main():
    parser = argparse.ArgumentParser(description='calculate the total volume \
    of the separation region')

    parser.add_argument('-config',
                        type=str,
                        help='file with the essential inputs',
                        required=True)

    args = parser.parse_args()

    # parse the config:
    configFile = open(args.config, mode='r')

    sepVolume = volume_of_separation_region(configFile)
    sepVolume = '%1.3e' % sepVolume
    writeLine = 'separation volume / h^3 = ' + sepVolume

    caseDir = os.getcwd()
    caseDir = caseDir + '/postProcessing/my-postprocess'
    if not os.path.exists(caseDir):
        os.mkdir(caseDir)

    fname = caseDir + '/volume_of_separation_region.txt'
    writeAns = open(fname, 'w')
    writeAns.write(writeLine)
    writeAns.close()


if __name__=='__main__':
    main()
