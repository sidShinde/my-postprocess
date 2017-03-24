import numpy as np
import re
from .reader_support_functions import *

__all__=['get_data', 'config_to_dict']


def get_data(fname, skiprows=0):
    nCols = get_number_of_cols(fname, skiprows)
    data = [[] for i in range(nCols)]

    count = 0
    with open(fname) as f:
        for line in f:
            count += 1
            
            if count > skiprows:
                line = re.split(r'[(|)|\s]', line)
                while '' in line:    # remove whitespaces from the line
                    line.remove('')
                    
                try:
                    for i in range( nCols ):
                        data[i].append( float( line[i] ) )

                except:
                    continue

            else: continue    # skip rows
                
    return np.array(data).T


def config_to_dict(configFile):
    '''
    Parse a config file to dictionary
    '''

    configDict = {}
    points = []

    for line in configFile:
        if (line[0] == '#') or (line == '\n'):
            continue

        else:
            configDict[line.split()[0]] = line.split()[1]

    return configDict
