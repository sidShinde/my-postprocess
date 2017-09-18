import numpy as np
import os
import argparse
from vgAnalysis.readers.reader_support_functions import *
from vgAnalysis.readers.reader import *
from .get_two_point_corr import *

from mpi4py import MPI
from mpi4py.MPI import ANY_SOURCE

# Begin MAIN()
def main():
    comm = MPI.COMM_WORLD  # initialize the communicator
    rank = comm.Get_rank() # get the rank of the process
    size = comm.Get_size() # get the number of processes

    parser = argparse.ArgumentParser(description='calculate spanwise two point \
    correlation at specific streamwise locations')

    parser.add_argument('-config',
                        type=str,
                        help='file with essential inputs',
                        required=True)

    args = parser.parse_args()

    # parse the config:
    configFile = open(args.config, mode='r')
    configDict = config_to_dict(configFile)

    caseDir = os.getcwd()
    filePath = caseDir + '/postProcessing/cuttingPlane'

    patchName = configDict['patchName']
    nPlanes   = int( configDict['nPlanes'] )
    delta     = float( configDict['delta'] )
    yw        = float( configDict['yw'] )
    nPts      = int( configDict['nPts'] )
    periodic  = configDict['periodic']

    configFile.close()

    # get list of time-dirs
    nTimeDirs = int( configDict['nTimeDirs'] )
    timeDirs  = np.sort( os.listdir(filePath) )
    try:
        timeDirs  = timeDirs[timeDirs.size - nTimeDirs:]
    except:
        ValueError('\n insufficient time directories for averaging ...')

    localN   = np.zeros(size)
    # get number of time dirs per processor
    if rank == 0:
        quo, rem = divmod( nTimeDirs, size )
        for i in range( size ):
            if ( i < rem ):
                localN[i] = quo + 1
            else:
                localN[i] = quo

    # boardcast localN to all the processes:
    comm.Bcast(localN, root=0)

    if rank == 0:
        caseDir = caseDir + '/postProcessing/my-postprocess/twoPointCorrData'
        if not os.path.exists(caseDir):
            os.makedirs(caseDir)

    Ruu, Rvv, Rww  = np.array([0]), np.array([0]), np.array([0])
    ycoord, zcoord = np.array([0]), np.array([0])

    for i in range( nPlanes ):
        if rank == 0:
            print('    working on plane ' + str(i+1) + ' ...')
        comm.Barrier()

        arrName = patchName + str(i+1)
        Ruu, Rvv, Rww, ycoord, zcoord = get_two_point_corr(filePath, arrName,
                                        timeDirs, delta, yw, nPts, periodic,
                                        rank, localN)

        comm.Barrier()
        if rank == 0:
            for i in range(size-1):
                Ruu[0]    += Ruu[i+1]
                Rvv[0]    += Rvv[i+1]
                Rww[0]    += Rww[i+1]

            Ruu    = Ruu[0] / size
            Rvv    = Rvv[0] / size
            Rww    = Rww[0] / size

            fname = caseDir + '/Ruu_' + arrName + '.csv'
            np.savetxt(fname, Ruu, fmt='%1.4e', delimiter=', ', newline='\n')

            fname = caseDir + '/Rvv_' + arrName + '.csv'
            np.savetxt(fname, Rvv, fmt='%1.4e', delimiter=', ', newline='\n')

            fname = caseDir + '/Rww_' + arrName + '.csv'
            np.savetxt(fname, Rww, fmt='%1.4e', delimiter=', ', newline='\n')

            fname = caseDir + '/ycoord_' + arrName + '.csv'
            np.savetxt(fname, ycoord, fmt='%1.4e', delimiter=', ', newline='\n')

            fname = caseDir + '/zcoord_' + arrName + '.csv'
            np.savetxt(fname, zcoord, fmt='%1.4e', delimiter=', ', newline='\n')


if __name__ == '__main__':
    main()
