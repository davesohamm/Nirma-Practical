from flask import Flask, request, jsonify
import pickle
import numpy as np
from waitress import serve

app = Flask(__name__)

with open("model.pkl", "rb") as file:
    model = pickle.load(file)


@app.route("/predict", methods=["POST"])
def make_pred():
    data = request.json

    pl = float(data["petal_length"])
    pw = float(data["petal_width"])
    sl = float(data["sepal_length"])
    sw = float(data["sepal_width"])

    inp = np.array([pl, pw, sl, sw]).reshape(1, -1)
    pred = model.predict(inp)

    return jsonify({"prediction": int(pred[0])})


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=2813)