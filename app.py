"""
Archivo principal de la aplicación Flask para Lubricentro API
"""
from app import create_app, db
# Importar modelos para que SQLAlchemy los registre
from app.models import Role, User, Client, Vehicle, WorkOrder

# Crear instancia de la aplicación
app = create_app()

# Crear tablas si no existen (para producción con Neon)
with app.app_context():
    try:
        db.create_all()
        print("✓ Tablas creadas/verificadas exitosamente")
    except Exception as e:
        print(f"⚠ Error al crear tablas: {e}")

if __name__ == '__main__':
    app.run(debug=True)