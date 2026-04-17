from flask import Flask, render_template, request
import pickle
import numpy as np
import requests

app = Flask(__name__)

# DB service URL
DB_URL = "http://iris_db_3:8001/store"

with open("model.pkl", "rb") as file:
    model = pickle.load(file)

class_names = ["setosa", "versicolor", "virginica"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        sl = float(request.form.get("sepal_length"))
        sw = float(request.form.get("sepal_width"))
        pl = float(request.form.get("petal_length"))
        pw = float(request.form.get("petal_width"))

        input_data = np.array([[sl, sw, pl, pw]])
        prediction = model.predict(input_data)[0]
        result = class_names[prediction]

        data = {
            "sepal_length": sl,
            "sepal_width": sw,
            "petal_length": pl,
            "petal_width": pw,
            "prediction": result
        }

        # Send to DB microservice
        requests.post(DB_URL, json=data)

        return render_template("index.html",
                               prediction_text=f"Prediction: {result}")

    except Exception:
        return render_template("index.html",
                               prediction_text="Invalid input")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)