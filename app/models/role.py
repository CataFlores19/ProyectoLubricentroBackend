"""
Modelo Role - Roles de usuarios del sistema
"""
from app import db
from sqlalchemy import Column, Integer, String

class Role(db.Model):
    __tablename__ = 'roles'
    
    # Primary Key
    ID = Column(Integer, primary_key=True)
    
    # Campos
    Name = Column(String(50), unique=True, nullable=False)
    
    # Relaciones (back_populates se definirá en User)
    users = db.relationship('User', back_populates='role')
    
    def __repr__(self):
        return f'<Role {self.Name}>'