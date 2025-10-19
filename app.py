"""
Archivo principal de la aplicación Flask para Lubricentro API
"""
from app import create_app, db
# Importar modelos para que SQLAlchemy los registre
from app.models import Role, User, Client, Vehicle, WorkOrder

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)