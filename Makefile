PLATFORM = mac
#PLATFORM = linux
#PLATFORM = bsd

ifeq "$(PLATFORM)" "mac"
#UTMP_SO = utmp.dylib
UTMP_SO = utmp.so
PYTHON_HOME = /Library/Frameworks/Python.framework/Versions/2.5
#LD_SO     = gcc -dynamiclib -install_name utmp.1.dylib -current_version 1.0.0 -compatibility_version 1.0 
LD_SO     = gcc -bundle -flat_namespace -undefined suppress
CC_SO     = gcc -fno-common
LDFLAGS   = -L$(PYTHON_HOME)/lib/python2.5/config -lpython2.5
INCLUDES  = -I$(PYTHON_HOME)/include/python2.5
else

ifeq "$(PLATFORM)" "linux"
UTMP_SO = utmp.so
PYTHON_HOME = /usr
CC_SO     = gcc -fPIC
LD_SO
INCLUDES  = -I/usr/include/python2.5
LDFLAGS   = -L$(PYTHON_HOME)/lib/python2.5/config -lpython2.5
endif

endif

CYTHON    = cython
CC        = gcc

.PHONY: all clean

all: $(UTMP_SO)

clean:
	rm -f utmp.c $(UTMP_SO) utmp.o

utmp.c: utmp-$(PLATFORM).py
	@rm -f utmp.py
	ln -s utmp-$(PLATFORM).py utmp.py
	$(CYTHON) utmp.py
	rm -f utmp.py
utmp.o: utmp.c
	$(CC_SO) $(INCLUDES) -o utmp.o -c utmp.c
$(UTMP_SO): utmp.o
	$(LD_SO) -o $(UTMP_SO) utmp.o $(LDFLAGS)

