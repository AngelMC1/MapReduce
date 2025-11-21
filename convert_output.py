#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para descargar y convertir la salida de MapReduce desde HDFS
Descarga el archivo part-00000 del directorio de salida en HDFS
y lo convierte a un archivo CSV legible.
"""

import subprocess
import os
import sys
import csv


def ejecutar_comando(comando):
    """
    Ejecuta un comando shell y retorna el resultado.
    
    Args:
        comando (str): Comando a ejecutar
        
    Returns:
        tuple: (success, output, error)
    """
    try:
        resultado = subprocess.run(
            comando,
            shell=True,
            capture_output=True,
            text=True
        )
        return resultado.returncode == 0, resultado.stdout, resultado.stderr
    except Exception as e:
        return False, "", str(e)


def verificar_hdfs():
    """
    Verifica que HDFS esté disponible.
    
    Returns:
        bool: True si HDFS está disponible
    """
    success, _, _ = ejecutar_comando("hdfs version")
    return success


def descargar_desde_hdfs(hdfs_path, local_path):
    """
    Descarga un archivo desde HDFS al sistema local.
    
    Args:
        hdfs_path (str): Ruta del archivo en HDFS
        local_path (str): Ruta local donde guardar el archivo
        
    Returns:
        bool: True si la descarga fue exitosa
    """
    # Eliminar archivo local si existe
    if os.path.exists(local_path):
        os.remove(local_path)
        print(f"✓ Archivo local {local_path} eliminado")
    
    # Descargar desde HDFS
    comando = f"hdfs dfs -get {hdfs_path} {local_path}"
    success, output, error = ejecutar_comando(comando)
    
    if success and os.path.exists(local_path):
        print(f"✓ Archivo descargado desde HDFS: {hdfs_path}")
        return True
    else:
        print(f"✗ Error al descargar: {error}")
        return False


def convertir_a_csv(input_file, output_file):
    """
    Convierte el archivo de salida de MapReduce a un CSV legible.
    
    El formato de entrada es:
    "categoria"\t"count,precio_promedio,total_cantidad,total_ingreso"
    
    Args:
        input_file (str): Archivo de entrada (part-00000)
        output_file (str): Archivo CSV de salida
        
    Returns:
        bool: True si la conversión fue exitosa
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f_in:
            lines = f_in.readlines()
        
        # Preparar datos para el CSV
        datos = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Dividir por tabulador
            partes = line.split('\t')
            if len(partes) != 2:
                continue
            
            # Extraer categoría (quitar comillas si existen)
            categoria = partes[0].strip('"')
            
            # Extraer valores (quitar comillas si existen)
            valores = partes[1].strip('"').split(',')
            
            if len(valores) == 4:
                datos.append({
                    'categoria': categoria,
                    'num_productos': valores[0],
                    'precio_promedio': valores[1],
                    'cantidad_total': valores[2],
                    'ingreso_total': valores[3]
                })
        
        # Escribir CSV
        with open(output_file, 'w', encoding='utf-8', newline='') as f_out:
            if datos:
                fieldnames = ['categoria', 'num_productos', 'precio_promedio', 
                             'cantidad_total', 'ingreso_total']
                writer = csv.DictWriter(f_out, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(datos)
                
                print(f"✓ CSV generado: {output_file}")
                print(f"  Total de categorías: {len(datos)}")
                return True
            else:
                print("✗ No se encontraron datos para convertir")
                return False
                
    except Exception as e:
        print(f"✗ Error al convertir archivo: {e}")
        return False


def main():
    """
    Función principal.
    """
    print("=== Descarga y conversión de resultados MapReduce ===\n")
    
    # Configuración
    HDFS_OUTPUT_DIR = "/data/output"
    HDFS_PART_FILE = f"{HDFS_OUTPUT_DIR}/part-00000"
    LOCAL_TEMP_FILE = "part-00000"
    OUTPUT_CSV = "resultado.csv"
    
    # Verificar que HDFS esté disponible
    print("Verificando conexión con HDFS...")
    if not verificar_hdfs():
        print("✗ ERROR: HDFS no está disponible")
        print("  Asegúrate de que Hadoop esté instalado y en el PATH")
        sys.exit(1)
    print("✓ HDFS disponible\n")
    
    # Verificar que exista el archivo en HDFS
    print(f"Verificando archivo en HDFS: {HDFS_PART_FILE}")
    success, output, error = ejecutar_comando(f"hdfs dfs -test -e {HDFS_PART_FILE}")
    if not success:
        print(f"✗ ERROR: El archivo {HDFS_PART_FILE} no existe en HDFS")
        print("  Asegúrate de haber ejecutado el job MapReduce primero")
        sys.exit(1)
    print("✓ Archivo encontrado en HDFS\n")
    
    # Descargar archivo desde HDFS
    print(f"Descargando {HDFS_PART_FILE}...")
    if not descargar_desde_hdfs(HDFS_PART_FILE, LOCAL_TEMP_FILE):
        sys.exit(1)
    print()
    
    # Convertir a CSV
    print(f"Convirtiendo a formato CSV...")
    if not convertir_a_csv(LOCAL_TEMP_FILE, OUTPUT_CSV):
        sys.exit(1)
    print()
    
    # Limpiar archivo temporal
    if os.path.exists(LOCAL_TEMP_FILE):
        os.remove(LOCAL_TEMP_FILE)
        print(f"✓ Archivo temporal eliminado: {LOCAL_TEMP_FILE}\n")
    
    # Mostrar preview del resultado
    print("=== Preview de resultados ===")
    if os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[:6]:  # Mostrar primeras 6 líneas
                print(line.strip())
    
    print("\n=== Conversión completada exitosamente ===")
    print(f"Archivo generado: {OUTPUT_CSV}")


if __name__ == '__main__':
    main()
