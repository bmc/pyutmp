#                                                               -*-python-*-
# Cython input file for pyutmp_bsd module.
#
# $Id$
# ---------------------------------------------------------------------------

cdef extern from "sys/types.h":
    ctypedef int size_t
    ctypedef int time_t

cdef extern from "utmp.h":
    struct exit_status:
        short e_termination
        short e_exit

    ctypedef int pid_t

    cdef enum:
         UT_LINESIZE = 1
         UT_NAMESIZE = 1
         UT_HOSTSIZE = 1

    cdef char *_PATH_UTMP

    struct utmp:
        char ut_line[UT_LINESIZE]
        char ut_name[UT_NAMESIZE]
        char ut_host[UT_HOSTSIZE]
        time_t ut_time

cdef extern from "fcntl.h":
    ctypedef int off_t
    ctypedef int mode_t

    int open(char *file, int flags, mode_t mode)
    int close(int fd)
    int read(int fd, void *buf, int n)
    int lseek(int fd, off_t offset, int whence)

    cdef enum:
        SEEK_SET = 0
        SEEK_CUR = 1
        SEEK_END = 2

    cdef enum:
        O_RDONLY = 0
        O_WRONLY = 1
        O_RDWR   = 2

class Utmp(object):
    ut_line = None
    ut_user = None
    ut_host = None
    ut_time = None
    ut_user_process = False

class _UtmpFile(object):

    def __init__(self, path=None):
        if not path:
            path = _PATH_UTMP
        self._fd = open(path, O_RDONLY, 0)

    def __del__(self):
        close(self._fd)

    def rewind(self):
        lseek(self._fd, 0, SEEK_SET)

    def _get_next_entry(self):
        cdef utmp entry
        cdef int bytes

        bytes = read(self._fd, &entry, sizeof(entry))
        if bytes > 0:
            entry.ut_host[UT_HOSTSIZE - 1] = '\0'
            entry.ut_line[UT_LINESIZE - 1] = '\0'
            entry.ut_name[UT_NAMESIZE - 1] = '\0'
            u = Utmp()
            u.ut_user_process = len(entry.ut_name) > 0
            u.ut_user = entry.ut_name
            u.ut_line = entry.ut_line
            if u.ut_line[0] != '/':
                u.ut_line = '/dev/' + u.ut_line
            if len(entry.ut_host) > 0:
                u.ut_host = entry.ut_host
            else:
                u.ut_host = None
            u.ut_time = entry.ut_time

        else:
            u = None
            close(self._fd)
            self._fd = -1

        return u

    def items(self):
        return [item for item in self]

