"""
Modelo WorkOrder - Órdenes de trabajo del lubricentro
"""
from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Date, ForeignKey

class WorkOrder(db.Model):
    __tablename__ = 'work_orders'
    
    # Primary Key
    ID = Column(Integer, primary_key=True)
    
    # Información de la orden
    OrderDate = Column(Date, nullable=False)
    Status = Column(String(50), nullable=False, default='Pendiente')
    Description = Column(Text, nullable=True)  # Descripción de los servicios
    
    # Foreign Keys
    VehicleID = Column(Integer, ForeignKey('vehicles.ID'), nullable=False)
    UserID = Column(Integer, ForeignKey('users.ID'), nullable=False)  # Mecánico responsable

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    # Relaciones
    vehicle = db.relationship('Vehicle', back_populates='work_orders')
    user = db.relationship('User', back_populates='work_orders')  # Mecánico responsable
    
    def __repr__(self):
        return f'<WorkOrder {self.WorkOrderID} - {self.Status}>'