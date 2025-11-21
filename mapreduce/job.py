#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MapReduce Job con MRJob para análisis de productos
Analiza datos de productos y calcula:
- Total de productos por categoría
- Promedio de precio por categoría
- Total de ingresos por categoría (precio * cantidad)
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
import csv


class ProductAnalysisJob(MRJob):
    """
    Job MapReduce para analizar productos por categoría.
    
    Entrada: CSV con columnas: id, producto, categoria, precio, cantidad, fecha
    Salida: Estadísticas agregadas por categoría
    """

    def mapper_init(self):
        """
        Inicializa el mapper.
        Se ejecuta una vez antes de procesar las líneas.
        """
        self.is_header = True

    def mapper(self, _, line):
        """
        Mapper: Lee cada línea del CSV y emite (categoría, datos del producto)
        
        Args:
            _: Key (ignorada en archivos de texto)
            line: Línea del CSV
            
        Yields:
            (categoria, dict): Tupla con categoría y datos del producto
        """
        # Saltar la primera línea (encabezado)
        if self.is_header:
            self.is_header = False
            return
        
        try:
            # Parsear la línea CSV
            reader = csv.reader([line])
            row = next(reader)
            
            # Validar que tenga las columnas esperadas
            if len(row) < 5:
                return
            
            # Extraer datos
            producto_id = row[0]
            producto = row[1]
            categoria = row[2]
            precio = float(row[3])
            cantidad = int(row[4])
            
            # Calcular ingreso total (precio * cantidad)
            ingreso = precio * cantidad
            
            # Emitir: key=categoría, value=diccionario con datos
            yield categoria, {
                'precio': precio,
                'cantidad': cantidad,
                'ingreso': ingreso,
                'count': 1
            }
            
        except (ValueError, IndexError) as e:
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
        total_cantidad = 0
        total_ingreso = 0
        count = 0
        
        for valor in valores:
            total_precio += valor['precio']
            total_cantidad += valor['cantidad']
            total_ingreso += valor['ingreso']
            count += valor['count']
        
        yield categoria, {
            'precio': total_precio,
            'cantidad': total_cantidad,
            'ingreso': total_ingreso,
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
        total_cantidad = 0
        total_ingreso = 0
        count = 0
        
        # Sumar todos los valores
        for valor in valores:
            total_precio += valor['precio']
            total_cantidad += valor['cantidad']
            total_ingreso += valor['ingreso']
            count += valor['count']
        
        # Calcular promedio de precio
        precio_promedio = total_precio / count if count > 0 else 0
        
        # Formatear resultado como CSV
        resultado = f"{count},{precio_promedio:.2f},{total_cantidad},{total_ingreso:.2f}"
        
        yield categoria, resultado

    def steps(self):
        """
        Define los pasos del job MapReduce.
        
        Returns:
            list: Lista de pasos MRStep
        """
        return [
            MRStep(
                mapper_init=self.mapper_init,
                mapper=self.mapper,
                combiner=self.combiner,
                reducer=self.reducer
            )
        ]


if __name__ == '__main__':
    # Ejecutar el job
    ProductAnalysisJob.run()
