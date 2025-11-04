"""
Configuración simple de la aplicación Flask
"""
import os

class Config:
    """Configuración básica"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-para-desarrollo'
    
    # Configuración JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-super-segura-cambiar-en-produccion'
    
    # Base de datos - SQLite por defecto, PostgreSQL si está configurado
    # Vercel/Neon usa DATABASE_URL o POSTGRES_URL
    DATABASE_URL = os.environ.get('DATABASE_URL') or os.environ.get('POSTGRES_URL')
    
    if DATABASE_URL:
        # Fix para Vercel/Neon: convertir postgres:// a postgresql://
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'lubricentro.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }