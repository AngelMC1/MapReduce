# Script para ejecutar el pipeline completo del proyecto MapReduce

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PIPELINE MAPREDUCE CON MRJOB" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Activar entorno virtual
Write-Host "[1/4] Activando entorno virtual..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Ejecutar MapReduce con MRJob
Write-Host "`n[2/4] Ejecutando job MapReduce..." -ForegroundColor Yellow
python mapreduce/job.py dataset/datos.csv > output_temp.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "  Exito: Job MapReduce completado" -ForegroundColor Green
} else {
    Write-Host "  ERROR: Fallo el job MapReduce" -ForegroundColor Red
    exit 1
}

# Convertir salida a CSV
Write-Host "`n[3/4] Convirtiendo resultados a CSV..." -ForegroundColor Yellow
python -c @"
import csv
import sys

# Leer output de MapReduce con diferentes encodings
lines = []
for encoding in ['utf-8', 'utf-16', 'latin-1']:
    try:
        with open('output_temp.txt', 'r', encoding=encoding) as f:
            lines = [line.strip() for line in f if line.strip() and '\t' in line]
        break
    except:
        continue

# Parsear y convertir a CSV
data = []
for line in lines:
    parts = line.split('\t')
    if len(parts) == 2:
        categoria = parts[0].replace('\"', '').strip()
        valores = parts[1].replace('\"', '').split(',')
        if len(valores) == 4:
            data.append({
                'categoria': categoria,
                'num_productos': valores[0].strip(),
                'precio_promedio': valores[1].strip(),
                'rating_promedio': valores[2].strip(),
                'total_reviews': valores[3].strip()
            })

# Escribir CSV
with open('resultado.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['categoria', 'num_productos', 'precio_promedio', 'rating_promedio', 'total_reviews'])
    writer.writeheader()
    writer.writerows(data)

print('CSV generado correctamente')
"@

if ($LASTEXITCODE -eq 0) {
    Write-Host "  Exito: CSV generado" -ForegroundColor Green
} else {
    Write-Host "  ERROR: Fallo la conversion" -ForegroundColor Red
    exit 1
}

# Mostrar resultados
Write-Host "`n[4/4] Resultados:" -ForegroundColor Yellow
Get-Content resultado.csv
Write-Host ""

# Limpiar archivos temporales
Remove-Item output_temp.txt -ErrorAction SilentlyContinue

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PIPELINE COMPLETADO EXITOSAMENTE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para iniciar la API REST:" -ForegroundColor Cyan
Write-Host "  uvicorn api.main:app --reload" -ForegroundColor White
Write-Host ""
