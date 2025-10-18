"""
Rutas principales de la API
"""
from flask import Blueprint, request, jsonify
from app import db

bp = Blueprint('main', __name__)



@bp.route('/')
def home():
    """Ruta principal"""
    return jsonify({'message': 'Bienvenido a la API del Lubricentro'})