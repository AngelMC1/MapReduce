#!/bin/bash

# Script para cargar datos al sistema HDFS
# Uso: ./upload_to_hdfs.sh

echo "=== Iniciando carga de datos a HDFS ==="

# Verificar que Hadoop esté disponible
if ! command -v hdfs &> /dev/null
then
    echo "ERROR: Hadoop no está instalado o no está en el PATH"
    exit 1
fi

# Definir variables
HDFS_INPUT_DIR="/data/input"
LOCAL_DATASET="../dataset/datos.csv"
DATASET_NAME="datos.csv"

echo "Verificando conexión con HDFS..."
hdfs dfs -ls / > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: No se puede conectar con HDFS. Verifica que Hadoop esté corriendo."
    exit 1
fi

# Crear directorio en HDFS si no existe
echo "Creando directorio en HDFS: $HDFS_INPUT_DIR"
hdfs dfs -mkdir -p $HDFS_INPUT_DIR

# Verificar si el archivo local existe
if [ ! -f "$LOCAL_DATASET" ]; then
    echo "ERROR: El archivo $LOCAL_DATASET no existe"
    exit 1
fi

# Subir archivo a HDFS (forzar sobrescritura si ya existe)
echo "Subiendo archivo $DATASET_NAME a HDFS..."
hdfs dfs -put -f $LOCAL_DATASET $HDFS_INPUT_DIR/$DATASET_NAME

# Verificar que se subió correctamente
if hdfs dfs -test -e $HDFS_INPUT_DIR/$DATASET_NAME; then
    echo "✓ Archivo subido exitosamente"
    echo "Ubicación en HDFS: hdfs://$HDFS_INPUT_DIR/$DATASET_NAME"
    
    # Mostrar información del archivo
    echo ""
    echo "=== Información del archivo en HDFS ==="
    hdfs dfs -ls $HDFS_INPUT_DIR/$DATASET_NAME
    
    # Mostrar las primeras líneas
    echo ""
    echo "=== Primeras 5 líneas del archivo ==="
    hdfs dfs -cat $HDFS_INPUT_DIR/$DATASET_NAME | head -5
else
    echo "ERROR: No se pudo subir el archivo a HDFS"
    exit 1
fi

echo ""
echo "=== Carga completada exitosamente ==="
