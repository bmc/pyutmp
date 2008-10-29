import pyutmp
import time
import tty
import subprocess

def tty():
    p = subprocess.Popen('tty', stdout=subprocess.PIPE)
    p.wait()
    if p.returncode != 0:
        raise Exception, 'tty(1) failed'
    return p.stdout.readlines()[0].strip()

f = UtmpFile()
for u in f:
    if u.ut_user_process:
        print '%s %s (%s) from %s' % (time.ctime(u.ut_time), u.ut_user, u.ut_line, u.ut_host)
