"""
Modelos de la aplicación para el sistema de lubricentro
"""
from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

# Modelo base con timestamps
class BaseModel(db.Model):
    __abstract__ = True
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

# Importar todos los modelos
from .role import Role
from .user import User
from .client import Client
from .vehicle import Vehicle
from .work_order import WorkOrder

__all__ = ['Role', 'User', 'Client', 'Vehicle', 'WorkOrder', 'BaseModel']