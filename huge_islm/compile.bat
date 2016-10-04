set CC=c:\Rtools\gcc-4.6.3\bin\gcc.exe
rem %CC% -O3 test.c big_islm.c -o test.exe
%CC% -O0 test.c huge_islm.c -o test.exe
