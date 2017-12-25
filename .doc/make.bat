@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
if "%SPHINXAPIDOC%" == "" (
	set SPHINXAPIDOC=sphinx-apidoc
)
set SOURCEDIR=.
set BUILDDIR=..\docs
set APPDIR=..\src
set SPHINXPROJ=PlasoSqlitePluginScaffolder

if "%1" == "" goto help
if "%1" == "rst" goto rst
if "%1" == "onlyhtml" goto onlyhtml

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.http://sphinx-doc.org/
	exit /b 1
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%

if "%1" == "onlyhtml"(
	:onlyhtml
	%SPHINXBUILD% -M html %SOURCEDIR% %BUILDDIR%
	xcopy %BUILDDIR%\html\*.* %BUILDDIR% /A /E /K /H
	rmdir /s /q %BUILDDIR%\doctrees
	rmdir /s /q %BUILDDIR%\html
)
if "%1" == "rst"(
	:rst
	%SPHINXAPIDOC% -o %SOURCEDIR% %APPDIR%
)

:end
popd
