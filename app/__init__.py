from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restx import Api
from dotenv import load_dotenv
import os

# Cargar las variables de entorno
load_dotenv()

# Instancia global de SQLAlchemy
db = SQLAlchemy()

def create_app():
    """Crea y configura una instancia de Flask."""
    app = Flask(__name__)

    # Configuración de la aplicación desde variables de entorno
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = os.getenv("SECRET_KEY")

    # Inicializar extensiones
    db.init_app(app)
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    # Configuración de Swagger
    api = Api(
        app,
        version="1.0",
        title="Documentación de la API",
        description="API con operaciones de usuario",
        doc="/docs"
    )

    # Registrar el Namespace de usuarios
    from app.routes.user_routes import ns as users_namespace
    api.add_namespace(users_namespace, path="/api/users")

    return app