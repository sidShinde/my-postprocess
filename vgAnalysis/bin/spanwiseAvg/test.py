import numpy as np
import os
from tqdm import tqdm
from vgAnalysis.readers.reader_support_functions import *
from vgAnalysis.readers.reader import *

fname = os.getcwd()
fname = fname + '/vgAnalysis/bin/spanwiseAvg/spanAvgConfig'
f = open(fname, mode='r')

configDict = config_to_dict(f)

print(configDict['qty'])

a = 'qty2'
print(a.startswith('qty'))

qty = list( )
for key in configDict.keys():
    if key.startswith('qty'):
        qty.append(configDict[key])
    else:
        continue

print(qty)

a = 'fafbak' + \
    'cjadkc'
print(a)

a = np.ones(3)
b = (a, a)
b

a = np.append([a],[a], axis=0)
a
