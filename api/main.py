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
                'rating_promedio': float(row['rating_promedio']),
                'total_reviews': int(row['total_reviews'])
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
        total_reviews = sum(r['total_reviews'] for r in resultados)
        precio_promedio_global = sum(r['precio_promedio'] for r in resultados) / len(resultados)
        rating_promedio_global = sum(r['rating_promedio'] for r in resultados) / len(resultados)
        
        # Encontrar categoría con mejor rating
        categoria_top_rating = max(resultados, key=lambda x: x['rating_promedio'])
        
        # Encontrar categoría con más reviews
        categoria_top_reviews = max(resultados, key=lambda x: x['total_reviews'])
        
        estadisticas = {
            "resumen_general": {
                "total_productos": total_productos,
                "total_reviews": total_reviews,
                "precio_promedio_global": round(precio_promedio_global, 2),
                "rating_promedio_global": round(rating_promedio_global, 2),
                "numero_categorias": len(resultados)
            },
            "categoria_mejor_rating": {
                "nombre": categoria_top_rating['categoria'],
                "rating": round(categoria_top_rating['rating_promedio'], 2)
            },
            "categoria_mas_reviews": {
                "nombre": categoria_top_reviews['categoria'],
                "total_reviews": categoria_top_reviews['total_reviews']
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
