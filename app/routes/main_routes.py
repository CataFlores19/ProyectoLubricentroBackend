"""
Rutas principales de la API
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.client import Client
from app.models.user import User
from app.models.role import Role
from app.models.vehicle import Vehicle
from app.models.work_order import WorkOrder
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

bp = Blueprint('main', __name__)


# ========================================
# RUTA PRINCIPAL
# ========================================

@bp.route('/')
def home():
    """Ruta principal"""
    return jsonify({'message': 'Bienvenido a la API del Lubricentro'})


# ========================================
# RUTAS DE AUTENTICACIÓN
# ========================================

@bp.route('/api/auth/login', methods=['POST'])
def login():
    """
    Endpoint de autenticación - Generar token JWT
    POST /api/auth/login
    Body: {
        "rut": "12345678-9",
        "password": "password123"
    }
    """
    try:
        data = request.get_json()
        
        # Validar que se enviaron los campos requeridos
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se enviaron datos'
            }), 400
            
        # Aceptar tanto 'rut'/'RUN' como 'password'/'Password' (case-insensitive)
        rut = data.get('rut') or data.get('RUN') or data.get('Rut')
        password = data.get('password') or data.get('Password')
        
        if not rut:
            return jsonify({
                'success': False,
                'error': 'El RUT es obligatorio'
            }), 400
            
        if not password:
            return jsonify({
                'success': False,
                'error': 'La contraseña es obligatoria'
            }), 400
        
        # Buscar el usuario por RUT (solo usuarios no eliminados)
        user = User.query.filter_by(RUN=rut, deleted_at=None).first()
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Credenciales inválidas'
            }), 401
        
        # Verificar la contraseña
        if not check_password_hash(user.Password, password):
            return jsonify({
                'success': False,
                'error': 'Credenciales inválidas'
            }), 401
        
        # Crear el token JWT con el ID del usuario (convertido a string)
        access_token = create_access_token(identity=str(user.ID))
        
        # Obtener información del rol
        role_name = user.role.Name if user.role else None
        
        return jsonify({
            'success': True,
            'message': 'Login exitoso',
            'token': access_token,
            'user': {
                'id': user.ID,
                'rut': user.RUN,
                'email': user.Email,
                'firstName': user.FirstName,
                'lastName': user.LastName,
                'roleId': user.RoleID,
                'roleName': role_name
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Obtener información del usuario autenticado (ruta protegida - ejemplo)
    GET /api/auth/me
    Headers: Authorization: Bearer <token>
    """
    try:
        # Obtener el ID del usuario desde el token JWT (convertir a int)
        current_user_id = int(get_jwt_identity())
        
        # Buscar el usuario en la base de datos
        user = User.query.get(current_user_id)
        
        if not user or user.deleted_at is not None:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        # Obtener información del rol
        role_name = user.role.Name if user.role else None
        
        return jsonify({
            'success': True,
            'user': {
                'id': user.ID,
                'rut': user.RUN,
                'email': user.Email,
                'firstName': user.FirstName,
                'lastName': user.LastName,
                'phone': user.Phone,
                'roleId': user.RoleID,
                'roleName': role_name
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ========================================
# RUTAS DE ROLES
# ========================================

@bp.route('/api/roles', methods=['GET'])
@jwt_required()
def get_roles():
    """
    Listar todos los roles (RUTA PROTEGIDA)
    GET /api/roles
    Headers: Authorization: Bearer <token>
    """
    try:
        roles = Role.query.all()
        
        result = []
        for role in roles:
            result.append({
                'ID': role.ID,
                'Name': role.Name
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ========================================
# RUTAS DE CLIENTES
# ========================================

@bp.route('/api/clients', methods=['GET'])
@jwt_required()
def get_clients():
    """
    Listar todos los clientes (excluyendo eliminados) - RUTA PROTEGIDA
    GET /api/clients
    Headers: Authorization: Bearer <token>
    """
    try:
        clients = Client.query.filter(Client.deleted_at.is_(None)).all()
        
        result = []
        for client in clients:
            result.append({
                'ID': client.ID,
                'RUN': client.RUN,
                'FirstName': client.FirstName,
                'LastName': client.LastName,
                'Phone': client.Phone,
                'Email': client.Email,
                'created_at': client.created_at.isoformat() if client.created_at else None,
                'updated_at': client.updated_at.isoformat() if client.updated_at else None
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/api/clients', methods=['POST'])
@jwt_required()
def create_client():
    """
    Crear un nuevo cliente - RUTA PROTEGIDA
    POST /api/clients
    Headers: Authorization: Bearer <token>
    Body: {
        "RUN": "12345678-9",
        "FirstName": "Juan",
        "LastName": "Pérez",
        "Phone": "+56912345678",
        "Email": "juan@example.com"
    }
    """
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if not data.get('RUN'):
            return jsonify({
                'success': False,
                'error': 'El RUN es obligatorio'
            }), 400
            
        if not data.get('FirstName'):
            return jsonify({
                'success': False,
                'error': 'El nombre es obligatorio'
            }), 400
            
        if not data.get('LastName'):
            return jsonify({
                'success': False,
                'error': 'El apellido es obligatorio'
            }), 400
        
        # Verificar si el RUN ya existe
        existing_client = Client.query.filter_by(RUN=data['RUN']).first()
        if existing_client:
            return jsonify({
                'success': False,
                'error': 'Ya existe un cliente con ese RUN'
            }), 400
        
        # Crear nuevo cliente
        new_client = Client(
            RUN=data['RUN'],
            FirstName=data['FirstName'],
            LastName=data['LastName'],
            Phone=data.get('Phone'),
            Email=data.get('Email')
        )
        
        db.session.add(new_client)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cliente creado exitosamente',
            'data': {
                'ID': new_client.ID,
                'RUN': new_client.RUN,
                'FirstName': new_client.FirstName,
                'LastName': new_client.LastName,
                'Phone': new_client.Phone,
                'Email': new_client.Email,
                'created_at': new_client.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/api/clients/<int:client_id>', methods=['GET'])
@jwt_required()
def get_client(client_id):
    """
    Obtener un cliente por ID - RUTA PROTEGIDA
    GET /api/clients/<id>
    Headers: Authorization: Bearer <token>
    """
    try:
        client = Client.query.filter_by(ID=client_id, deleted_at=None).first()
        
        if not client:
            return jsonify({
                'success': False,
                'error': 'Cliente no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'ID': client.ID,
                'RUN': client.RUN,
                'FirstName': client.FirstName,
                'LastName': client.LastName,
                'Phone': client.Phone,
                'Email': client.Email,
                'created_at': client.created_at.isoformat() if client.created_at else None,
                'updated_at': client.updated_at.isoformat() if client.updated_at else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ========================================
# RUTAS DE USUARIOS
# ========================================

@bp.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    """
    Listar todos los usuarios (excluyendo eliminados) - RUTA PROTEGIDA
    GET /api/users
    Headers: Authorization: Bearer <token>
    """
    try:
        users = User.query.filter(User.deleted_at.is_(None)).all()
        
        result = []
        for user in users:
            result.append({
                'ID': user.ID,
                'RUN': user.RUN,
                'Email': user.Email,
                'FirstName': user.FirstName,
                'LastName': user.LastName,
                'Phone': user.Phone,
                'RoleID': user.RoleID,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'updated_at': user.updated_at.isoformat() if user.updated_at else None
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/api/users/mechanics', methods=['GET'])
@jwt_required()
def get_mechanics():
    """
    Listar todos los usuarios con rol de Mecánico (excluyendo eliminados) - RUTA PROTEGIDA
    GET /api/users/mechanics
    Headers: Authorization: Bearer <token>
    """
    try:
        # Buscar el rol de Mecánico
        mechanic_role = Role.query.filter_by(Name='Mecánico').first()
        
        if not mechanic_role:
            return jsonify({
                'success': False,
                'error': 'Rol de Mecánico no encontrado'
            }), 404
        
        # Obtener usuarios con rol de Mecánico
        mechanics = User.query.filter_by(
            RoleID=mechanic_role.ID,
            deleted_at=None
        ).all()
        
        result = []
        for user in mechanics:
            result.append({
                'ID': user.ID,
                'RUN': user.RUN,
                'Email': user.Email,
                'FirstName': user.FirstName,
                'LastName': user.LastName,
                'Phone': user.Phone,
                'RoleID': user.RoleID,
                'RoleName': mechanic_role.Name,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'updated_at': user.updated_at.isoformat() if user.updated_at else None
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/api/users', methods=['POST'])
@jwt_required()
def create_user():
    """
    Crear un nuevo usuario - RUTA PROTEGIDA
    POST /api/users
    Headers: Authorization: Bearer <token>
    Body: {
        "RUN": "12345678-9",
        "Email": "usuario@example.com",
        "FirstName": "Juan",
        "LastName": "Pérez",
        "Password": "password123",
        "Phone": "+56912345678",
        "RoleID": 1
    }
    """
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['RUN', 'Email', 'FirstName', 'LastName', 'Password', 'RoleID']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'El campo {field} es obligatorio'
                }), 400
        
        # Verificar si el RUN ya existe
        existing_user_run = User.query.filter_by(RUN=data['RUN']).first()
        if existing_user_run:
            return jsonify({
                'success': False,
                'error': 'Ya existe un usuario con ese RUN'
            }), 400
        
        # Verificar si el Email ya existe
        existing_user_email = User.query.filter_by(Email=data['Email']).first()
        if existing_user_email:
            return jsonify({
                'success': False,
                'error': 'Ya existe un usuario con ese Email'
            }), 400
        
        # Crear nuevo usuario con password hasheado
        new_user = User(
            RUN=data['RUN'],
            Email=data['Email'],
            FirstName=data['FirstName'],
            LastName=data['LastName'],
            Password=generate_password_hash(data['Password']),
            Phone=data.get('Phone'),
            RoleID=data['RoleID']
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Usuario creado exitosamente',
            'data': {
                'ID': new_user.ID,
                'RUN': new_user.RUN,
                'Email': new_user.Email,
                'FirstName': new_user.FirstName,
                'LastName': new_user.LastName,
                'Phone': new_user.Phone,
                'RoleID': new_user.RoleID,
                'created_at': new_user.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """
    Obtener un usuario por ID - RUTA PROTEGIDA
    GET /api/users/<id>
    Headers: Authorization: Bearer <token>
    """
    try:
        user = User.query.filter_by(ID=user_id, deleted_at=None).first()
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'ID': user.ID,
                'RUN': user.RUN,
                'Email': user.Email,
                'FirstName': user.FirstName,
                'LastName': user.LastName,
                'Phone': user.Phone,
                'RoleID': user.RoleID,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'updated_at': user.updated_at.isoformat() if user.updated_at else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ========================================
# RUTAS DE VEHÍCULOS
# ========================================

@bp.route('/api/vehicles', methods=['GET'])
@jwt_required()
def get_vehicles():
    """
    Listar todos los vehículos (excluyendo eliminados) - RUTA PROTEGIDA
    GET /api/vehicles
    Headers: Authorization: Bearer <token>
    """
    try:
        vehicles = Vehicle.query.filter(Vehicle.deleted_at.is_(None)).all()
        
        result = []
        for vehicle in vehicles:
            # Obtener el nombre completo del cliente
            client_name = f"{vehicle.client.FirstName} {vehicle.client.LastName}" if vehicle.client else None
            
            result.append({
                'ID': vehicle.ID,
                'LicensePlate': vehicle.LicensePlate,
                'Color': vehicle.Color,
                'Brand': vehicle.Brand,
                'Model': vehicle.Model,
                'Year': vehicle.Year,
                'ClientID': vehicle.ClientID,
                'ClientName': client_name,
                'created_at': vehicle.created_at.isoformat() if vehicle.created_at else None,
                'updated_at': vehicle.updated_at.isoformat() if vehicle.updated_at else None
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/api/vehicles', methods=['POST'])
@jwt_required()
def create_vehicle():
    """
    Crear un nuevo vehículo - RUTA PROTEGIDA
    POST /api/vehicles
    Headers: Authorization: Bearer <token>
    Body: {
        "LicensePlate": "ABCD12",
        "Color": "Rojo",
        "Brand": "Toyota",
        "Model": "Corolla",
        "Year": 2020,
        "ClientID": 1
    }
    """
    try:
        data = request.get_json()
        
        # DEBUG: Log de datos recibidos (comentar en producción)
        print("Datos recibidos:", data)
        print("ClientID recibido:", data.get('ClientID'), "Tipo:", type(data.get('ClientID')))
        
        # Validar campos requeridos
        if not data.get('LicensePlate'):
            return jsonify({
                'success': False,
                'error': 'La patente es obligatoria'
            }), 400
            
        # Validar ClientID - verificar que no sea None, null o vacío
        client_id = data.get('ClientID')
        if client_id is None or client_id == '':
            return jsonify({
                'success': False,
                'error': 'El ID del cliente es obligatorio y no puede ser nulo',
                'received_data': {
                    'ClientID': client_id,
                    'type': str(type(client_id))
                }
            }), 400
        
        # Verificar que el cliente exista
        client = Client.query.filter_by(ID=client_id, deleted_at=None).first()
        if not client:
            return jsonify({
                'success': False,
                'error': f'No existe un cliente con ID {client_id}'
            }), 404
        
        # Verificar si la patente ya existe
        existing_vehicle = Vehicle.query.filter_by(LicensePlate=data['LicensePlate']).first()
        if existing_vehicle:
            return jsonify({
                'success': False,
                'error': 'Ya existe un vehículo con esa patente'
            }), 400
        
        # Crear nuevo vehículo
        new_vehicle = Vehicle(
            LicensePlate=data['LicensePlate'],
            Color=data.get('Color'),
            Brand=data.get('Brand'),
            Model=data.get('Model'),
            Year=data.get('Year'),
            ClientID=data['ClientID']
        )
        
        db.session.add(new_vehicle)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Vehículo creado exitosamente',
            'data': {
                'ID': new_vehicle.ID,
                'LicensePlate': new_vehicle.LicensePlate,
                'Color': new_vehicle.Color,
                'Brand': new_vehicle.Brand,
                'Model': new_vehicle.Model,
                'Year': new_vehicle.Year,
                'ClientID': new_vehicle.ClientID,
                'created_at': new_vehicle.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/api/vehicles/<int:vehicle_id>', methods=['GET'])
@jwt_required()
def get_vehicle(vehicle_id):
    """
    Obtener un vehículo por ID - RUTA PROTEGIDA
    GET /api/vehicles/<id>
    Headers: Authorization: Bearer <token>
    """
    try:
        vehicle = Vehicle.query.filter_by(ID=vehicle_id, deleted_at=None).first()
        
        if not vehicle:
            return jsonify({
                'success': False,
                'error': 'Vehículo no encontrado'
            }), 404
        
        # Obtener el nombre completo del cliente
        client_name = f"{vehicle.client.FirstName} {vehicle.client.LastName}" if vehicle.client else None
        
        return jsonify({
            'success': True,
            'data': {
                'ID': vehicle.ID,
                'LicensePlate': vehicle.LicensePlate,
                'Color': vehicle.Color,
                'Brand': vehicle.Brand,
                'Model': vehicle.Model,
                'Year': vehicle.Year,
                'ClientID': vehicle.ClientID,
                'ClientName': client_name,
                'created_at': vehicle.created_at.isoformat() if vehicle.created_at else None,
                'updated_at': vehicle.updated_at.isoformat() if vehicle.updated_at else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/api/vehicles/client/<int:client_id>', methods=['GET'])
@jwt_required()
def get_vehicles_by_client(client_id):
    """
    Obtener todos los vehículos de un cliente - RUTA PROTEGIDA
    GET /api/vehicles/client/<client_id>
    Headers: Authorization: Bearer <token>
    """
    try:
        vehicles = Vehicle.query.filter_by(ClientID=client_id, deleted_at=None).all()
        
        result = []
        for vehicle in vehicles:
            # Obtener el nombre completo del cliente
            client_name = f"{vehicle.client.FirstName} {vehicle.client.LastName}" if vehicle.client else None
            
            result.append({
                'ID': vehicle.ID,
                'LicensePlate': vehicle.LicensePlate,
                'Color': vehicle.Color,
                'Brand': vehicle.Brand,
                'Model': vehicle.Model,
                'Year': vehicle.Year,
                'ClientID': vehicle.ClientID,
                'ClientName': client_name,
                'created_at': vehicle.created_at.isoformat() if vehicle.created_at else None,
                'updated_at': vehicle.updated_at.isoformat() if vehicle.updated_at else None
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ========================================
# RUTAS DE ÓRDENES DE TRABAJO
# ========================================

@bp.route('/api/work-orders', methods=['GET'])
@jwt_required()
def get_work_orders():
    """
    Listar todas las órdenes de trabajo (excluyendo eliminadas) - RUTA PROTEGIDA
    GET /api/work-orders
    Headers: Authorization: Bearer <token>
    """
    try:
        work_orders = WorkOrder.query.filter(WorkOrder.deleted_at.is_(None)).all()
        
        result = []
        for order in work_orders:
            # Obtener la patente del vehículo
            license_plate = order.vehicle.LicensePlate if order.vehicle else None
            
            # Obtener el nombre del técnico/mecánico
            technician_name = f"{order.user.FirstName} {order.user.LastName}" if order.user else None
            
            result.append({
                'ID': order.ID,
                'OrderDate': order.OrderDate.isoformat() if order.OrderDate else None,
                'Status': order.Status,
                'Description': order.Description,
                'VehicleID': order.VehicleID,
                'LicensePlate': license_plate,
                'UserID': order.UserID,
                'TechnicianName': technician_name,
                'created_at': order.created_at.isoformat() if order.created_at else None,
                'updated_at': order.updated_at.isoformat() if order.updated_at else None
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/api/work-orders', methods=['POST'])
@jwt_required()
def create_work_order():
    """
    Crear una nueva orden de trabajo - RUTA PROTEGIDA
    POST /api/work-orders
    Headers: Authorization: Bearer <token>
    Body: {
        "OrderDate": "2024-10-26",
        "Status": "Pendiente",
        "Description": "Cambio de aceite y filtro",
        "VehicleID": 1,
        "UserID": 1
    }
    """
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['OrderDate', 'VehicleID', 'UserID']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'El campo {field} es obligatorio'
                }), 400
        
        # Convertir fecha si viene como string
        order_date = data['OrderDate']
        if isinstance(order_date, str):
            try:
                order_date = datetime.strptime(order_date, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Formato de fecha inválido. Use YYYY-MM-DD'
                }), 400
        
        # Crear nueva orden de trabajo
        new_order = WorkOrder(
            OrderDate=order_date,
            Status=data.get('Status', 'Pendiente'),
            Description=data.get('Description'),
            VehicleID=data['VehicleID'],
            UserID=data['UserID']
        )
        
        db.session.add(new_order)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Orden de trabajo creada exitosamente',
            'data': {
                'ID': new_order.ID,
                'OrderDate': new_order.OrderDate.isoformat() if new_order.OrderDate else None,
                'Status': new_order.Status,
                'Description': new_order.Description,
                'VehicleID': new_order.VehicleID,
                'UserID': new_order.UserID,
                'created_at': new_order.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/api/work-orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_work_order(order_id):
    """
    Obtener una orden de trabajo por ID - RUTA PROTEGIDA
    GET /api/work-orders/<id>
    Headers: Authorization: Bearer <token>
    """
    try:
        order = WorkOrder.query.filter_by(ID=order_id, deleted_at=None).first()
        
        if not order:
            return jsonify({
                'success': False,
                'error': 'Orden de trabajo no encontrada'
            }), 404
        
        # Obtener la patente del vehículo
        license_plate = order.vehicle.LicensePlate if order.vehicle else None
        
        # Obtener el nombre del técnico/mecánico
        technician_name = f"{order.user.FirstName} {order.user.LastName}" if order.user else None
        
        return jsonify({
            'success': True,
            'data': {
                'ID': order.ID,
                'OrderDate': order.OrderDate.isoformat() if order.OrderDate else None,
                'Status': order.Status,
                'Description': order.Description,
                'VehicleID': order.VehicleID,
                'LicensePlate': license_plate,
                'UserID': order.UserID,
                'TechnicianName': technician_name,
                'created_at': order.created_at.isoformat() if order.created_at else None,
                'updated_at': order.updated_at.isoformat() if order.updated_at else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/api/work-orders/vehicle/<int:vehicle_id>', methods=['GET'])
@jwt_required()
def get_work_orders_by_vehicle(vehicle_id):
    """
    Obtener todas las órdenes de trabajo de un vehículo - RUTA PROTEGIDA
    GET /api/work-orders/vehicle/<vehicle_id>
    Headers: Authorization: Bearer <token>
    """
    try:
        orders = WorkOrder.query.filter_by(VehicleID=vehicle_id, deleted_at=None).all()
        
        result = []
        for order in orders:
            # Obtener la patente del vehículo
            license_plate = order.vehicle.LicensePlate if order.vehicle else None
            
            # Obtener el nombre del técnico/mecánico
            technician_name = f"{order.user.FirstName} {order.user.LastName}" if order.user else None
            
            result.append({
                'ID': order.ID,
                'OrderDate': order.OrderDate.isoformat() if order.OrderDate else None,
                'Status': order.Status,
                'Description': order.Description,
                'VehicleID': order.VehicleID,
                'LicensePlate': license_plate,
                'UserID': order.UserID,
                'TechnicianName': technician_name,
                'created_at': order.created_at.isoformat() if order.created_at else None,
                'updated_at': order.updated_at.isoformat() if order.updated_at else None
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/api/work-orders/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_work_orders_by_user(user_id):
    """
    Obtener todas las órdenes de trabajo asignadas a un usuario (mecánico) - RUTA PROTEGIDA
    GET /api/work-orders/user/<user_id>
    Headers: Authorization: Bearer <token>
    """
    try:
        orders = WorkOrder.query.filter_by(UserID=user_id, deleted_at=None).all()
        
        result = []
        for order in orders:
            # Obtener la patente del vehículo
            license_plate = order.vehicle.LicensePlate if order.vehicle else None
            
            # Obtener el nombre del técnico/mecánico
            technician_name = f"{order.user.FirstName} {order.user.LastName}" if order.user else None
            
            result.append({
                'ID': order.ID,
                'OrderDate': order.OrderDate.isoformat() if order.OrderDate else None,
                'Status': order.Status,
                'Description': order.Description,
                'VehicleID': order.VehicleID,
                'LicensePlate': license_plate,
                'UserID': order.UserID,
                'TechnicianName': technician_name,
                'created_at': order.created_at.isoformat() if order.created_at else None,
                'updated_at': order.updated_at.isoformat() if order.updated_at else None
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500