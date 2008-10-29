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
MODULE      = pyutmp_bsd
PYUTMP_SO   = pyutmp_bsd.so
PYUTMP_CPY  = pyutmp_bsd.pyx
PYUTMP_O    = pyutmp_bsd.o
PYUTMP_C    = pyutmp_bsd.c
PYTHON_HOME = /Library/Frameworks/Python.framework/Versions/2.5
LD_SO       = gcc -bundle -flat_namespace -undefined suppress
CC_SO       = gcc -fno-common
LDFLAGS     = -L$(PYTHON_HOME)/lib/python2.5/config -lpython2.5
INCLUDES    = -I$(PYTHON_HOME)/include/python2.5
else

ifeq "$(PLATFORM)" "linux"
MODULE      = pyutmp_linux
PYUTMP_SO   = pyutmp_linux.so
PYUTMP_CPY  = pyutmp_linux.pyx
PYUTMP_O    = pyutmp_linux.o
PYUTMP_C    = pyutmp_linux.c
PYTHON_HOME = /usr
CC_SO       = gcc -fPIC
LD_SO       = gcc -shared
INCLUDES    = -I/usr/include/python2.5
LDFLAGS     = -L$(PYTHON_HOME)/lib/python2.5/config -lpython2.5

else
ifeq "$(PLATFORM)" "bsd"
PYTHON_HOME = /usr/local
MODULE      = pyutmp_bsd
PYUTMP_SO   = pyutmp_bsd.so
PYUTMP_CPY  = pyutmp_bsd.pyx
PYUTMP_O    = pyutmp_bsd.o
PYUTMP_C    = pyutmp_bsd.c
CC_SO       = gcc -fPIC
LD_SO       = gcc -shared
LDFLAGS     = -L$(PYTHON_HOME)/lib/python2.5/config -lpython2.5
INCLUDES    = -I$(PYTHON_HOME)/include/python2.5
endif
endif
endif

CYTHON    = cython
CC        = gcc

.PHONY: all clean

all: $(PYUTMP_SO) pyutmp.py

clean:
	rm -f $(PYUTMP_C) $(PYUTMP_SO) $(PYUTMP_O) pyutmp.py pyutmp.pyc

pyutmp.py:
	echo "import $(MODULE)" >pyutmp.py
	echo "utgetents = $(MODULE).utgetents" >>pyutmp.py
$(PYUTMP_C): $(PYUTMP_CPY)
	$(CYTHON) $(PYUTMP_CPY)
$(PYUTMP_O): $(PYUTMP_C)
	$(CC_SO) $(INCLUDES) -o $(PYUTMP_O) -c $(PYUTMP_C)
$(PYUTMP_SO): $(PYUTMP_O)
	$(LD_SO) -o $(PYUTMP_SO) $(PYUTMP_O) $(LDFLAGS)

