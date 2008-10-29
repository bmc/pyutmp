# This will eventually be converted to setup.py logic.
#
# NOTE: Set PLATFORM to "mac", "bsd" or "linux". Make logic currently assumes
# Python 2.5 on all platforms.
#
# Examples:
#
# FreeBSD:   gmake all PLATFORM=bsd
# Mac OS X:  make all PLATFORM=mac
# Linux:     make all PLATFORM=linux


#PLATFORM = mac
#PLATFORM = linux
#PLATFORM = bsd

ifeq "$(PLATFORM)" "mac"
UTMP_SO   = pyutmp.so
UTMP_PY   = utmp-bsd.py
PYTHON_HOME = /Library/Frameworks/Python.framework/Versions/2.5
LD_SO     = gcc -bundle -flat_namespace -undefined suppress
CC_SO     = gcc -fno-common
LDFLAGS   = -L$(PYTHON_HOME)/lib/python2.5/config -lpython2.5
INCLUDES  = -I$(PYTHON_HOME)/include/python2.5
else

ifeq "$(PLATFORM)" "linux"
UTMP_SO   = pyutmp.so
UTMP_PY   = utmp-linux.py
PYTHON_HOME = /usr
CC_SO     = gcc -fPIC
LD_SO     = gcc -shared
INCLUDES  = -I/usr/include/python2.5
LDFLAGS   = -L$(PYTHON_HOME)/lib/python2.5/config -lpython2.5

else
ifeq "$(PLATFORM)" "bsd"
PYTHON_HOME = /usr/local
UTMP_SO   = pyutmp.so
UTMP_PY   = utmp-bsd.py
CC_SO     = gcc -fPIC
LD_SO     = gcc -shared
LDFLAGS   = -L$(PYTHON_HOME)/lib/python2.5/config -lpython2.5
INCLUDES  = -I$(PYTHON_HOME)/include/python2.5
endif
endif
endif

CYTHON    = cython
CC        = gcc

.PHONY: all clean

all: $(UTMP_SO)

clean:
	rm -f pyutmp.c $(UTMP_SO) pyutmp.o

pyutmp.c: $(UTMP_PY)
	@rm -f pyutmp.py
	ln -s $(UTMP_PY) pyutmp.py
	$(CYTHON) pyutmp.py
	rm -f pyutmp.py
pyutmp.o: pyutmp.c
	$(CC_SO) $(INCLUDES) -o pyutmp.o -c pyutmp.c
$(UTMP_SO): pyutmp.o
	$(LD_SO) -o $(UTMP_SO) pyutmp.o $(LDFLAGS)

