import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["bdm_scraper"]
collection = db["articles"]

# Récupérer tous les liens d’articles depuis la page d'accueil
def get_article_links():
    url = "https://www.blogdumoderateur.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    links = set()
    for tag in soup.find_all('a', href=True):
        href = tag['href']
        if href.startswith("https://www.blogdumoderateur.com/") and len(href.split('/')) > 4:
            if not any(x in href for x in ['contact', 'mentions-legales', 'a-propos', 'tools', 'agenda', 'dossier', 'service']):
                links.add(href)
    return list(links)

# Scraper un article
def scrape_article(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        titre = soup.find("h1").text.strip()
        date_tag = soup.find("time")
        date = date_tag["datetime"].split("T")[0] if date_tag else "Inconnue"

        # Trouver l’auteur via les balises <img alt="Nom"> (car c’est souvent dans la photo auteur)
        auteur = "Auteur non trouvé"
        for img in soup.find_all('img', alt=True):
            if "bdm" in img.get('src', '') and len(img['alt'].strip().split()) >= 2:
                auteur = img['alt'].strip()
                break

        # Récupérer le contenu
        contenu_tag = soup.select_one(".post-content")
        contenu = contenu_tag.get_text(separator="\n").strip() if contenu_tag else "Contenu non trouvé"

        # Récupérer les images
        images = []
        if contenu_tag:
            for img in contenu_tag.find_all('img'):
                src = img.get('src') or img.get('data-src')
                alt = img.get('alt') or ''
                if src and not src.startswith("data:"):
                    images.append({"url": src, "alt": alt})

        # Document à enregistrer
        article_data = {
            "url": url,
            "titre": titre,
            "date": date,
            "auteur": auteur,
            "contenu": contenu,
            "images": images
        }

        # Sauvegarde dans MongoDB
        collection.insert_one(article_data)
        print(f"✅ Article sauvegardé : {titre}")
    
    except Exception as e:
        print(f"⚠️ Erreur sur {url} : {e}")

# Lancer le scraper sur plusieurs articles
def run():
    links = get_article_links()
    print(f"\n🔎 {len(links)} articles trouvés.\n")

    for link in links:
        scrape_article(link)
        time.sleep(1)  # petite pause pour être gentil avec le serveur

if __name__ == "__main__":
    run()
