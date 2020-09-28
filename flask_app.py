from flask import Flask, request, render_template,jsonify
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import re
from numpy import argmax

app = Flask(__name__)
model = AutoModelForSequenceClassification.from_pretrained("model/bart-large-mnli/")
tokenizer = AutoTokenizer.from_pretrained("model/bart-large-mnli/")
zero_shot_classifier = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer)

@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/join', methods=['GET','POST'])
def my_form_post():
    text = request.form['text1']
    labels = request.form['text2']
    labels = labels.split(",")
    results = zero_shot_classifier(text,labels, multi_class=True)
    SCORES = results["scores"]
    CLASSES = results["labels"]
    result = ""
    for scr, cls in zip(SCORES, CLASSES):
        result = result + str(cls) + " (" + str(round(scr, 2)) + "), "
    #BEST_INDEX = argmax(SCORES)
    #predicted_class = CLASSES[BEST_INDEX]
    #predicted_class = " ".join(re.findall("[a-zA-Z]+", predicted_class))
    return result[0:-2]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
