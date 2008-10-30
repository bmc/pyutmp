#
# $Id$
# ---------------------------------------------------------------------------

"""
Introduction
============

The ``pyutmp`` module provides a Python-oriented interface to the *utmp*
file on Unix-like operating systems. To paraphrase the *Linux Programmer's
Manual* page *utmp*\ (5), the *utmp* file allows one to discover information
about who is currently using (i.e., is logged into) the system. The *utmp*
file is a series of entries whose structure is typically defined by the
``utmp.h`` C header file.

This module provides an read-only interface to the underlying operating
system's C *utmp* API.

Interface and Usage
===================

The ``pyutmp`` module supplies two classes: `UtmpFile` and `Utmp`. A
`UtmpFile` object represents the open *utmp* file; when you iterate over a
`UtmpFile` object, it yields successive `Utmp` objects. For example:

.. python::

    from pyutmp import UtmpFile
    import time

    for utmp in UtmpFile():
        # utmp is a Utmp object
        if utmp.ut_user_process:
            print '%s logged in at %s on tty %s' % (utmp.ut_user, time.ctime(utmp.ut_time), utmp.ut_line)


UtmpFile
--------

In addition to the ``__iter__()`` generator method, allowing iteration over
the contents of the *utmp* file, the `UtmpFile` class also provides a
``rewind()`` method that permits you to reset the file pointer to the top
of the file. See the class documentation for details.

Utmp
----

The fields of the `Utmp` class are operating system-dependent. However, they
will *always* include at least the following fields:

+---------------------+-----------+----------------------------------------+
| Field               | Type      | Description                            |
+=====================+===========+========================================+
| ``ut_user``         | ``str``   | The user associated with the *utmp*    |
|                     |           | entry, if any.                         |
+---------------------+-----------+----------------------------------------+
| ``ut_line``         | ``str``   | The tty or pseudo-tty associated with  |
|                     |           | the entry, if any. In this API, the    |
|                     |           | line will *always* be the full path to |
|                     |           | the device.                            |
+---------------------+-----------+----------------------------------------+
| ``ut_host``         | ``str``   | The host name associated with the      |
|                     |           | entry, if any.                         |
+---------------------+-----------+----------------------------------------+
| ``ut_time``         | timestamp | The timestamp associated with the      |
|                     |           | entry. This timestamp is in the form   |
|                     |           | returned by ``time.time()`` and may be |
|                     |           | passed directly to methods like        |
|                     |           | ``time.ctime()``.                      |
+---------------------+-----------+----------------------------------------+
| ``ut_user_process`` | ``bool``  | Whether or not the *utmp* entry is a   |
|                     |           | user process (as opposed to a reboot or|
|                     |           | some other system event).              |
+---------------------+-----------+----------------------------------------+
    
On some operating systems, other fields may be present. For instance, on
Linux and Solaris systems (and other System V-derived systems), `Utmp` also
contains the following fields:

+---------------------+-----------+----------------------------------------+
| Optional Field      | Type      | Description                            |
+=====================+===========+========================================+
| ``ut_type``         | ``str``   | The type of the entry, typically one of|
|                     |           | the following string values:           |
|                     |           | "RUN_LVL", "BOOT_TIME", "NEW_TIME",    |
|                     |           | "OLD_TIME", "INIT_PROCESS",            |
|                     |           | "LOGIN_PROCESS", "USER_PROCESS",       |
|                     |           | "DEAD_PROCESS", "ACCOUNTING".          |
|                     |           | See the *utmp*\ (5) manual page for a  |
|                     |           | description of these values            |
+---------------------+-----------+----------------------------------------+
| ``ut_pid``          | ``int``   | Associated process ID, if any.         |
+---------------------+-----------+----------------------------------------+
| ``ut_id``           | ``str``   | The *init*\ (8) ID, or the abbreviated |
|                     |           | tty name.                              |
+---------------------+-----------+----------------------------------------+
| ``ut_exit_code``    | ``int``   | Process exit code, if applicable.      |
+---------------------+-----------+----------------------------------------+
| ``ut_session``      | ``int``   | Session ID, for windowing.             |
+---------------------+-----------+----------------------------------------+
| ``ut_addr``         | ``int``   | IPv4 address of remote host (if        |
|                     | array     | applicable), one octet per array       |
|                     |           | element.                               |
+---------------------+-----------+----------------------------------------+

If you're writing portable code, you should not count on the presence of
those attributes--or, at the very least, you should wrap access to them in
a ``try/catch`` block that catches ``AttributeError``.


Notes
=====

This module has been tested on the following operating systems:

- Ubuntu Linux, version 8.04
- FreeBSD
- Mac OS X 10.4 (Tiger)
- OpenSolaris (2008.05, x86, using the SunStudio 12 compiler suite)

Adding support for other Unix variants should be straightforward.

Restrictions
============

- Access to the *utmp* file is read-only. There is no provision for writing
  to the file.

Copyright and License
=====================

Copyright (c) 2008 Brian M. Clapper

This is free software, released under the following BSD-like license:

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

- Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.

- The end-user documentation included with the redistribution, if any,
  must include the following acknowlegement:

  This product includes software developed by Brian M. Clapper
  (bmc@clapper.org, http://www.clapper.org/bmc/). That software is
  copyright (c) 2008 Brian M. Clapper.

  Alternately, this acknowlegement may appear in the software itself, if
  and wherever such third-party acknowlegements normally appear.

THIS SOFTWARE IS PROVIDED B{AS IS} AND ANY EXPRESSED OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
EVENT SHALL BRIAN M. CLAPPER BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

__docformat__ = 'restructuredtext'

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import sys
import os

# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

__all__ = ['UtmpFile', 'Utmp']

# ---------------------------------------------------------------------------
# Classes
# ---------------------------------------------------------------------------

class UtmpFile(object):
    """
    """
    def __init__(self):
        pass

    def __del__(self):
        pass

    def __iter__(self):
        """
        Generator function that yields each entry from the *utmp* file.
        The method automatically opens and closes the file.

        :rtype: `Utmp`
        :return: Successive `Utmp` objects from the *utmp* file.
        """
        utmp = self._get_next_entry()
        while utmp:
            yield utmp
            utmp = self._get_next_entry()

class Utmp(object):

    pass

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

def _get_platform():
    if sys.platform.startswith('linux'):
        platform = 'linux'

    elif sys.platform.startswith('sunos'):
        platform = 'solaris'

    elif sys.platform.startswith('darwin') or \
         (sys.platform.find('bsd') >= 0):
        platform = 'bsd'
        
    else:
        raise Exception, 'Unknown or unsupported platform: "%s"' %\
              sys.platform
    
    return platform

# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------

class UtmpFile(object):
    """
    Represents the *utmp* file itself.
    """
    def __init__(self, path=None):
        """
        Initialize a new UtmpFile object that will read `Utmp` entries from the
        specified *utmp*\ -format path.

        :Parameters:
            path : str
                Path to the *utmp* file to read. Defaults to the appropriate
                "live" *utmp* file for the current operating system.
        """
        self.__utmp = _pyutmp._UtmpFile(path)

    def __del__(self):
        """
        Destructor: Ensures that all resources (open files, etc.) are
        cleaned up.
        """
        del self.__utmp

    def rewind(self):
        """
        Rewind the *utmp* file to the first entry in the file.
        """
        self.__utmp.rewind()

    def __iter__(self):
        """
        Iterate over the `Utmp` entries in the file. This method is a generator
        method.

        :rtype: `Utmp`
        :return: Successive `Utmp` objects
        """
        u = self.__utmp._get_next_entry()
        while u:
            yield u
            u = self.__utmp._get_next_entry()

class Utmp(object):
    """
    Represents an individual entry in the *utmp* file. At a minimum, a
    Utmp object will contain the following fields.

    :IVariables:
        ut_user : str
           The user associated with the *utmp* entry, if any
        ut_line : str
           The tty or pseudo-tty associated with the entry, if any.
           This value will always be the full path to the device.
        ut_host : str
           The host name associated with the entry, if any.
        ut_time : timestamp
           The timestamp associated with the entry. This timestamp is in
           the form returned by ``time.time()`` and may be passed directly
           to methods like ``time.ctime()``.
        ut_user_process : bool
           ``True`` if the entry represents a user process, ``False`` if not.

    On some operating systems, additional fields may be available. See
    the module documentation for details.
    """
    pass


# Kludge: setup.py sets __IN_SETUP_PY to prevent the import of the C
# extension module that might not yet have been generated.

if not os.environ.get('__IN_SETUP_PY'):
    exec('import pyutmp_%s as _pyutmp' % _get_platform())

