"""
Script para inicializar la base de datos y ver las tablas creadas
"""
from app import create_app, db
from app.models import Role, User, Client, Vehicle, WorkOrder
from werkzeug.security import generate_password_hash
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
           
        
        # Crear usuario de prueba si no existe
        if not User.query.filter_by(RUN='12345678-9').first():
            # Obtener el rol de Mecánico
            mechanic_role = Role.query.filter_by(Name='Mecánico').first()
            
            test_user = User(
                RUN='12345678-9',
                Email='test@lubricentro.com',
                FirstName='Usuario',
                LastName='Prueba',
                Password=generate_password_hash('password123'),  # Contraseña encriptada
                Phone='+56912345678',
                RoleID=mechanic_role.ID
            )
            
            db.session.add(test_user)
            db.session.commit()
            
            print("✅ Usuario de prueba creado:")
            print(f"   RUT: 12345678-9")
            print(f"   Email: test@lubricentro.com")
            print(f"   Password: password123")
            print(f"   Rol: Mecánico")
        else:
            print("ℹ️  Usuario de prueba ya existe")
        
        print("\n✅ Base de datos inicializada correctamente")


if __name__ == '__main__':
    init_db()