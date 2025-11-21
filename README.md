# 🚀 Proyecto MapReduce con Hadoop y HDFS

Proyecto académico de procesamiento distribuido con **Hadoop MapReduce** y **HDFS**, desarrollado en Python usando **MRJob**. Incluye análisis de datos de productos y una API REST para consultar resultados.

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Requisitos](#-requisitos)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación](#-instalación)
- [Uso del Proyecto](#-uso-del-proyecto)
  - [1. Cargar Datos a HDFS](#1-cargar-datos-a-hdfs)
  - [2. Ejecutar MapReduce](#2-ejecutar-mapreduce)
  - [3. Convertir Resultados](#3-convertir-resultados)
  - [4. Levantar la API](#4-levantar-la-api)
- [Resultados Esperados](#-resultados-esperados)
- [Endpoints de la API](#-endpoints-de-la-api)
- [Troubleshooting](#-troubleshooting)

---

## 📝 Descripción

Este proyecto implementa un pipeline completo de procesamiento distribuido:

1. **Dataset**: Archivo CSV con información de productos (id, nombre, categoría, precio, cantidad)
2. **HDFS**: Sistema de archivos distribuido de Hadoop para almacenar datos
3. **MapReduce**: Job que analiza productos y calcula estadísticas por categoría:
   - Número de productos por categoría
   - Precio promedio por categoría
   - Cantidad total de unidades por categoría
   - Ingresos totales por categoría (precio × cantidad)
4. **API REST**: Servicio FastAPI para consultar los resultados procesados

---

## ✅ Requisitos

### Software Requerido

- **Hadoop** 3.x o superior (con HDFS y YARN configurados)
- **Python** 3.10 o superior
- **Java** 8 u 11 (requerido por Hadoop)

### Variables de Entorno

Asegúrate de tener configuradas las siguientes variables:

```bash
# Ejemplo para Linux/Mac (añadir a ~/.bashrc o ~/.zshrc)
export HADOOP_HOME=/path/to/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
export JAVA_HOME=/path/to/java
```

Para verificar la instalación:

```bash
# Verificar Hadoop
hadoop version

# Verificar HDFS
hdfs dfs -ls /

# Verificar Python
python3 --version
```

---

## 📁 Estructura del Proyecto

```
proyecto-mapreduce/
├── dataset/
│   └── datos.csv              # Dataset de ejemplo con 30 productos
├── hdfs/
│   └── upload_to_hdfs.sh      # Script para subir datos a HDFS
├── mapreduce/
│   └── job.py                 # Job MapReduce con MRJob
├── api/
│   └── main.py                # API REST con FastAPI
├── convert_output.py          # Script para convertir salida de HDFS
├── requirements.txt           # Dependencias de Python
└── README.md                  # Este archivo
```

---

## 🔧 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd proyecto-mapreduce
```

### 2. Crear entorno virtual (recomendado)

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate

# En Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# En Windows (CMD):
.\venv\Scripts\activate.bat
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Verificar instalación de MRJob

```bash
python3 -c "import mrjob; print('MRJob instalado correctamente')"
```

---

## 🚀 Uso del Proyecto

### 1. Cargar Datos a HDFS

Primero, asegúrate de que Hadoop esté corriendo:

```bash
# Iniciar HDFS (si no está corriendo)
start-dfs.sh

# Verificar que funcione
hdfs dfs -ls /
```

Luego, sube el dataset a HDFS:

```bash
cd hdfs
bash upload_to_hdfs.sh
```

**Salida esperada:**
```
=== Iniciando carga de datos a HDFS ===
Verificando conexión con HDFS...
Creando directorio en HDFS: /data/input
Subiendo archivo datos.csv a HDFS...
✓ Archivo subido exitosamente
Ubicación en HDFS: hdfs:///data/input/datos.csv
```

### 2. Ejecutar MapReduce

Ejecuta el job MapReduce usando MRJob con el runner de Hadoop:

```bash
cd mapreduce

# Ejecutar en modo Hadoop (procesamiento distribuido)
python3 job.py -r hadoop hdfs:///data/input/datos.csv -o hdfs:///data/output
```

**Parámetros:**
- `-r hadoop`: Usa el runner de Hadoop (procesamiento distribuido)
- `hdfs:///data/input/datos.csv`: Ruta del archivo de entrada en HDFS
- `-o hdfs:///data/output`: Directorio de salida en HDFS

**Nota:** Si HDFS no está disponible, puedes probar en modo local:

```bash
# Modo local (sin Hadoop, solo para pruebas)
python3 job.py -r local ../dataset/datos.csv -o output_local
```

El job tomará unos momentos para ejecutarse. Verás logs de Hadoop mostrando el progreso.

### 3. Convertir Resultados

Una vez completado el MapReduce, convierte la salida a formato CSV legible:

```bash
cd ..  # Volver al directorio raíz
python3 convert_output.py
```

**Salida esperada:**
```
=== Descarga y conversión de resultados MapReduce ===

Verificando conexión con HDFS...
✓ HDFS disponible

Verificando archivo en HDFS: /data/output/part-00000
✓ Archivo encontrado en HDFS

Descargando /data/output/part-00000...
✓ Archivo descargado desde HDFS: /data/output/part-00000

Convirtiendo a formato CSV...
✓ CSV generado: resultado.csv
  Total de categorías: 3

✓ Archivo temporal eliminado: part-00000

=== Preview de resultados ===
categoria,num_productos,precio_promedio,cantidad_total,ingreso_total
Electronica,19,155.31,1225,105537.55
Iluminacion,6,44.75,432,11865.48
Muebles,5,230.79,132,25398.68

=== Conversión completada exitosamente ===
Archivo generado: resultado.csv
```

### 4. Levantar la API

Inicia el servidor FastAPI para consultar los resultados:

```bash
cd api
python3 main.py
```

O usando uvicorn directamente:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Salida esperada:**
```
=== Iniciando servidor FastAPI ===
Documentación disponible en: http://localhost:8000/docs
API disponible en: http://localhost:8000

INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## 📊 Resultados Esperados

### Archivo `resultado.csv`

```csv
categoria,num_productos,precio_promedio,cantidad_total,ingreso_total
Electronica,19,155.31,1225,105537.55
Iluminacion,6,44.75,432,11865.48
Muebles,5,230.79,132,25398.68
```

### Interpretación

- **Electronica**: 19 productos diferentes, precio promedio de $155.31, total de 1225 unidades, ingresos de $105,537.55
- **Iluminacion**: 6 productos diferentes, precio promedio de $44.75, total de 432 unidades, ingresos de $11,865.48
- **Muebles**: 5 productos diferentes, precio promedio de $230.79, total de 132 unidades, ingresos de $25,398.68

---

## 🌐 Endpoints de la API

Una vez que la API esté corriendo, puedes acceder a:

### 1. **Documentación Interactiva** (Swagger)

```
http://localhost:8000/docs
```

### 2. **GET /** - Información de la API

```bash
curl http://localhost:8000/
```

Respuesta:
```json
{
  "mensaje": "API de Análisis de Productos con MapReduce",
  "version": "1.0.0",
  "endpoints": {
    "/resultados": "GET - Obtener todos los resultados del análisis",
    "/resultados/{categoria}": "GET - Obtener resultados de una categoría específica",
    "/estadisticas": "GET - Obtener estadísticas generales"
  }
}
```

### 3. **GET /resultados** - Todos los resultados

```bash
curl http://localhost:8000/resultados
```

Respuesta:
```json
{
  "total_categorias": 3,
  "resultados": [
    {
      "categoria": "Electronica",
      "num_productos": 19,
      "precio_promedio": 155.31,
      "cantidad_total": 1225,
      "ingreso_total": 105537.55
    },
    ...
  ]
}
```

### 4. **GET /resultados/{categoria}** - Resultado por categoría

```bash
curl http://localhost:8000/resultados/Electronica
```

Respuesta:
```json
{
  "categoria": "Electronica",
  "num_productos": 19,
  "precio_promedio": 155.31,
  "cantidad_total": 1225,
  "ingreso_total": 105537.55
}
```

### 5. **GET /estadisticas** - Estadísticas generales

```bash
curl http://localhost:8000/estadisticas
```

Respuesta:
```json
{
  "resumen_general": {
    "total_productos": 30,
    "total_unidades": 1789,
    "ingresos_totales": 142801.71,
    "precio_promedio_global": 143.62,
    "numero_categorias": 3
  },
  "categoria_top": {
    "nombre": "Electronica",
    "ingresos": 105537.55
  },
  "por_categoria": [...]
}
```

### 6. **GET /health** - Health Check

```bash
curl http://localhost:8000/health
```

Respuesta:
```json
{
  "estado": "activo",
  "servicio": "API MapReduce"
}
```

---

## 🔧 Troubleshooting

### Error: "hdfs: command not found"

**Solución:** Hadoop no está en el PATH. Configura las variables de entorno:

```bash
export HADOOP_HOME=/path/to/hadoop
export PATH=$PATH:$HADOOP_HOME/bin
```

### Error: "Connection refused" al conectar con HDFS

**Solución:** HDFS no está corriendo. Inicia los servicios:

```bash
start-dfs.sh
hdfs dfs -ls /  # Verificar
```

### Error: "No module named 'mrjob'"

**Solución:** Instala las dependencias:

```bash
pip install -r requirements.txt
```

### Error: "File not found: hdfs:///data/output/part-00000"

**Solución:** El job MapReduce no se ejecutó correctamente o no generó salida. Revisa:

1. Que el directorio de salida no exista previamente (Hadoop no sobrescribe)
2. Los logs de Hadoop para ver errores

```bash
# Eliminar directorio de salida anterior
hdfs dfs -rm -r /data/output

# Volver a ejecutar el job
python3 mapreduce/job.py -r hadoop hdfs:///data/input/datos.csv -o hdfs:///data/output
```

### Error: "Archivo de resultados no encontrado" en la API

**Solución:** Ejecuta `convert_output.py` antes de iniciar la API:

```bash
python3 convert_output.py
```

---

## 📚 Referencias

- [Hadoop Documentation](https://hadoop.apache.org/docs/current/)
- [MRJob Documentation](https://mrjob.readthedocs.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

## 👨‍💻 Autor

Proyecto académico - Telemática 2025-2

---

## 📄 Licencia

Este proyecto es de uso académico.
