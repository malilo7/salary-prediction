import logging
import webbrowser
from flask import Flask, request, render_template
from joblib import load
from waitress import serve

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
logging.debug("Flask app initialized")

# Load the saved model
model = load("ALLY_DAUDI_MALILO_reg-01493.joblib")
logging.debug("Model loaded successfully")

# Define the home route
@app.route("/", methods=["GET", "POST"])
def index():
    logging.debug("Handling request")
    predicted_salary = None
    if request.method == "POST":
        try:
            # Get user input from the form
            years_of_experience = float(request.form["years_of_experience"])
            logging.debug(f"Received input: {years_of_experience}")
            # Prepare input for prediction
            input_data = [[years_of_experience]]
            logging.debug(f"Input data for model: {input_data}")
            # Make a prediction
            predicted_salary = model.predict(input_data)[0]
            logging.debug(f"Predicted salary: {predicted_salary}")
        except Exception as e:
            predicted_salary = f"Error: {e}"
            logging.error(f"Error occurred: {e}")

    return render_template("index.html", predicted_salary=predicted_salary)

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response


if __name__ == '__main__':
    app.run(debug=True)
    
# Run Flask app with Waitress
if __name__ == "__main__":
    logging.debug("Running Flask app with Waitress")
    # Open a browser tab at the correct address
    webbrowser.open('http://localhost:5000')
    serve(app, host='0.0.0.0', port=5000)
