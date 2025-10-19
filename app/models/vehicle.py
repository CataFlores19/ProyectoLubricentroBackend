"""
Modelo Vehicle - Vehículos de los clientes
"""
from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    
    # Primary Key
    ID = Column(Integer, primary_key=True)
    
    # Campo único
    LicensePlate = Column(String(10), unique=True, nullable=False)
    
    # Información del vehículo
    Color = Column(String(30), nullable=True)
    Brand = Column(String(50), nullable=True)
    Model = Column(String(50), nullable=True)
    Year = Column(Integer, nullable=True)
    
    # Foreign Key
    ClientID = Column(Integer, ForeignKey('clients.ID'), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    # Relaciones
    client = db.relationship('Client', back_populates='vehicles')
    work_orders = db.relationship('WorkOrder', back_populates='vehicle')
    
    def __repr__(self):
        return f'<Vehicle {self.LicensePlate} - {self.Brand} {self.Model}>'