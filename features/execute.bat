@echo off
cd /d "%~dp0.."
behave -f html -o reporte_pruebas.html features/
