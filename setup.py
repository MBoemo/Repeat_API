#!/usr/bin/env python

#----------------------------------------------------------
# Written by Michael A. Boemo (mb915@cam.ac.uk)
# This software is licensed under MIT.  You should have
# received a copy of the license with this software.  If
# not, please Email the author.
#----------------------------------------------------------

from distutils.core import setup
from distutils.extension import Extension
import numpy as np

filenames = [ 'main']

modules= ["Repeat_API/{}".format(name) for name in filenames]

setup(
      name='Repeat_API',
      version='1.0',
      description='Simple API for analysing tandem repeats.',
      author='Michael A. Boemo',
      author_email='mb915@cam.ac.uk',
      url='https://github.com/MBoemo/Repeat_API.git',
      license='MIT',
      packages=['Repeat_API'],
      py_modules=modules
     )
