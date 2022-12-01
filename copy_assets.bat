@ECHO OFF

FOR /D %%d IN ("%~dp0*") DO CALL :copy_assets "%%d"

EXIT /B %ERRORLEVEL%

:copy_assets
	@ECHO Copying to " %~1 "
	COPY /Y "assets\output_dialog.*" "%~1"\
	COPY /Y "assets\icon.png" "%~1"\
	EXIT /B 0
