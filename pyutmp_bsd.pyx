cdef extern from "time.h":
    struct timeval:
        long tv_sec
        long tv_usec

cdef extern from "string.h":
    char *strncpy(char *dest, char *src, int n)

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
    int open(char *file, int flags, int mode)
    int close(int fd)
    int read(int fd, void *buf, int n)

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

def utgetents():
    cdef utmp entry
    cdef int bytes
    cdef int f_utmp

    f_utmp = open(_PATH_UTMP, O_RDONLY, 0)
    if f_utmp < 0:
        return []

    try:
        bytes = read(f_utmp, &entry, sizeof(entry))
        results = []
        while bytes > 0:
            entry.ut_host[UT_HOSTSIZE - 1] = '\0'
            entry.ut_line[UT_LINESIZE - 1] = '\0'
            entry.ut_name[UT_NAMESIZE - 1] = '\0'
            utmp = Utmp()
            utmp.ut_user_process = len(entry.ut_name) > 0
            utmp.ut_user = entry.ut_name
            utmp.ut_line = entry.ut_line
            if len(entry.ut_host) > 0:
                utmp.ut_host = entry.ut_host
            else:
                utmp.ut_host = 'localhost'
            utmp.ut_time = entry.ut_time
            results.append(utmp)

            bytes = read(f_utmp, &entry, sizeof(entry))

        return results

    finally:
        close(f_utmp)
