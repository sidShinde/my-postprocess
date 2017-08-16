import numpy as np
import os
from tqdm import tqdm
from scipy.interpolate import griddata
from vgAnalysis.readers.reader_support_functions import *
from vgAnalysis.readers.reader import *

__all__ = ['get_int_length_scale']

def get_int_length_scale(data, zcoord, tValue):
    ny, nz = data.shape
    iLArr = np.zeros(ny)

    for i in range(ny):
        for j in range(nz):
            if data[i, j] <= tValue:
                iLArr[i] = zcoord[j]
                break
            else:
                continue

    return iLArr
