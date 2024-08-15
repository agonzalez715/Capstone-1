from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate

# db = SQLAlchemy()
from models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)  # Initialize Flask-Migrate

    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

if __name__ == "__main__":
   app = create_app()
   app.run(debug=True)

# app = create_app()
# app.run(debug = True)
