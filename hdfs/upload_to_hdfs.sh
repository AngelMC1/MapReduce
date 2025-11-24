#!/bin/bash

# Script para subir datos al HDFS de Hadoop
# Uso: bash upload_to_hdfs.sh

echo "=========================================="
echo "  Subiendo datos a HDFS"
echo "=========================================="

# Verificar que Hadoop está disponible
if ! command -v hdfs &> /dev/null; then
    echo "ERROR: Comando 'hdfs' no encontrado."
    echo "Asegúrate de que Hadoop esté instalado y en el PATH."
    exit 1
fi

# Verificar que HDFS está corriendo
if ! hdfs dfsadmin -report &> /dev/null; then
    echo "ERROR: HDFS no está corriendo o no está accesible."
    echo "Inicia los servicios de Hadoop primero."
    exit 1
fi

echo ""
echo "[1/3] Creando directorio en HDFS..."
hdfs dfs -mkdir -p /data/input

if [ $? -eq 0 ]; then
    echo "  ✓ Directorio /data/input creado exitosamente"
else
    echo "  ✗ Error al crear directorio (puede que ya exista)"
fi

echo ""
echo "[2/3] Subiendo datos.csv a HDFS..."
hdfs dfs -put -f ../dataset/datos.csv /data/input/

if [ $? -eq 0 ]; then
    echo "  ✓ Archivo subido exitosamente"
else
    echo "  ✗ Error al subir archivo"
    exit 1
fi

echo ""
echo "[3/3] Verificando archivo en HDFS..."
if hdfs dfs -test -e /data/input/datos.csv; then
    echo "  ✓ Archivo existe en HDFS"
    echo ""
    echo "Información del archivo:"
    hdfs dfs -ls /data/input/datos.csv
    echo ""
    echo "Primeras líneas del archivo:"
    hdfs dfs -cat /data/input/datos.csv | head -5
else
    echo "  ✗ Archivo no encontrado en HDFS"
    exit 1
fi

echo ""
echo "=========================================="
echo "  Datos subidos exitosamente a HDFS"
echo "=========================================="
echo ""
echo "Ruta en HDFS: hdfs:///data/input/datos.csv"
echo ""
echo "Para ejecutar el job MapReduce:"
echo "  python mapreduce/job.py -r hadoop hdfs:///data/input/datos.csv"
echo ""
