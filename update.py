import os
import requests
import re

# Création du dossier docs s'il n'existe pas
if not os.path.exists("docs"):
    os.makedirs("docs")

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

print("1. Recherche des dernières modifications sur Fandom...")
url_recent = "https://marvel.fandom.com/api.php?action=query&list=recentchanges&rclimit=50&rcnamespace=0&format=json"

titres_a_importer = set()

try:
    res = requests.get(url_recent, headers=headers).json()
    changes = res.get("query", {}).get("recentchanges", [])
    for c in changes:
        title = c.get("title", "")
        if title and not title.startswith("Category:") and not title.startswith("File:") and not title.startswith("Talk:"):
            titres_a_importer.add(title)
except Exception as e:
    print(f"Erreur lors de la récupération : {e}")

print(f"Fiches à télécharger : {len(titres_a_importer)}")

for titre in titres_a_importer:
    url_parse = f"https://marvel.fandom.com/api.php?action=parse&page={titre.replace(' ', '_')}&format=json"
    try:
        res_parse = requests.get(url_parse, headers=headers).json()
        if "parse" in res_parse:
            contenu_html = res_parse["parse"]["text"]["*"]
            contenu_propre = re.sub(r'href="/wiki/', r'href="./', contenu_html)

            nom_clean = re.sub(r'[\\/*?:"<>|]', '_', titre).replace(' ', '_')
            nom_fichier = f"docs/{nom_clean}.html"

            with open(nom_fichier, "w", encoding="utf-8") as f:
                f.write("<!DOCTYPE html><html lang='fr'><head><meta charset='UTF-8'><title>" + titre + "</title><style>body{font-family:sans-serif;padding:20px;max-width:1000px;margin:auto;line-height:1.6;} img{max-width:100%;height:auto;}</style></head><body>")
                f.write("<p><a href='../index.html'>← Retour à l'accueil</a></p>")
                f.write("<h1>" + titre + "</h1>\n")
                f.write(contenu_propre)
                f.write("</body></html>")
    except Exception as e:
        print(f"Erreur sur {titre}: {e}")

print("2. Génération de la page d'accueil (index.html)...")

fichiers = [f for f in os.listdir("docs") if f.endswith(".html")]
fichiers.sort()

with open("index.html", "w", encoding="utf-8") as f:
    f.write("<!DOCTYPE html>\n")
    f.write("<html lang='fr'>\n")
    f.write("<head>\n")
    f.write("    <meta charset='UTF-8'>\n")
    f.write("    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
    f.write("    <title>Marvel Database - Encyclopédie & Comics</title>\n")
    f.write("    <style>\n")
    f.write("        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f0f12; color: #ffffff; margin: 0; padding: 20px; }\n")
    f.write("        header { text-align: center; padding: 30px 10px; background: #e62429; border-radius: 8px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(230, 36, 41, 0.4); }\n")
    f.write("        h1 { margin: 0; font-size: 2.5em; text-transform: uppercase; letter-spacing: 2px; }\n")
    f.write("        p.subtitle { margin-top: 5px; font-weight: 300; opacity: 0.9; }\n")
    f.write("        .search-box { text-align: center; margin-bottom: 30px; }\n")
    f.write("        input[type='text'] { width: 80%; max-width: 500px; padding: 12px 20px; font-size: 16px; border-radius: 25px; border: none; outline: none; }\n")
    f.write("        .ad-space { background: #1a1a24; border: 1px dashed #444; padding: 15px; text-align: center; margin: 20px auto; max-width: 800px; color: #888; border-radius: 6px; }\n")
    f.write("        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; list-style: none; padding: 0; max-width: 1200px; margin: 0 auto; }\n")
    f.write("        .card { background: #1f1f2e; border-radius: 8px; padding: 15px; transition: transform 0.2s, background 0.2s; border: 1px solid #2d2d3f; }\
