"""
Archivo API simplificado para Vercel
Este archivo maneja las peticiones serverless en Vercel
"""
from app import create_app

# Crear la app
app = create_app()

# Este será el handler de Vercel
# Vercel lo llama automáticamente
