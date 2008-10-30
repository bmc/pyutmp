#                                                               -*-python-*-
# Cython input file for pyutmp_sysv module.
#
# $Id$
# ---------------------------------------------------------------------------

cdef extern from "time.h":
    struct timeval:
        long tv_sec
        long tv_usec

cdef extern from "utmpx.h":
    struct exit_status:
        short e_termination
        short e_exit

    ctypedef int pid_t

    cdef enum:
         EMPTY = 0
         RUN_LVL = 1
         BOOT_TIME = 2
         OLD_TIME = 3
         NEW_TIME = 4
         INIT_PROCESS = 5
         LOGIN_PROCESS = 6
         USER_PROCESS = 7
         DEAD_PROCESS = 8
         ACCOUNTING = 0
         DOWN_TIME = 10

    struct utmpx:
        short ut_type
        pid_t ut_pid
        char ut_user[32]
        char ut_line[32]
        char ut_id[4]
        char ut_host[257]
        short ut_syslen
        exit_status ut_exit
        int ut_session
        #timeval ut_tv
        long ut_xtime

    void setutxent()
    void endutxent()
    utmpx *getutxent()
    utmpx *getutxline(utmpx *u)
    void utmpxname(char *path)

_TYPE_MAP = {RUN_LVL: 'RUN_LVL',
             BOOT_TIME: 'BOOT_TIME',
             NEW_TIME: 'NEW_TIME',
             OLD_TIME: 'OLD_TIME',
             INIT_PROCESS: 'INIT_PROCESS',
             LOGIN_PROCESS: 'LOGIN_PROCESS',
             USER_PROCESS: 'USER_PROCESS',
             DEAD_PROCESS: 'DEAD_PROCESS',
             ACCOUNTING: 'ACCOUNTING',
             DOWN_TIME: 'DOWN_TIME',}

class Utmp(object):
    ut_type = None
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
            utmpxname(path)

    def __del__(self):
        if self._is_open:
            endutxent()

    def rewind(self):
        setutxent()

    def _get_next_entry(self):
        if not self._is_open:
            setutxent()
            self._is_open = True

        cdef utmpx *entry = getutxent()
        if entry:
            u = Utmp()
            u.ut_type = _TYPE_MAP[entry.ut_type]
            u.ut_user_process = (u.ut_type == 'USER_PROCESS')
            u.ut_pid = entry.ut_pid
            u.ut_id = entry.ut_id
            u.ut_user = entry.ut_user
            u.ut_exit_code = entry.ut_exit.e_exit
            u.ut_time = float(entry.ut_xtime)

            if len(entry.ut_user) > 0:
                u.ut_user = entry.ut_user
            else:
                u.ut_user = None

            if len(entry.ut_line) == 0:
                u.ut_line = None
            else:
                u.ut_line = entry.ut_line
                if not u.ut_line.startswith('/'):
                    u.ut_line = '/dev/' + u.ut_line

            u.ut_host = entry.ut_host[0:entry.ut_syslen]
            if len(u.ut_host) == 0:
                u.ut_host = None

        else:
            u = None
            endutxent()

        return u
