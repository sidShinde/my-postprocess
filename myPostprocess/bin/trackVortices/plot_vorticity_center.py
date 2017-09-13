import os
import numpy as np
import argparse
import matplotlib
matplotlib.use('PDF')
from matplotlib import pyplot as plt


def main():
    '''
    plot 1: vortex centers on different planes
    '''
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(
            description="Write POD modes and singular values in the postProcessing/POD. \
                         Modes are arranged in decreasing singular value order.",
            prefix_chars='-')

    # case directory:
    caseDir = os.getcwd()
    caseDir = caseDir + '/postProcessing/vgAnalysis' 
    fname = caseDir + '/vorticity_center.csv'

    if not os.path.exists(fname):
        raise ValueError('\n run [writeVorticityCenter] before using this utility ...')
    else:
        solution = np.genfromtxt(fname, delimiter=', ', 
                                 skip_header=1)
        coordPlane = solution[:, 0]
        vorCenter  = solution[:, 1:3]
        
        # plot figure 1:
        fig1 = plt.figure(1, figsize=(6,6))
        ax = fig1.add_subplot(111)

        plt.rc('text', usetex=True)
        plt.scatter(vorCenter[:, 1], vorCenter[:, 0], s=30, c='k')
        plt.rc('font', family='serif')
        for i in range(np.size(coordPlane)):
            txt = str( round(coordPlane[i], 1) - 1 ) + 'h'
            ax.annotate(txt, (vorCenter[i, 1], vorCenter[i, 0]), fontsize=12)

        ax.tick_params(axis='both', which='major', labelsize=12)
        plt.xlabel(r'$\rm{z/h}$', fontsize=14, family='serif')
        plt.ylabel(r'$\rm{y/h}$', fontsize=14, family='serif')
        plt.savefig(caseDir + '/vorticityCenter.pdf')


if __name__== "__main__":
    main()
