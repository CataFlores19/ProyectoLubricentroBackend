# Lubricentro API - Backend

API REST para un sistema de lubricentro desarrollado con Flask y protegido con JWT.

## Características de Seguridad

- **Autenticación JWT**: Todas las rutas están protegidas con JSON Web Tokens
- **Contraseñas Encriptadas**: Uso de bcrypt para hash de contraseñas
- **CORS**: Configurado para frontend
- **Soft Delete**: Los registros no se eliminan físicamente

## Tecnologías

- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **ORM**: SQLAlchemy
- **Framework**: Flask
- **Autenticación**: Flask-JWT-Extended
- **Seguridad**: Werkzeug Security (password hashing)

## Modelos

- **Client**: Clientes del lubricentro
- **User**: Usuarios del sistema (mecánicos, administradores)
- **Vehicle**: Vehículos de los clientes
- **WorkOrder**: Órdenes de trabajo
- **Role**: Roles de usuarios

## Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
```

2. Activar entorno virtual:
```bash
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno (opcional):
```bash
copy .env.example .env
```
5. Inicializar la base de datos:
```bash
python init_db.py
```

6. Ejecutar la aplicación:
```bash
python app.py
```

## Autenticación

La API usa **JWT (JSON Web Tokens)** para autenticación. 

### Obtener un Token

```http
POST /api/auth/login
Content-Type: application/json

{
  "rut": "12345678-9",
  "password": "password123"
}
```

**Respuesta:**
```json
{
  "success": true,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": { ... }
}
```

### Usar el Token

Incluye el token en el header de cada petición:

```http
Authorization: Bearer <tu_token_aqui>
```

## Endpoints

### Rutas Públicas (No requieren token)

- `GET /` - Mensaje de bienvenida
- `POST /api/auth/login` - Login y obtención de token

### Rutas Protegidas (Requieren token JWT)

#### Autenticación
- `GET /api/auth/me` - Obtener usuario actual

#### Roles
- `GET /api/roles` - Listar todos los roles

#### Clientes
- `GET /api/clients` - Listar todos los clientes
- `POST /api/clients` - Crear un nuevo cliente
- `GET /api/clients/<id>` - Obtener un cliente por ID

#### Usuarios
- `GET /api/users` - Listar todos los usuarios
- `GET /api/users/mechanics` - Listar todos los mecánicos
- `POST /api/users` - Crear un nuevo usuario
- `GET /api/users/<id>` - Obtener un usuario por ID

#### Vehículos
- `GET /api/vehicles` - Listar todos los vehículos
- `POST /api/vehicles` - Crear un nuevo vehículo
- `GET /api/vehicles/<id>` - Obtener un vehículo por ID
- `GET /api/vehicles/client/<client_id>` - Obtener vehículos por cliente

#### Órdenes de Trabajo
- `GET /api/work-orders` - Listar todas las órdenes de trabajo
- `POST /api/work-orders` - Crear una nueva orden de trabajo
- `GET /api/work-orders/<id>` - Obtener una orden por ID
- `GET /api/work-orders/vehicle/<vehicle_id>` - Obtener órdenes por vehículo
- `GET /api/work-orders/user/<user_id>` - Obtener órdenes por usuario/mecánico
