"""
Inicialización de la aplicación Flask
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config.config import Config

# Inicialización de extensiones
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar extensiones
    db.init_app(app)
    CORS(app)
    jwt.init_app(app)
    
    # Registrar blueprints
    from app.routes import main_routes
    app.register_blueprint(main_routes.bp)
    
    return app