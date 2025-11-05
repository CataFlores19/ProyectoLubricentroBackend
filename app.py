"""
Archivo principal de la aplicación Flask para Lubricentro API
"""
from app import create_app, db
# Importar modelos para que SQLAlchemy los registre
from app.models import Role, User, Client, Vehicle, WorkOrder

# Crear instancia de la aplicación
app = create_app()

# Endpoint para inicializar la base de datos (llamar una vez después del deploy)
@app.route('/init-db', methods=['GET', 'POST'])
def init_database():
    try:
        db.create_all()
        return {"message": "Base de datos inicializada correctamente", "success": True}, 200
    except Exception as e:
        return {"message": f"Error al inicializar: {str(e)}", "success": False}, 500

# Endpoint de prueba para verificar que la API funciona
@app.route('/')
def home():
    return {
        "message": "API Lubricentro funcionando correctamente",
        "status": "online",
        "endpoints": {
            "auth": "/api/auth/login, /api/auth/register",
            "roles": "/api/roles",
            "users": "/api/users",
            "init": "/init-db (llamar una vez para crear tablas)"
        }
    }, 200

if __name__ == '__main__':
    app.run(debug=True)