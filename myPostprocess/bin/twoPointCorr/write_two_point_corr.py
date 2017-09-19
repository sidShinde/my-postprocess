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

    for i in range( nPlanes ):
        arrName = patchName + str(i+1)

        points, yGrid, zGrid, ycoord, zcoord = get_grid(filePath, arrName,
                                               timeDirs, delta, yw, nPts, periodic)

        comm.Barrier()

        recvbufRuu = None
        recvbufRvv = None
        recvbufRww = None
        recvbufY   = None
        recvbufZ   = None

        if rank == 0:
            print('\n   working on plane ' + str(i+1) + ' ...')
            [ny, nz]   = yGrid.shape
            recvbufRuu = np.empty([ny, nz], dtype='float64')
            recvbufRvv = np.empty([ny, nz], dtype='float64')
            recvbufRww = np.empty([ny, nz], dtype='float64')
            recvbufY   = np.empty([ny], dtype='float64')
            recvbufZ   = np.empty([nz], dtype='float64')

        Ruu, Rvv, Rww = get_two_point_corr(filePath, arrName,
                        timeDirs, points, yGrid, zGrid, periodic,
                        rank, localN)

        comm.Barrier()
        comm.Reduce(Ruu, recvbufRuu, op=MPI.SUM, root=0)
        comm.Reduce(Rvv, recvbufRvv, op=MPI.SUM, root=0)
        comm.Reduce(Rww, recvbufRww, op=MPI.SUM, root=0)
        comm.Reduce(ycoord, recvbufY, op=MPI.SUM, root=0)
        comm.Reduce(zcoord, recvbufZ, op=MPI.SUM, root=0)

        if rank == 0:

            fname = caseDir + '/Ruu_' + arrName + '.csv'
            np.savetxt(fname, recvbufRuu / size, fmt='%1.4e', delimiter=', ',
            newline='\n')

            fname = caseDir + '/Rvv_' + arrName + '.csv'
            np.savetxt(fname, recvbufRvv / size, fmt='%1.4e', delimiter=', ',
            newline='\n')

            fname = caseDir + '/Rww_' + arrName + '.csv'
            np.savetxt(fname, recvbufRww / size, fmt='%1.4e', delimiter=', ',
            newline='\n')

            fname = caseDir + '/ycoord_' + arrName + '.csv'
            np.savetxt(fname, recvbufY / size, fmt='%1.4e', delimiter=', ',
            newline='\n')

            fname = caseDir + '/zcoord_' + arrName + '.csv'
            np.savetxt(fname, recvbufZ / size, fmt='%1.4e', delimiter=', ',
            newline='\n')

    if rank == 0:
        print('\n   Finished calculation ...')

if __name__ == '__main__':
    main()
