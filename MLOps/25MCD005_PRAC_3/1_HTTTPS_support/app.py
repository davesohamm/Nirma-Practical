from flask import Flask, request, render_template, redirect, url_for
import pickle, numpy
from waitress import serve
app = Flask(__name__)
with open("model.pkl", "rb") as file:
    model = pickle.load(file)
@app.route("/")
def welcome():
    return render_template("index.html")
@app.route("/predict", methods=["GET", "POST"])
def make_pred():
    if request.method == "POST":
        pl = float(request.form["petal_length"])
        pw = float(request.form["petal_width"])
        sl = float(request.form["sepal_length"])
        sw = float(request.form["sepal_width"])
        inp = numpy.array([pl, pw, sl, sw])
        reshaped = inp.reshape(1, -1)
        pred = model.predict(reshaped)
        #return str(pred[0])
        return render_template("prediction.html", prediction=pred[0])
    else:
        return redirect(url_for("welcome"))

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=2812, debug=True)
    serve(app=app, host="0.0.0.0", port=2813)