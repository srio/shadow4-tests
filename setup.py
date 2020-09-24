# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2020 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

#
# Memorandum: 
#
# Install from sources: 
#     git clone https://github.com/srio/shadow4-tests
#     cd shadow4-tests
#     python -m pip install -e . --no-deps --no-binary :all:
#
#

__authors__ = ["M Sanchez del Rio - ESRF"]
__license__ = "MIT"
__date__ = "2020"

from setuptools import setup

PACKAGES = [
    "shadow4-tests",
    "shadow4-tests.io",
    "shadow4-tests.compatibility",
    "shadow4-tests.optical_elements",
    "shadow4-tests.sources",
    "shadow4-tests.preprocessors",
    "shadow4-tests.library",
]

INSTALL_REQUIRES = (
    'setuptools',
    'shadow4',
    'Shadow',
)


setup(name='shadow4-tests',
      version='0.0.1',
      description='shadow4 tests',
      author='Manuel Sanchez del Rio',
      author_email='srio@esrf.eu',
      url='https://github.com/srio/shadow4-tests/',
      packages=PACKAGES,
      install_requires=INSTALL_REQUIRES,
     )

