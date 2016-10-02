set PYTHON=c:\Users\rvh\AppData\Local\Continuum\Anaconda3\python.exe
call %PYTHON% ../convert_mdl.py intermediate_islm.mdl --output-type=C
call %PYTHON% ../convert_mdl.py intermediate_islm.mdl --output-type=R
call %PYTHON% ../convert_mdl.py intermediate_islm.mdl --output-type=Python
call %PYTHON% ../convert_mdl.py intermediate_islm.mdl --output-type=Julia
call %PYTHON% ../convert_mdl.py intermediate_islm.mdl --output-type=Matlab
