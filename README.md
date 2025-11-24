# MapReduce - Análisis de Productos

Proyecto de análisis de datos usando MapReduce con MRJob y FastAPI.

## Requisitos

- Python 3.10 o superior
- PowerShell (Windows)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/AngelMC1/MapReduce.git
cd MapReduce
```

2. Crear y activar entorno virtual:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Instalar dependencias:
```powershell
pip install -r requirements.txt
```

## Ejecución

### Opción 1: Script automático (Recomendado)
```powershell
.\ejecutar_proyecto.ps1
```

### Opción 2: Manual
```powershell
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Ejecutar MapReduce
python mapreduce/job.py dataset/datos.csv

# Los resultados se guardan en resultado.csv
```

### Opción 3: API REST
```powershell
uvicorn api.main:app --reload
```

## Estructura del Proyecto

```
mapreduce/
├── dataset/          # Datos de entrada (JSON y CSV)
├── mapreduce/        # Implementación MapReduce
├── api/              # API REST con FastAPI
├── hdfs/             # Scripts para HDFS/Hadoop
└── resultado.csv     # Salida generada
```

## Resultados

El proyecto genera `resultado.csv` con estadísticas por categoría:
- Número de productos
- Precio promedio
- Rating promedio
- Total de reviews

## Documentación Completa

Ver la wiki para detalles técnicos completos del proyecto.

## Link del Video Sustentacion

https://youtu.be/aoiP-HxSRt0


