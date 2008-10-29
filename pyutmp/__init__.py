#
# $Id$


class UtmpFileBase(object):

    def __init__(self):
        pass

    def __del__(self):
        pass

    def __iter__(self):
        utmp = self.get_next_entry()
        while utmp:
            yield utmp
            utmp = self.get_next_entry()

from pyutmp.pyutmp_platform import *
