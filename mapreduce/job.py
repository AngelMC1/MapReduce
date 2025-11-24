#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MapReduce Job con MRJob para análisis de productos de Fake Store API
Analiza datos de productos y calcula:
- Total de productos por categoría
- Promedio de precio por categoría
- Promedio de rating por categoría
- Total de reviews por categoría
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
import csv


class ProductAnalysisJob(MRJob):
    """
    Job MapReduce para analizar productos por categoría.
    
    Entrada: CSV con columnas: id, title, price, description, category, image, rating_rate, rating_count
    Salida: Estadísticas agregadas por categoría
    """

    def mapper(self, _, line):
        """
        Mapper: Lee cada línea del CSV y emite (categoría, datos del producto)
        
        Args:
            _: Key (ignorada en archivos de texto)
            line: Línea del CSV
            
        Yields:
            (categoria, dict): Tupla con categoría y datos del producto
        """
        try:
            # Limpiar la línea
            line = line.strip()
            if not line or line.startswith('"id"'):
                # Saltar línea vacía o encabezado
                return
            
            # Parsear la línea CSV con RFC 4180 compliance
            reader = csv.reader([line], quotechar='"', doublequote=True)
            row = next(reader)
            
            # Validar que tenga las columnas esperadas (8 columnas)
            if len(row) != 8:
                return
            
            # Extraer datos
            precio = float(row[2])
            categoria = row[4]
            rating_rate = float(row[6])
            rating_count = int(row[7])
            
            # Emitir: key=categoría, value=diccionario con datos
            yield categoria, {
                'precio': precio,
                'rating_rate': rating_rate,
                'rating_count': rating_count,
                'count': 1
            }
            
        except (ValueError, IndexError, TypeError):
            # Ignorar líneas con errores de formato
            pass

    def combiner(self, categoria, valores):
        """
        Combiner: Agrega valores localmente antes de enviar al reducer
        Reduce el tráfico de red al hacer agregación parcial.
        
        Args:
            categoria: Categoría del producto
            valores: Iterador de diccionarios con datos
            
        Yields:
            (categoria, dict): Tupla con categoría y datos agregados
        """
        total_precio = 0
        total_rating = 0
        total_reviews = 0
        count = 0
        
        for valor in valores:
            total_precio += valor['precio']
            total_rating += valor['rating_rate']
            total_reviews += valor['rating_count']
            count += valor['count']
        
        yield categoria, {
            'precio': total_precio,
            'rating_rate': total_rating,
            'rating_count': total_reviews,
            'count': count
        }

    def reducer(self, categoria, valores):
        """
        Reducer: Agrega todos los valores por categoría y calcula estadísticas finales
        
        Args:
            categoria: Categoría del producto
            valores: Iterador de diccionarios con datos agregados
            
        Yields:
            (categoria, str): Tupla con categoría y estadísticas en formato CSV
        """
        total_precio = 0
        total_rating = 0
        total_reviews = 0
        count = 0
        
        # Sumar todos los valores
        for valor in valores:
            total_precio += valor['precio']
            total_rating += valor['rating_rate']
            total_reviews += valor['rating_count']
            count += valor['count']
        
        # Calcular promedios
        precio_promedio = total_precio / count if count > 0 else 0
        rating_promedio = total_rating / count if count > 0 else 0
        
        # Formatear resultado como CSV
        resultado = f"{count},{precio_promedio:.2f},{rating_promedio:.2f},{total_reviews}"
        
        yield categoria, resultado

    def steps(self):
        """
        Define los pasos del job MapReduce.
        
        Returns:
            list: Lista de pasos MRStep
        """
        return [
            MRStep(
                mapper=self.mapper,
                combiner=self.combiner,
                reducer=self.reducer
            )
        ]


if __name__ == '__main__':
    # Ejecutar el job
    ProductAnalysisJob.run()
