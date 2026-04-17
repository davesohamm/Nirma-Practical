from flask import Flask, render_template, request
import pickle
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load trained model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

# Iris class labels
class_names = ["setosa", "versicolor", "virginica"]

# Home route
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# Prediction route 
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        try:
            # Read form inputs
            sepal_length = float(request.form.get("sepal_length"))
            sepal_width = float(request.form.get("sepal_width"))
            petal_length = float(request.form.get("petal_length"))
            petal_width = float(request.form.get("petal_width"))

            # Prepare input
            input_data = np.array([
                [sepal_length, sepal_width, petal_length, petal_width]
            ])

            # Prediction
            prediction = model.predict(input_data)[0]
            predicted_class = class_names[prediction]

            return render_template(
                "index.html",
                prediction_text=f"Predicted Iris Flower: {predicted_class}"
            )

        except Exception:
            return render_template(
                "index.html",
                prediction_text="Invalid input. Please enter numeric values."
            )

    return render_template("index.html")

# Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=False)