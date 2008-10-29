#!/usr/bin/env python
#
# Distutils setup script for Munkres
#
# $Id$
# ---------------------------------------------------------------------------

from distutils.core import setup, Extension
import re
import os
import sys
import imp
import string
import time

PYTHON_MODULE_TEMPLATE = \
"""
# Generated automatically on ${datetime}.

import ${ext_module}
utgetents = ${ext_module}.utgetents
"""

def run_command(cmd):
    print '+ %s' % cmd
    return os.system(cmd)

def die(msg):
    print >> sys.stderr, msg
    sys.exit(1)

# Figure out what platform we're using.

if sys.platform.startswith('linux'):
    platform = 'linux'
elif sys.platform.startswith('darwin'):
    platform = 'bsd'
elif sys.platform.find('bsd') >= 0:
    platform = 'bsd'
else:
    die('Unsupported or unknown platform: "%s"' % sys.platform)

# Determine whether the C file is there. If not, build it.

c_file = 'pyutmp_%s.c' % platform
pyx_file = 'pyutmp_%s.pyx' % platform
ext_module = 'pyutmp_%s' % platform

if not os.access(c_file, os.F_OK):
    print 'Can\'t find "%s". Attempting to make it.' % c_file
    rc = run_command('cython %s' % pyx_file)
    if rc != 0:
        die('Failed to build "%s" from "%s"' % (c_file, pyx_file))

# Make the Python module.

py = string.Template(PYTHON_MODULE_TEMPLATE).substitute({
    'ext_module' : ext_module,
    'datetime'   : time.asctime(time.localtime())
})
open('pyutmp.py', 'w').write(py)

# Run setup

setup(
    name='pyutmp',
    version='0.1',
    description='Python UTMP wrapper for Un*x systems',
    long_description='Python UTMP wrapper for Un*x systems',
    url='http://www.clapper.org/software/python/pyutmp/',
    license='BSD license',
    author='Brian M. Clapper',
    author_email='bmc@clapper.org',
    py_modules=['pyutmp',],
    ext_modules=[Extension(ext_module, [c_file]),],
    classifiers = [
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
