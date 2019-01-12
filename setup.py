#############################################################################
##  © Copyright CERN 2018. All rights not expressly granted are reserved.  ##
##                 Author: Gian.Michele.Innocenti@cern.ch                  ##
## This program is free software: you can redistribute it and/or modify it ##
##  under the terms of the GNU General Public License as published by the  ##
## Free Software Foundation, either version 3 of the License, or (at your  ##
## option) any later version. This program is distributed in the hope that ##
##  it will be useful, but WITHOUT ANY WARRANTY; without even the implied  ##
##     warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    ##
##           See the GNU General Public License for more details.          ##
##    You should have received a copy of the GNU General Public License    ##
##   along with this program. if not, see <https://www.gnu.org/licenses/>. ##
#############################################################################

from setuptools import setup, find_packages
from codecs import open
from os import path
from glob import glob

setup(
  name='TwistedKleinTemplate',

  # LAST-TAG is a placeholder. Automatically replaced at deploy time with the right tag
  version='LAST-TAG',

  description='Twisted/Klein webapp template',

  # Long description from Markdown -- https://dustingram.com/articles/2018/03/16/markdown-descriptions-on-pypi
  # Filter out lines that look like GitHub "badges"
  long_description="\n".join([ line for line in open('README.md').read().split("\n") if not line.startswith("[![") ]),
  long_description_content_type='text/markdown',

  url='https://github.com/dberzano/TwistedKleinTemplate',
  author='Dario Berzano',
  author_email='dario.berzano@cern.ch',
  license='GPL',

  # See https://pypi.org/classifiers/
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3.7',
    ],

  # What does your project relate to?
  keywords='HEP Computing MachineLearning',

  # You can just specify the packages manually here if your project is
  # simple. Or you can use find_packages().
  packages=find_packages(),

  # Alternatively, if you want to distribute just a my_module.py, uncomment
  # this:
  #   py_modules=["my_module"],

  # List run-time dependencies here.  These will be installed by pip when
  # your project is installed. For an analysis of "install_requires" vs pip's
  # requirements files see:
  # https://packaging.python.org/en/latest/requirements.html
  install_requires=[ "pylint", "twisted", "klein", "Jinja2" ],

  python_requires='>=3.7',

  # List additional groups of dependencies here (e.g. development
  # dependencies). You can install these using the following syntax,
  # for example:
  # $ pip install -e .[dev,test]
  extras_require={
  },

  # If there are data files included in your packages that need to be
  # installed, specify them here. Note that you need to specify those files in
  # MANIFEST.in as well, since Python tools behave inconsistently
  include_package_data=True,
  package_data={ "webapp.templates": [ "index.html" ],
                 "webapp.static": [ "script.js", "style.css" ] },

  # Although 'package_data' is the preferred approach, in some case you may
  # need to place data files outside of your packages. See:
  # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
  # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
  data_files=[],

  # To provide executable scripts, use entry points in preference to the
  # "scripts" keyword. Entry points provide cross-platform support and allow
  # pip to create the appropriate form of executable for the target platform.
  # See: https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/
  entry_points={
      "console_scripts": [ "twisted-klein-webapp = webapp:main" ]
  }
)
