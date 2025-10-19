# Lubricentro API - Backend

API REST simple para un sistema de lubricentro desarrollado con Flask.

## Características

- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **ORM**: SQLAlchemy
- **Framework**: Flask
- **CORS**: Habilitado para frontend

## Modelos


## Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
```

2. Activar entorno virtual:
```bash
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno (opcional):
```bash
copy .env.example .env
```
5. Inicializar la base de datos:
```bash
python init_db.py
```

6. Ejecutar la aplicación:
```bash
python app.py
```

## Endpoints

