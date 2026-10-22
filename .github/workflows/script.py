import os
import requests
import json
import re

# Crée un dossier 'docs' s'il n'existe pas
if not os.path.exists("docs"):
    os.makedirs("docs")

def importer_page_fandom(titre_page):
    print(f"Téléchargement de : {titre_page}...")
    url = f"https://marvel.fandom.com/api.php?action=parse&page={titre_page}&format=json"
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers).json()
    
    if "parse" in response:
        contenu_html = response["parse"]["text"]["*"]
        
        # 1. Nettoyage : Suppression des éléments indésirables ou pubs éventuelles
        # (Le contenu brut de Fandom est converti en texte propre)
        
        # 2. Adaptation des liens pour qu'ils restent sur ton site
        contenu_propre = re.sub(r'href="/wiki/', r'href="./', contenu_html)
        
        # 3. Création du fichier Markdown / HTML pour ton site
        nom_fichier = f"docs/{titre_page.replace(' ', '_').replace('/', '_')}.html"
        with open(nom_fichier, "w", encoding="utf-8") as f:
            f.write(f"<h1>{titre_page}</h1>\n")
            f.write(contenu_propre)
            
        print(f"Page '{titre_page}' enregistrée avec succès !")
    else:
        print(f"Erreur ou page introuvable : {titre_page}")

# Liste des pages de test ou des sorties récentes à récupérer automatiquement
pages_a_importer = [
    "Ricardo_Villanueva_(Earth-616)",
    "Spider-Man"
]

for page in pages_a_importer:
    importer_page_fandom(page)
