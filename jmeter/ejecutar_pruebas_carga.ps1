# =============================================================
# ejecutar_pruebas_carga.ps1
# Ejecuta el plan de pruebas JMeter en modo CLI (headless)
# y genera reporte HTML en jmeter/resultados/dashboard/
#
# USO:
#   .\jmeter\ejecutar_pruebas_carga.ps1
#   .\jmeter\ejecutar_pruebas_carga.ps1 -Usuarios 20 -Duracion 180
# =============================================================

param(
    [int]$Usuarios  = 10,
    [int]$RampUp    = 30,
    [int]$Duracion  = 120,
    [int]$ThinkTime = 1500,
    [string]$JMeterBin = "C:\apache-jmeter\bin\jmeter.bat"
)

# Asegurar que JMeter use Java 11 (instalado via winget)
$java11 = (Get-ChildItem "C:\Program Files\Eclipse Adoptium" -Filter "jdk-11*" -Directory -ErrorAction SilentlyContinue | Select-Object -First 1).FullName
if ($java11) { $env:JAVA_HOME = $java11 }

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path $PSScriptRoot -Parent
$JmxFile     = Join-Path $PSScriptRoot "timeanddate_load_test.jmx"
$ResultsDir  = Join-Path $PSScriptRoot "resultados"
$Timestamp   = Get-Date -Format "yyyyMMdd_HHmmss"
$JtlFile     = Join-Path $ResultsDir "resultados_$Timestamp.jtl"
$DashboardDir = Join-Path $ResultsDir "dashboard_$Timestamp"

# Verificar JMeter instalado
if (-not (Test-Path $JMeterBin)) {
    Write-Error @"
JMeter no encontrado en: $JMeterBin

INSTALA JMETER:
  1. Descarga desde: https://jmeter.apache.org/download_jmeter.cgi
     Archivo: apache-jmeter-5.6.3.zip  (o la version mas reciente)
  2. Extrae en C:\apache-jmeter\
  3. Asegurate de tener Java 11+ instalado:
     java -version
  4. (Opcional) Agrega C:\apache-jmeter\bin al PATH del sistema

O pasa la ruta correcta con -JMeterBin:
  .\ejecutar_pruebas_carga.ps1 -JMeterBin "C:\tu-ruta\bin\jmeter.bat"
"@
}

# Limpiar si existe (JMeter requiere dir inexistente o vacio)
if (Test-Path $DashboardDir) {
    Remove-Item $DashboardDir -Recurse -Force
}
# NO pre-crear el dir — JMeter lo crea solo

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  PRUEBAS DE CARGA - TimeAndDate.com" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Usuarios    : $Usuarios"
Write-Host "  Ramp-up     : $RampUp seg"
Write-Host "  Duracion    : $Duracion seg"
Write-Host "  Think time  : $ThinkTime ms"
Write-Host "  JTL output  : $JtlFile"
Write-Host "  Dashboard   : $DashboardDir"
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Ejecutar JMeter CLI
& $JMeterBin -n -t $JmxFile -l $JtlFile -e -o $DashboardDir -JNUM_USUARIOS=$Usuarios -JRAMP_UP_SEG=$RampUp -JDURACION_SEG=$Duracion -JTHINK_TIME_MS=$ThinkTime

$indexHtml = Join-Path $DashboardDir "index.html"
if ($LASTEXITCODE -eq 0 -and (Test-Path $indexHtml)) {
    Write-Host ""
    Write-Host "PRUEBAS COMPLETADAS" -ForegroundColor Green
    Write-Host "Reporte HTML: $indexHtml" -ForegroundColor Green
    Start-Process $indexHtml
} elseif (Test-Path $JtlFile) {
    Write-Host ""
    Write-Host "JMeter termino (codigo $LASTEXITCODE) pero sin dashboard." -ForegroundColor Yellow
    Write-Host "JTL disponible: $JtlFile" -ForegroundColor Yellow
    Write-Host "Generar dashboard manualmente:" -ForegroundColor Cyan
    Write-Host "  jmeter -g `"$JtlFile`" -o `"$DashboardDir`"" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "ERROR: JMeter fallo (codigo $LASTEXITCODE)" -ForegroundColor Red
    Write-Host "Revisa la salida anterior para ver el error." -ForegroundColor Yellow
}
