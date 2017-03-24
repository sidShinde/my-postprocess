from setuptools import setup
from setuptools import find_packages

setup(name='vgAnalysis',
      description='Package to perform post-porcessing of data from OpenFOAM simulations',
      version='1.0.0',
      author='Siddhesh Shinde',
      packages=find_packages(),
      entry_points = {
          'console_scripts':[
              'writeVorticityCenter=vgAnalysis.bin.trackVortices.write_vorticity_center:main',
              'plotVorticityCenter=vgAnalysis.bin.trackVortices.plot_vorticity_center:main', 
              'writeTkePerArea=vgAnalysis.bin.tkePerUnitArea.write_tke_per_unit_area:main'
              ]
          },
      install_requires=[
          'numpy',
          'scipy',
          'matplotlib',
          ],
      zip_safe=False)

