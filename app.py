"""
Archivo principal de la aplicación Flask para Lubricentro API
"""
from app import create_app

# Crear instancia de la aplicación
app = create_app()

if __name__ == '__main__':
    # Solo para desarrollo local
    app.run(debug=True)