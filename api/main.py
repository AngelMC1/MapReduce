#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API REST con FastAPI para consultar resultados del análisis MapReduce
Expone los resultados procesados en formato JSON
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Dict
import csv
import os
from pathlib import Path


# Inicializar la aplicación FastAPI
app = FastAPI(
    title="API de Análisis de Productos",
    description="API para consultar resultados del análisis MapReduce de productos",
    version="1.0.0"
)


def leer_resultados_csv(archivo: str = "resultado.csv") -> List[Dict]:
    """
    Lee el archivo CSV con los resultados y lo convierte a una lista de diccionarios.
    
    Args:
        archivo (str): Ruta al archivo CSV
        
    Returns:
        List[Dict]: Lista de resultados
        
    Raises:
        FileNotFoundError: Si el archivo no existe
    """
    # Buscar el archivo en el directorio raíz del proyecto
    ruta_base = Path(__file__).parent.parent
    ruta_archivo = ruta_base / archivo
    
    if not ruta_archivo.exists():
        raise FileNotFoundError(f"El archivo {archivo} no existe en {ruta_archivo}")
    
    resultados = []
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convertir valores numéricos
            resultados.append({
                'categoria': row['categoria'],
                'num_productos': int(row['num_productos']),
                'precio_promedio': float(row['precio_promedio']),
                'cantidad_total': int(row['cantidad_total']),
                'ingreso_total': float(row['ingreso_total'])
            })
    
    return resultados


@app.get("/")
async def root():
    """
    Endpoint raíz con información básica de la API.
    """
    return {
        "mensaje": "API de Análisis de Productos con MapReduce",
        "version": "1.0.0",
        "endpoints": {
            "/resultados": "GET - Obtener todos los resultados del análisis",
            "/resultados/{categoria}": "GET - Obtener resultados de una categoría específica",
            "/estadisticas": "GET - Obtener estadísticas generales"
        }
    }


@app.get("/resultados")
async def obtener_resultados():
    """
    Obtiene todos los resultados del análisis MapReduce.
    
    Returns:
        JSONResponse: Lista completa de resultados por categoría
    """
    try:
        resultados = leer_resultados_csv()
        
        return JSONResponse(
            content={
                "total_categorias": len(resultados),
                "resultados": resultados
            },
            status_code=200
        )
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Archivo de resultados no encontrado. Ejecuta primero el MapReduce y convert_output.py"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al leer los resultados: {str(e)}"
        )


@app.get("/resultados/{categoria}")
async def obtener_resultado_por_categoria(categoria: str):
    """
    Obtiene los resultados de una categoría específica.
    
    Args:
        categoria (str): Nombre de la categoría
        
    Returns:
        JSONResponse: Resultados de la categoría solicitada
    """
    try:
        resultados = leer_resultados_csv()
        
        # Buscar la categoría (case-insensitive)
        resultado = next(
            (r for r in resultados if r['categoria'].lower() == categoria.lower()),
            None
        )
        
        if resultado:
            return JSONResponse(content=resultado, status_code=200)
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Categoría '{categoria}' no encontrada"
            )
            
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Archivo de resultados no encontrado"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al buscar la categoría: {str(e)}"
        )


@app.get("/estadisticas")
async def obtener_estadisticas():
    """
    Obtiene estadísticas generales del análisis.
    
    Returns:
        JSONResponse: Estadísticas agregadas de todas las categorías
    """
    try:
        resultados = leer_resultados_csv()
        
        if not resultados:
            raise HTTPException(
                status_code=404,
                detail="No hay resultados disponibles"
            )
        
        # Calcular estadísticas generales
        total_productos = sum(r['num_productos'] for r in resultados)
        total_cantidad = sum(r['cantidad_total'] for r in resultados)
        total_ingresos = sum(r['ingreso_total'] for r in resultados)
        precio_promedio_global = sum(r['precio_promedio'] for r in resultados) / len(resultados)
        
        # Encontrar categoría con más ingresos
        categoria_top = max(resultados, key=lambda x: x['ingreso_total'])
        
        estadisticas = {
            "resumen_general": {
                "total_productos": total_productos,
                "total_unidades": total_cantidad,
                "ingresos_totales": round(total_ingresos, 2),
                "precio_promedio_global": round(precio_promedio_global, 2),
                "numero_categorias": len(resultados)
            },
            "categoria_top": {
                "nombre": categoria_top['categoria'],
                "ingresos": round(categoria_top['ingreso_total'], 2)
            },
            "por_categoria": resultados
        }
        
        return JSONResponse(content=estadisticas, status_code=200)
        
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Archivo de resultados no encontrado"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al calcular estadísticas: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """
    Endpoint para verificar el estado de la API.
    """
    return {
        "estado": "activo",
        "servicio": "API MapReduce"
    }


# Para ejecutar la aplicación directamente
if __name__ == "__main__":
    import uvicorn
    
    print("=== Iniciando servidor FastAPI ===")
    print("Documentación disponible en: http://localhost:8000/docs")
    print("API disponible en: http://localhost:8000")
    print("\nPresiona Ctrl+C para detener el servidor\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
