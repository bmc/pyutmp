#                                                               -*-python-*-
# Cython input file for pyutmp_sysv module.
#
# $Id$
# ---------------------------------------------------------------------------

cdef extern from "time.h":
    struct timeval:
        long tv_sec
        long tv_usec

cdef extern from "utmp.h":
    struct exit_status:
        short e_termination
        short e_exit

    ctypedef int pid_t

    cdef enum:
         UT_LINESIZE = 1
         UT_NAMESIZE = 1
         UT_HOSTSIZE = 1
         UT_UNKNOWN = 0
         RUN_LVL = 1
         BOOT_TIME = 2
         NEW_TIME = 3
         OLD_TIME = 4
         INIT_PROCESS = 5
         LOGIN_PROCESS = 6
         USER_PROCESS = 7
         DEAD_PROCESS = 8
         ACCOUNTING = 9

    struct utmp:
        short ut_type
        pid_t ut_pid
        char ut_line[UT_LINESIZE]
        char ut_id[4]
        char ut_user[UT_NAMESIZE]
        char ut_host[UT_HOSTSIZE]
        exit_status ut_exit
        long ut_session
        timeval ut_tv
        int ut_addr_v6[4]

    void setutent()
    void endutent()
    utmp *getutent()
    utmp *getutline(utmp *u)
    void utmpname(char *path)

_TYPE_MAP = {RUN_LVL: 'RUN_LVL',
             BOOT_TIME: 'BOOT_TIME',
             NEW_TIME: 'NEW_TIME',
             OLD_TIME: 'OLD_TIME',
             INIT_PROCESS: 'INIT_PROCESS',
             LOGIN_PROCESS: 'LOGIN_PROCESS',
             USER_PROCESS: 'USER_PROCESS',
             DEAD_PROCESS: 'DEAD_PROCESS',
             ACCOUNTING: 'ACCOUNTING'}

class Utmp(object):
    ut_type = UT_UNKNOWN
    ut_pid = None
    ut_line = None
    ut_id = None
    ut_user = None
    ut_host = None
    ut_exit_code = 0
    ut_session = None
    ut_time = None
    ut_addr = None
    ut_user_process = False

class _UtmpFile(object):
    def __init__(self, path=None):
        self._is_open = False
        if path:
            utmpname(path)

    def __del__(self):
        if self._is_open:
            endutent()

    def rewind(self):
        setutent()

    def _get_next_entry(self):
        if not self._is_open:
            setutent()
            self._is_open = True

        cdef utmp *entry = getutent()
        if entry:
            u = Utmp()
            u.ut_type = _TYPE_MAP[entry.ut_type]
            u.ut_user_process = (u.ut_type == 'USER_PROCESS')
            u.ut_line = entry.ut_line
            if u.ut_line[0] != '/':
                u.ut_line = '/dev/' + u.ut_line
            u.ut_pid = entry.ut_pid
            u.ut_id = entry.ut_id
            u.ut_user = entry.ut_user
            u.ut_host = entry.ut_host
            u.ut_exit_code = entry.ut_exit.e_exit
            u.ut_time = float(entry.ut_tv.tv_sec)
            u.ut_addr = entry.ut_addr_v6[0]
        else:
            u = None
            endutent()

        return u
