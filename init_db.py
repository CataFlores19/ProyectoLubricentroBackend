"""
Script para inicializar la base de datos y ver las tablas creadas
"""
from app import create_app, db
from app.models import Role, User, Client, Vehicle, WorkOrder
import sqlite3
import os

def init_db():
    app = create_app()
    
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        
        # Crear algunos roles por defecto si no existen
        if not Role.query.first():
            admin_role = Role(Name='Administrador')
            mechanic_role = Role(Name='Mecánico')
            receptionist_role = Role(Name='Recepcionista')
            
            db.session.add(admin_role)
            db.session.add(mechanic_role)
            db.session.add(receptionist_role)
            db.session.commit()


if __name__ == '__main__':
    init_db()