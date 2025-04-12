from app import create_app, db  # Importar desde __init__.py
from flask_migrate import Migrate

# Crear la aplicación Flask
app = create_app()

# Inicializar Flask-Migrate
migrate = Migrate(app, db)

# Crear las tablas dentro del contexto de la aplicación (solo si no usas migraciones)
with app.app_context():
    db.create_all()  # Esto es opcional si ya tienes configurado Flask-Migrate

if __name__ == "__main__":
    app.run(debug=True, port=3000)