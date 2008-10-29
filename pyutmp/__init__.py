#
# $Id$
# ---------------------------------------------------------------------------

import sys
import os

__all__ = ['UtmpFile']

class UtmpFileBase(object):

    def __init__(self):
        pass

    def __del__(self):
        pass

    def __iter__(self):
        utmp = self._get_next_entry()
        while utmp:
            yield utmp
            utmp = self._get_next_entry()


def _get_platform():
    if sys.platform.startswith('linux') or \
       sys.platform.startswith('solaris'):
        platform = 'sysv'
    
    elif sys.platform.startswith('darwin') or \
         (sys.platform.find('bsd') >= 0):
        platform = 'bsd'
        
    else:
        raise Exception, 'Unknown or unsupported platform: "%s"' %\
              sys.platform
    
    return platform

if not os.environ.get('_IN_SETUP_PY'):
    platform = _get_platform()
    exec('import pyutmp_%s as _pyutmp' % platform)
    
    UtmpFile = _pyutmp.UtmpFile
