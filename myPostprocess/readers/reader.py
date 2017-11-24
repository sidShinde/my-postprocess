import numpy as np
import re
from .reader_support_functions import *

__all__=['get_internal_field', 'get_data', 'config_to_dict']


def get_internal_field(fname, skiprows=0):
    nCols = get_number_of_cols(fname, skiprows)
    data = [[] for i in range(nCols)]

    count = 0                   # line counter
    pointsInternalField = 0     # number of points in the internal field

    with open(fname) as f:
        for line in f:
            count += 1

            if count == (skiprows-1):
                line = re.split(r'[\s]', line)

                # remove whitespaces from the line
                while '' in line:
                    line.remove('')

                pointsInternalField = int( line[0] )

            elif (count > skiprows) and (count <= pointsInternalField + skiprows):
                line = re.split(r'[(|)|\s]', line)

                # remove whitespaces from the line
                while '' in line:
                    line.remove('')

                try:
                    for i in range( nCols ):
                        data[i].append( float( line[i] ) )

                except:
                    continue

            elif count > pointsInternalField + skiprows:
                break

            # skip rows
            else: continue

    return np.array(data).T


def get_data(fname, skiprows=0):
    nCols = get_number_of_cols(fname, skiprows)
    data = [[] for i in range(nCols)]

    count = 0

    with open(fname) as f:
        for line in f:
            count += 1

            if count > skiprows:
                line = re.split(r'[(|)|\s]', line)

                # remove whitespaces from the line
                while '' in line:
                    line.remove('')

                try:
                    for i in range( nCols ):
                        data[i].append( float( line[i] ) )

                except:
                    continue

            # skip rows
            else: continue

    return np.array(data).T


def config_to_dict(configFile):
    '''
    Parse a config file to dictionary
    '''
    configDict = {}

    for line in configFile:

        if (line[0] == '#') or (line == '\n'):
            continue
        else:
            if '{' in line:
                configDict[line.split('{')[0]] = \
                           read_between_brackets(configFile)
            else:
                configDict[line.split()[0]] = line.split()[1]
    
    return configDict

                
