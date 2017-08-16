import numpy as np

__all__ = ['get_int_length_scale']

def get_int_length_scale(data, zcoord, tValue):
    ny, nz = data.shape
    iLVect = np.zeros(ny)

    for i in range(ny):
        for j in range(nz):
            if data[i, j] <= tValue:
                iLVect[i] = zcoord[j]
                break
            else:
                continue

    return iLVect
