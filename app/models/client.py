"""
Modelo Client - Clientes del lubricentro
"""
from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

class Client(db.Model):
    __tablename__ = 'clients'
    
    # Primary Key
    ID = Column(Integer, primary_key=True)
    
    # Campo único
    RUN = Column(String(20), unique=True, nullable=False)
    
    # Información personal
    FirstName = Column(String(50), nullable=False)
    LastName = Column(String(50), nullable=False)
    Phone = Column(String(20), nullable=True)
    Email = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    # Relaciones
    vehicles = db.relationship('Vehicle', back_populates='client')
    
    def __repr__(self):
        return f'<Client {self.FirstName} {self.LastName}>'