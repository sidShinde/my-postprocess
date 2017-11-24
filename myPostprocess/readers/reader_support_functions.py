import numpy as np
import re
import os

__all__=['get_columns', 'get_indices_npts', 'get_time_dir', 'is_number',
         'get_number_of_cols', 'read_between_brackets']


def get_columns(dir1, dir2):
    '''return the column numbers of the POD directions'''

    if (dir1 == 'x' and dir2 == 'y') or (dir1 == 'y' and dir2 == 'x'):
        dataCols  = [0, 1]
        normalCol = 2
    elif (dir1 == 'y' and dir2 == 'z') or (dir1 == 'z' and dir2 == 'y'):
        dataCols  = [1, 2]
        normalCol = 0
    elif (dir1 == 'x' and dir2 == 'z') or (dir1 == 'z' and dir2 == 'x'):
        dataCols  = [0, 2]
        normalCol = 1
    else:
        raise ValueError('\n wrong set of dimensions')

    return dataCols, normalCol


def get_indices_npts(coords, minX, maxX):
    '''
    Input
    -----
        x1, x2: coordinates of the snapshot window
        x1min, x2min, x3max: lower bound of the POD window
        x1max, x2max, x3max: upper bound of the POD window

    Output
    ------
        indices: list of indices in the snapshot window
        npts: number of points in the snapshot window
    '''

    # number of dimensions in the field:
    dim = coords.shape[1]

    indices = []
    npts = coords[:, 0].shape[0]

    if dim == 2:
        for i in range(npts):
            if ( (minX['x1']<= coords[i, 0]) and (coords[i, 0] <= maxX['x1']) and
                 (minX['x2'] <= coords[i, 1]) and (coords[i, 1] <= maxX['x2']) ):
                indices.append(i)
            else: continue
    elif dim == 3:
        for i in range(npts):
            if ( (minX['x1']<= coords[i, 0]) and (coords[i, 0] <= maxX['x1']) and
                 (minX['x2'] <= coords[i, 1]) and (coords[i, 1] <= maxX['x2']) and
                 (minX['x3'] <= coords[i, 2]) and (coords[i, 2] <= maxX['x3']) ):
                indices.append(i)
            else: continue
    else: raise ValueError('\n wrong number input dimensions')

    indices = np.array(indices)
    nPts = indices.size

    return indices, nPts


def get_time_dir(caseDir, configFile):
    '''
    return the time directory to read data from
    '''
    timeStr = configFile['tDir']

    # if time string is latestTime:
    if timeStr == 'latestTime':
        allDirs = os.listdir(caseDir)
        numStr = []

        for folder in allDirs:
            if is_number(folder):
                numStr.append(folder)

        timeDirs = np.sort( np.array(numStr) )
        folder = str( timeDirs[-1] )
    # if time string is value
    else:
        folder = timeStr

    return folder


def is_number(s):
    '''
    returns True if string 's' is a number
    '''
    try:
        complex(s) # for int, long, float and complex
    except ValueError:
        return False

    return True


def get_number_of_cols(fname, skiprows=0):
    count = 0
    with open(fname) as f:
        for line in f:
            count += 1

            if count > skiprows:
                line = re.split(r'[(|)|\s]', line)
                while '' in line:
                    line.remove('')

                try:
                    temp = float( line[0] )
                    nCols = len(line)
                    break
                except:
                    continue

            else: continue

    return nCols


def read_between_brackets(configFile):
    strList = list()

    for line in configFile:
        if '}' in line:
            break
        else:
            line = line.strip()
            words = line.split(',')
            strList.append(words[0])

    return strList
