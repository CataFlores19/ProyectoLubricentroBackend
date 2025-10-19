"""
Modelo User - Usuarios del sistema (mecánicos, administradores, etc.)
"""
from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class User(db.Model):
    __tablename__ = 'users'
    
    # Primary Key
    ID = Column(Integer, primary_key=True)
    
    # Campos únicos
    RUN = Column(String(20), unique=True, nullable=False)
    Email = Column(String(100), unique=True, nullable=False)
    
    # Información personal
    FirstName = Column(String(50), nullable=False)
    LastName = Column(String(50), nullable=False)
    Password = Column(String(255), nullable=False)
    Phone = Column(String(20), nullable=True)
    
    # Foreign Key
    RoleID = Column(Integer, ForeignKey('roles.ID'), nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    # Relaciones
    role = db.relationship('Role', back_populates='users')
    work_orders = db.relationship('WorkOrder', back_populates='user')
    
    def __repr__(self):
        return f'<User {self.FirstName} {self.LastName}>'