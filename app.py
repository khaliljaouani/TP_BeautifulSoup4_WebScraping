from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["bdm_scraper"]
collection = db["articles"]

@app.route('/', methods=['GET', 'POST'])
def index():
    articles = []
    if request.method == 'POST':
        auteur = request.form.get('auteur', '').strip()
        titre = request.form.get('titre', '').strip()
        categorie = request.form.get('categorie', '').strip()
        date_debut = request.form.get('date_debut', '').strip()
        date_fin = request.form.get('date_fin', '').strip()

        query = {}
        if auteur:
            query['auteur'] = {'$regex': auteur, '$options': 'i'}
        if titre:
            query['titre'] = {'$regex': titre, '$options': 'i'}
        if categorie:
            query['categorie'] = {'$regex': categorie, '$options': 'i'}
        if date_debut or date_fin:
            query['date'] = {}
            if date_debut:
                query['date']['$gte'] = date_debut
            if date_fin:
                query['date']['$lte'] = date_fin

        articles = list(collection.find(query).sort("date", -1))

    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
