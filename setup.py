from setuptools import setup
from setuptools import find_packages

setup(name='myPostprocess',
      description='Package to perform post-porcessing of data from OpenFOAM simulations',
      version='1.0.0',
      author='Siddhesh Shinde',
      packages=find_packages(),
      entry_points = {
          'console_scripts':[
              'writeVorticityCenter=myPostprocess.bin.trackVortices.write_vorticity_center:main',
              'plotVorticityCenter=myPostprocess.bin.trackVortices.plot_vorticity_center:main',
              'writeTkePerArea=myPostprocess.bin.tkePerUnitArea.write_tke_per_unit_area:main',
              'writeSgsTkePerArea=myPostprocesss.bin.sgsTkePerUnitArea.write_sgs_tke_per_unit_area:main',
              'writeTkeStdDev=myPostprocess.bin.tkeStdDev.write_tke_std_dev:main',
              'writeSeparationVolume=myPostprocess.bin.regionOfSeparation.write_separation_volume:main',
              'writeTwoPointCorr=myPostprocess.bin.twoPointCorr.write_two_point_corr:main',
              'writeSpanAvg=myPostprocess.bin.spanwiseAvg.write_spanwise_avg:main',
              'writeIntLengthScale=myPostprocess.bin.intLengthScale.write_int_length_scale:main'
              ]
          },
      install_requires=[
          'numpy',
          'scipy',
          'matplotlib',
          'tqdm',
          ],
      zip_safe=False)
