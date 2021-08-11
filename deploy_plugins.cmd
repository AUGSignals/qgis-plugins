@ECHO OFF

ECHO.
ECHO A3DP GUI Installer
ECHO.
REM TODO: Check for Python 
REM TODO: Check for pip

REM Get user input for online vs offline installation
ECHO This installer requires an internet connection (online install).
ECHO If you do not have internet, you must download the installation files and then choose offline installation.

CHOICE /c yn /n /m "Would you like to perform an offline installation? [y/N] "
ECHO.
goto %ERRORLEVEL%

REM Install Python packages (dependencies)
:1
	ECHO Offline installation selected...
	pip install --no-index --find-links ../py_packages -r requirements.txt

:2
	ECHO Online installation selected...
	pip install -r requirements.txt

REM TODO: Check for pb-tool

REM Set deployment path
SET QgisPluginsPath=%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins

REM Deploy plugins from source directory to QgisPluginsPath
FOR /D %%d IN ("%~dp0*") DO CALL :install_plugin "%%d"

EXIT /B %ERRORLEVEL%

:install_plugin
	@ECHO %~1
	CD "%~1"
	pb_tool deploy -y -p %QgisPluginsPath%
	CD ..
	EXIT /B 0
