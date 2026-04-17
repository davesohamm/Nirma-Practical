from flask import Flask, render_template, request
import pickle
import numpy as np
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://iris_db_cont_2:27017/")
db = client["iris_db"]
collection = db["predictions"]

# Load model
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

        # Store in DB service
        collection.insert_one({
            "sepal_length": sl,
            "sepal_width": sw,
            "petal_length": pl,
            "petal_width": pw,
            "prediction": result
        })

        return render_template("index.html",
                               prediction_text=f"Prediction: {result}")

    except Exception:
        return render_template("index.html",
                               prediction_text="Invalid input")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=False)