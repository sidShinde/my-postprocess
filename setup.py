from setuptools import setup
from setuptools import find_packages

setup(name='myPostprocess',
      description='Package to perform post-porcessing of data from OpenFOAM simulations',
      version='1.0.0',
      author='Siddhesh Shinde',
      packages=find_packages(),
      entry_points = {
          'console_scripts':[
              'writeVorticityCenter=myPostProcess.bin.trackVortices.write_vorticity_center:main',
              'plotVorticityCenter=myPostProcess.bin.trackVortices.plot_vorticity_center:main',
              'writeTkePerArea=myPostProcess.bin.tkePerUnitArea.write_tke_per_unit_area:main',
              'writeSgsTkePerArea=myPostProcesss.bin.sgsTkePerUnitArea.write_sgs_tke_per_unit_area:main',
              'writeTkeStdDev=myPostProcess.bin.tkeStdDev.write_tke_std_dev:main',
              'writeSeparationVolume=myPostProcess.bin.regionOfSeparation.write_separation_volume:main',
              'writeTwoPointCorr=myPostProcess.bin.twoPointCorr.write_two_point_corr:main',
              'writeSpanAvg=myPostProcess.bin.spanwiseAvg.write_spanwise_avg:main',
              'writeIntLengthScale=myPostProcess.bin.intLengthScale.write_int_length_scale:main'
              ]
          },
      install_requires=[
          'numpy',
          'scipy',
          'matplotlib',
          'tqdm',
          ],
      zip_safe=False)
