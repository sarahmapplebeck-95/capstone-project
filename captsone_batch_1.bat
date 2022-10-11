rem How to run a Python script in a given conda environment from a batch file.

rem Define here the path to your conda installation
set CONDAPATH=C:\Users\SarahMapplebeck\anaconda3

rem Define here the name of the environment
set ENVNAME=capstone1

rem The following command activates the base environment.
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)

rem Activate the conda environment
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%

rem Set filepath so file can be run in the enviroment.
set FILEPATH=C:\Users\SarahMapplebeck\Documents\Digital_Futures\project

rem Run a python script in that environment
python %FILEPATH%\Original_transform.py

rem Deactivate the environment
call conda deactivate