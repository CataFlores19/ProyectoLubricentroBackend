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
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'lubricentro.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False