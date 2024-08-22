from app.app import create_app  # Import the create_app function from the app module

# Create an instance of the Flask application by calling the create_app function
app = create_app()

# Entry point of the application
if __name__ == '__main__':
    # Start the Flask application in debug mode
    # Debug mode enables automatic reloading of the server when code changes
    # and provides detailed error messages in the browser
    app.run(debug=True)
