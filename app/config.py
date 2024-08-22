class Config:
    # The SECRET_KEY is used by Flask to securely sign session cookies and other security-related tasks.
    # It should be a random and complex string. In a production environment, it's crucial to keep this key secret.
    SECRET_KEY = 'asdfghjkqwertyui!'  # Replace with a more secure key in a real-world scenario

    # SQLALCHEMY_DATABASE_URI is the connection string for your database.
    # In this case, it's connecting to a PostgreSQL database named 'car'.
    # The format is 'postgresql://username:password@host:port/database_name'.
    SQLALCHEMY_DATABASE_URI = 'postgresql:///car'  # Assumes local PostgreSQL setup with the 'car' database

    # SQLALCHEMY_TRACK_MODIFICATIONS is a setting to disable Flask-SQLAlchemy's event system, 
    # which tracks modifications to objects and emits signals. Disabling it can save memory.
    # It's recommended to set this to False in most applications.
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Improves performance by disabling modification tracking
