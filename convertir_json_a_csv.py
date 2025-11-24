#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para convertir datos.json de Fake Store API a formato CSV
Preserva TODOS los datos del JSON original
"""

import json
import csv

def convertir_json_a_csv():
    """
    Convierte el archivo datos.json a datos.csv
    Preserva todos los campos del JSON
    """
    
    # Leer el JSON
    with open('dataset/datos.json', 'r', encoding='utf-8') as f:
        productos = json.load(f)
    
    print(f" Productos encontrados en JSON: {len(productos)}")
    
    # Crear CSV con TODOS los campos del JSON
    with open('dataset/datos.csv', 'w', newline='', encoding='utf-8') as f:
        # Encabezados: incluye TODOS los campos del JSON
        fieldnames = [
            'id',
            'title',
            'price',
            'description',
            'category',
            'image',
            'rating_rate',
            'rating_count'
        ]
        
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        
        # Escribir cada producto
        for producto in productos:
            writer.writerow({
                'id': producto['id'],
                'title': producto['title'],
                'price': producto['price'],
                'description': producto['description'],
                'category': producto['category'],
                'image': producto['image'],
                'rating_rate': producto['rating']['rate'],
                'rating_count': producto['rating']['count']
            })
    
    print(f" CSV generado exitosamente: dataset/datos.csv")
    print(f" Todos los {len(productos)} productos fueron convertidos")
    print(f" Campos preservados: {', '.join(fieldnames)}")
    
    # Mostrar preview de los primeros 3 productos
    print("\n📊 Preview de los primeros 3 productos:")
    with open('dataset/datos.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= 3:
                break
            print(f"\n  Producto {row['id']}:")
            print(f"    - Título: {row['title'][:50]}...")
            print(f"    - Categoría: {row['category']}")
            print(f"    - Precio: ${row['price']}")
            print(f"    - Rating: {row['rating_rate']} ({row['rating_count']} reviews)")

if __name__ == '__main__':
    convertir_json_a_csv()
