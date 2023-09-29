from flask import Flask, render_template, request
import re
import pickle
from model_nlp import SentimentClassifier, infer, tokenizer, load_model

checkpoint_path = "phobert_fold5.pth"
n_classes = 7
loaded_model = SentimentClassifier(n_classes)

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("home.html")

@app.route("/upload" , methods = ['POST'])
def upload():
    data = request.get_data()
    decoded_data = data.decode('utf-8')
    load_model(loaded_model ,checkpoint_path)
    result = infer(loaded_model, str(decoded_data), tokenizer)
    return str(result)

if __name__ == "__main__":
    app.run() 