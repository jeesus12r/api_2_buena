from app import create_app, db  # Importa desde __init__.py, no desde config.py

app = create_app()

# Crear las tablas dentro del contexto de la aplicación
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=3000)