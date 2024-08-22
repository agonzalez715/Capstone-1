from flask import Flask, render_template  # Import Flask class and render_template function from flask module

# Create an instance of the Flask class.
# __name__ is a special variable in Python that is set to the name of the current module.
# Flask uses it to determine the root path of the application.
app = Flask(__name__)

# Define a route for the root URL ("/").
# A route is a URL pattern that is mapped to a specific function.
# The function will be called whenever a user visits the specified route.
@app.route("/")  # The @app.route("/") decorator associates this route with the home() function.
def home():  # Define the home() function, which is executed when the root URL is accessed.
    return render_template("home.html")  # The render_template function loads the HTML file from the templates folder.

# The following block ensures that the app runs only if this script is executed directly, not when imported as a module.
if __name__ == "__main__":  # Check if the script is being run directly (not imported).
    app.run(debug=True)  # Start the Flask web server in debug mode. Debug mode provides detailed error messages and automatically restarts the server when code changes are detected.
