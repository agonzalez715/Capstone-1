from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate

# db = SQLAlchemy()
from models import db

def create_app():
    # Create a Flask application instance
    app = Flask(__name__)

    # Load configuration settings from the Config class in config.py
    app.config.from_object(Config)

    # Initialize the SQLAlchemy database instance with the app
    db.init_app(app)

    # Initialize Flask-Migrate to handle database migrations
    migrate = Migrate(app, db)  # Initialize Flask-Migrate

    # Import and register the main Blueprint from routes.py
    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Return the Flask app instance
    return app

# This block ensures the app runs only if the script is executed directly (not imported)
if __name__ == "__main__":
    # Create the Flask app instance
    app = create_app()
    
    # Run the Flask app with debug mode enabled
    app.run(debug=True)

# app = create_app()
# app.run(debug = True)  # Commented-out alternative way to run the app, likely for testing different configurations
