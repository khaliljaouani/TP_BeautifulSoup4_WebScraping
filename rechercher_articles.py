from pymongo import MongoClient
from datetime import datetime

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["bdm_scraper"]
collection = db["articles"]

# 🔍 Fonction pour rechercher dans MongoDB
def rechercher_articles(auteur=None, mot_cle=None, date_debut=None, date_fin=None):
    query = {}

    if auteur:
        query["auteur"] = {"$regex": auteur, "$options": "i"}  # insensitive

    if mot_cle:
        query["titre"] = {"$regex": mot_cle, "$options": "i"}

    if date_debut or date_fin:
        date_filter = {}
        if date_debut:
            date_filter["$gte"] = date_debut
        if date_fin:
            date_filter["$lte"] = date_fin
        query["date"] = date_filter

    resultats = list(collection.find(query).sort("date", -1))

    print(f"\n🔎 {len(resultats)} article(s) trouvé(s) :\n")
    for article in resultats:
        print(f"📝 Titre   : {article.get('titre', 'N/A')}")
        print(f"📅 Date    : {article.get('date', 'N/A')}")
        print(f"✍️ Auteur  : {article.get('auteur', 'N/A')}")
        print(f"🔗 Lien    : {article.get('url', '')}")
        print("-" * 60)

# 🔁 Interface utilisateur console
def menu_recherche():
    while True:
        print("\n🔍 MOTEUR DE RECHERCHE BDM (console)")
        auteur = input("Auteur (laisser vide si aucun filtre) : ").strip()
        mot_cle = input("Mot-clé dans le titre : ").strip()
        date_debut = input("Date début (AAAA-MM-JJ) : ").strip()
        date_fin = input("Date fin   (AAAA-MM-JJ) : ").strip()

        # Nettoyer les champs vides
        auteur = auteur if auteur else None
        mot_cle = mot_cle if mot_cle else None
        date_debut = date_debut if date_debut else None
        date_fin = date_fin if date_fin else None

        # Lancer la recherche
        rechercher_articles(auteur, mot_cle, date_debut, date_fin)

        # Continuer ?
        again = input("\nSouhaitez-vous faire une autre recherche ? (o/n) : ").lower()
        if again != "o":
            print("👋 Fin du moteur de recherche.")
            break

# ▶️ Lancer le programme
if __name__ == "__main__":
    menu_recherche()
