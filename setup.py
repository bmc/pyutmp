#!/usr/bin/env python
#
# Distutils setup script for pyutmp
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

DESCRIPTION = 'Python UTMP wrapper for Un*x systems',
HERE = os.path.dirname(os.path.abspath(__file__))
PACKAGE = 'pyutmp'

sys.path = [HERE] + sys.path

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
    die('Unknown or unsupported platform: "%s"' % sys.platform)

# Determine whether the C file is there. If not, build it. If it's older than
# the pyx file, build it.

os.chdir('pyutmp')
c_file = 'pyutmp_%s.c' % platform
pyx_file = 'pyutmp_%s.pyx' % platform
ext_module = 'pyutmp_%s' % platform
ext_package = os.path.join(PACKAGE, ext_module)

build_c_file = False
if not os.access(c_file, os.F_OK):
    build_c_file = True
    print 'Can\'t find "%s". Attempting to make it.' % c_file
else:
    st_c = os.stat(c_file)
    st_pyx = os.stat(pyx_file)
    if st_c.st_mtime < st_pyx.st_mtime:
        print '"%s" is newer than "%s". Rebuilding "%s".' %\
              (pyx_file, c_file, c_file)
        build_c_file = True
if build_c_file:
    rc = run_command('cython %s' % pyx_file)
    if rc != 0:
        die('Failed to build "%s" from "%s"' % (c_file, pyx_file))
os.chdir(HERE)

# Build the platform-specific file

template = ''.join(open(os.path.join(PACKAGE, 'pyutmp_platform.pyt')).readlines())
s = string.Template(template).substitute(
    {'datetime'   : time.asctime(time.localtime()),
     'ext_module' : ext_module}
)
open(os.path.join(PACKAGE, 'pyutmp_platform.py'), 'w').write(s)

# Run setup

setup(
    name='pyutmp',
    packages = [PACKAGE],
    version='0.1',
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    url='http://www.clapper.org/software/python/pyutmp/',
    license='BSD license',
    author='Brian M. Clapper',
    author_email='bmc@clapper.org',
    py_modules=['pyutmp',],
    ext_modules=[Extension(ext_package, [os.path.join(PACKAGE, c_file)]),],
    classifiers = [
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
