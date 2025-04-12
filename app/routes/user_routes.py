from flask_restx import Namespace, Resource
from flask import request, jsonify
from app.controllers.user_controller import (
    create_user, login_user, get_all_users, get_user_by_id, update_user, delete_user
)

# Crear el Namespace para usuarios
ns = Namespace("users", description="Operaciones con usuarios")

@ns.route('/login')
class Login(Resource):
    def post(self):
        """Iniciar sesión de un usuario"""
        try:
            data = request.json
            if not data:  # Validar si el cuerpo de la solicitud está vacío
                return {"error": "Datos no proporcionados"}, 400
            return login_user(data), 200
        except Exception as e:
            return {"error": str(e)}, 400

@ns.route('/')
class UserList(Resource):
    def get(self):
        """Listar todos los usuarios"""
        try:
            users = get_all_users()
            if not users:  # Validar si no hay usuarios disponibles
                return {"message": "No hay usuarios registrados"}, 404
            return users, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def post(self):
        """Crear un nuevo usuario"""
        try:
            data = request.json
            if not data or not all(key in data for key in ['nombre', 'email', 'password', 'edad']):
                return {"error": "Datos incompletos"}, 400
            return create_user(data), 201
        except Exception as e:
            return {"error": str(e)}, 400

@ns.route('/<int:user_id>')
class User(Resource):
    def get(self, user_id):
        """Obtener información de un usuario por ID"""
        try:
            user = get_user_by_id(user_id)
            if not user:  # Validar si el usuario no existe
                return {"error": "Usuario no encontrado"}, 404
            return user, 200
        except Exception as e:
            return {"error": str(e)}, 404

    def put(self, user_id):
        """Actualizar un usuario existente"""
        try:
            data = request.json
            if not data:
                return {"error": "Datos no proporcionados"}, 400
            return update_user(user_id, data), 200
        except Exception as e:
            return {"error": str(e)}, 400

    def delete(self, user_id):
        """Eliminar un usuario por ID"""
        try:
            user = delete_user(user_id)
            if not user:  # Validar si el usuario no existe o no se pudo eliminar
                return {"error": "Usuario no encontrado o no se pudo eliminar"}, 404
            return {"message": "Usuario eliminado exitosamente"}, 200
        except Exception as e:
            return {"error": str(e)}, 400