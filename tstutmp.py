import utmp
import time
import tty
import subprocess

def tty():
    p = subprocess.Popen('tty', stdout=subprocess.PIPE)
    p.wait()
    if p.returncode != 0:
        raise Exception, 'tty(1) failed'
    return p.stdout.readlines()[0].strip()

utmps = utmp.utgetents()
for i in range(0, len(utmps)):
    u = utmps[i]
    if u.ut_user_process:
        print '%s %s (%s) from %s' % (time.ctime(u.ut_time), u.ut_user, u.ut_line, u.ut_host)
