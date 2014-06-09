CC=gfortran
FFLAGS= -falign-loops=2 -falign-jumps=2 -falign-functions=2\
-ffast-math -fno-f2c \
-fforce-addr -fcaller-saves -fstrength-reduce\
-funroll-loops -frerun-cse-after-loop -fno-underscoring

LIB=``

objects = EEE_V15.o iopenfile.o ireadfile.o

EEE_V15 : $(objects)
	gfortran -o EEE_V15 $(objects) $(LIB)

EEE_V15.o : EEE_V15.f 
	gfortran -c $(FFLAGS) EEE_V15.f

iopenfile.o : iopenfile.c 
	gcc -c iopenfile.c

ireadfile.o : ireadfile.c 
	gcc -c ireadfile.c


install :
	cp -f EEE_V15 ${DATE_SITE}/${DATE_HOSTNAME}
	chmod +s ${DATE_SITE}/${DATE_HOSTNAME}/EEE_V15

clean:
	rm -f *.o

cleanall:
	make clean; rm -f EEE_V15
