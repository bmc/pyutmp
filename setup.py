#!/usr/bin/env python
#
# Distutils setup script for pyutmp
#
# $Id$
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

from distutils.core import setup, Extension
import os
import sys
import imp

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DESCRIPTION = 'Python UTMP wrapper for Un*x systems'
HERE = os.path.dirname(os.path.abspath(__file__))
PACKAGE = 'pyutmp'

sys.path = [HERE] + sys.path

# ---------------------------------------------------------------------------
# Functions 
# ---------------------------------------------------------------------------

def run_command(cmd):
    print '+ %s' % cmd
    return os.system(cmd)

def die(msg):
    print >> sys.stderr, msg
    sys.exit(1)

# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------

# Get some info from the module itself.

mf = os.path.join(HERE, 'pyutmp', '__init__.py')
os.environ['__IN_SETUP_PY'] = 'True'
m = imp.load_module('pyutmp', open(mf), mf,
                    ('__init__.py', 'r', imp.PY_SOURCE))
platform = m._get_platform()
long_description = m.__doc__

# Scrub the long description, for PyPI. It uses normal reStructuredText;
# we have to remove some epydoc-isms.

lines = long_description.split('\n')
lines2 = []
for line in lines:
    if line.startswith('.. python::'):
        lines2.append('::')
        continue

    line = line.replace('``', '%%--%%').replace('`', '').replace('%%--%%', '``')
    lines2.append(line)

long_description = '\n'.join(lines2)
del lines
del lines2

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

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

setup(
    name='pyutmp',
    packages = [PACKAGE],
    version='0.2',
    description=DESCRIPTION,
    long_description=long_description,
    url='http://www.clapper.org/software/python/pyutmp/',
    license='BSD license',
    author='Brian M. Clapper',
    author_email='bmc@clapper.org',
    py_modules=['pyutmp'],
    ext_modules=[Extension(ext_package,
                           [os.path.join(PACKAGE, c_file)],)],
    classifiers = [
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
