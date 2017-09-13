import numpy as np

__all__ = ['get_int_length_scale']

def get_int_length_scale(data, zcoord, tValue):
    ny, nz = data.shape
    iLVect = np.zeros(ny)

    for i in range(ny):
        for j in range(nz):
            if data[i, j] >= tValue and data[i, j+1] <= tValue:
                iLVect[i] = zcoord[j] - \
                            ((tValue - data[i, j])*(zcoord[j] - zcoord[j+1]))/(data[i, j] - data[i, j+1])
                break
            else:
                continue

    return iLVect
