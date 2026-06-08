@echo off
:: =============================================================
:: ejecutar_pruebas_carga.bat
:: Ejecuta pruebas de carga JMeter desde CMD o doble-clic
:: USO: ejecutar_pruebas_carga.bat [usuarios] [rampup_seg] [duracion_seg]
::   ejecutar_pruebas_carga.bat           -> 10 usuarios, 30s ramp, 120s
::   ejecutar_pruebas_carga.bat 20 30 180 -> 20 usuarios, 30s ramp, 180s
:: =============================================================

:: Valores por defecto
set USUARIOS=10
set RAMPUP=30
set DURACION=120

:: Sobreescribir si se pasan argumentos
if not "%~1"=="" set USUARIOS=%~1
if not "%~2"=="" set RAMPUP=%~2
if not "%~3"=="" set DURACION=%~3

:: Rutas (JMETER_CMD — no usar JMETER_BIN, es variable interna de jmeter.bat)
set JMETER_CMD=C:\apache-jmeter\bin\jmeter.bat
set JMX=%~dp0timeanddate_load_test.jmx
set RESULTS_DIR=%~dp0resultados

:: Usar Java 11 (Temurin instalado)
for /d %%D in ("C:\Program Files\Eclipse Adoptium\jdk-11*") do set JAVA_HOME=%%D

:: Timestamp para nombre de archivos
for /f "tokens=1-6 delims=/:. " %%a in ("%date% %time%") do (
    set YY=%%c
    set MM=%%b
    set DD=%%a
    set HH=%%d
    set MIN=%%e
    set SS=%%f
)
set TS=%YY%%MM%%DD%_%HH%%MIN%%SS%
set JTL=%RESULTS_DIR%\resultados_%TS%.jtl
set DASH=%RESULTS_DIR%\dashboard_%TS%

echo.
echo ============================================
echo   PRUEBAS DE CARGA - TimeAndDate.com
echo ============================================
echo   Usuarios  : %USUARIOS%
echo   Ramp-up   : %RAMPUP% seg
echo   Duracion  : %DURACION% seg
echo   JAVA_HOME : %JAVA_HOME%
echo   JTL       : %JTL%
echo   Dashboard : %DASH%
echo ============================================
echo.

if not exist "%JMETER_CMD%" (
    echo ERROR: JMeter no encontrado en %JMETER_CMD%
    pause
    exit /b 1
)

:: Paso 1: ejecutar test (sin -e -o para evitar fallo si el CSV tiene datos de error)
call "%JMETER_CMD%" -n -t "%JMX%" -l "%JTL%" -JNUM_USUARIOS=%USUARIOS% -JRAMP_UP_SEG=%RAMPUP% -JDURACION_SEG=%DURACION%

if not exist "%JTL%" (
    echo ERROR: JTL no generado. Revisa la salida anterior.
    pause
    exit /b 1
)

echo.
echo Generando reporte HTML...
call "%JMETER_CMD%" -g "%JTL%" -o "%DASH%"

if exist "%DASH%\index.html" (
    echo.
    echo PRUEBAS COMPLETADAS
    echo Reporte: %DASH%\index.html
    start "" "%DASH%\index.html"
) else (
    echo.
    echo Reporte no generado, pero JTL disponible:
    echo %JTL%
)
pause
