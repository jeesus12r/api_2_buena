from app.models.user_model import User
from app import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def create_user(data):
    if not all(key in data for key in ["nombre", "email", "password", "edad"]):
        return {"error": "Faltan campos obligatorios en la solicitud"}, 400

    # Validación de tipo de edad
    try:
        edad = int(data['edad'])
        if edad <= 0:
            return {"error": "La edad debe ser un número positivo"}, 400
    except ValueError:
        return {"error": "La edad debe ser un número válido"}, 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(
        nombre=data['nombre'],
        email=data['email'],
        password=hashed_password,
        edad=edad
    )
    db.session.add(new_user)
    db.session.commit()
    return {"message": "Usuario creado exitosamente"}, 201

def login_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        return {"message": f"¡Bienvenido, {user.nombre}!"}
    return {"error": "Credenciales inválidas"}

def get_all_users():
    users = User.query.all()
    return [user.to_dict() for user in users]

def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": f"Usuario con ID {user_id} no encontrado"}
    return user.to_dict()

def update_user(user_id, data):
    user = User.query.get(user_id)
    if not user:
        return {"error": f"Usuario con ID {user_id} no encontrado"}
    user.nombre = data.get('nombre', user.nombre)
    user.email = data.get('email', user.email)
    user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8') if 'password' in data else user.password
    user.edad = data.get('edad', user.edad)
    db.session.commit()
    return {"message": "Usuario actualizado exitosamente"}

def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": f"Usuario con ID {user_id} no encontrado"}
    db.session.delete(user)
    db.session.commit()
    return {"message": "Usuario eliminado exitosamente"}