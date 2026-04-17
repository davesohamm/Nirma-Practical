from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import pickle

def load_trained_model(path: str):
    with open(path, "rb") as file:
        return pickle.load(file)

app = Flask(__name__)

model = load_trained_model("model.pkl")

LABELS = {
    0: "Setosa",
    1: "Versicolor",
    2: "Virginica"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def make_prediction():
    try:
        user_input = [
            float(request.form.get("sl")),
            float(request.form.get("sw")),
            float(request.form.get("pl")),
            float(request.form.get("pw"))
        ]

        data = np.array(user_input).reshape(1, -1)
        pred = model.predict(data)[0]

        output = f"Predicted Iris Type: {LABELS.get(pred, 'Unknown')}"
        return render_template("index.html", prediction_text=output)

    except Exception as e:
        return render_template("index.html", prediction_text=f"Error: {str(e)}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)