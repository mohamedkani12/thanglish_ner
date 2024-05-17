import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template, request
import spacy
from spacy import displacy
from collections import Counter

app = Flask(__name__)

# Load the custom SpaCy model
nlp = spacy.load(r"D:\Review_NLP\output\model-best")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def process_text():
    text = request.form['text']
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    html = displacy.render(doc, style="ent", page=True)
    
    # Count occurrences of each entity label
    entity_counts = Counter([ent.label_ for ent in doc.ents])
    
    # Extract entity texts for specific labels with given counts
    entity_text_lists = {}
    for label, count in entity_counts.items():
        entity_text_lists[label] = [ent.text for ent in doc.ents if ent.label_ == label]
    
    return render_template('index.html', entities=entities, text=text, html=html, entity_counts=entity_counts, entity_text_lists=entity_text_lists)

if __name__ == '__main__':
    app.run(debug=True)
