import os
import requests
import re

# Création du dossier docs s'il n'existe pas
if not os.path.exists("docs"):
    os.makedirs("docs")

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

print("1. Récupération intégrale de TOUS les comics de 2026 (Pagination active)...")

# Les catégories officielles sur Marvel Database Fandom
categories = [
    "Category:2026_Comic_Books",
    "Category:Comics_released_in_2026",
    "Category:2026_issues"
]

titres_a_importer = set()

for cat in categories:
    cmcontinue = ""
    print(f"Examen de la catégorie : {cat}")
    while True:
        url = f"https://marvel.fandom.com/api.php?action=query&list=categorymembers&cmtitle={cat}&cmlimit=500&format=json"
        if cmcontinue:
            url += f"&cmcontinue={cmcontinue}"
        
        try:
            res = requests.get(url, headers=headers).json()
            query = res.get("query", {})
            members = query.get("categorymembers", [])
            
            for m in members:
                title = m["title"]
                if title and not title.startswith("Category:") and not title.startswith("File:") and not title.startswith("Talk:") and not title.startswith("Template:"):
                    titres_a_importer.add(title)
            
            # Si Fandom indique qu'il y a d'autres pages dans cette catégorie, on continue
            if "continue" in res and "cmcontinue" in res["continue"]:
                cmcontinue = res["continue"]["cmcontinue"]
            else:
                break
        except Exception as e:
            print(f"Erreur sur {cat}: {e}")
            break

print(f"Total cumulé de comics 2026 trouvés : {len(titres_a_importer)}")

print("2. Téléchargement des fiches HTML...")
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

print("3. Génération de la page d'accueil (index.html)...")

fichiers = [f for f in os.listdir("docs") if f.endswith(".html")]
fichiers.sort()

liens_html = ""
for nom_fichier in fichiers:
    nom_lisible = nom_fichier.replace(".html", "").replace("_", " ")
    liens_html += f"        <li class='card'><a href='docs/{nom_fichier}'>{nom_lisible}</a></li>\n"

template_html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Marvel Database - Encyclopédie & Comics</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f0f12; color: #ffffff; margin: 0; padding: 20px; }
        header { text-align: center; padding: 30px 10px; background: #e62429; border-radius: 8px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(230, 36, 41, 0.4); }
        h1 { margin: 0; font-size: 2.5em; text-transform: uppercase; letter-spacing: 2px; }
        p.subtitle { margin-top: 5px; font-weight: 300; opacity: 0.9; }
        .search-box { text-align: center; margin-bottom: 30px; }
        input[type="text"] { width: 80%; max-width: 500px; padding: 12px 20px; font-size: 16px; border-radius: 25px; border: none; outline: none; }
        .ad-space { background: #1a1a24; border: 1px dashed #444; padding: 15px; text-align: center; margin: 20px auto; max-width: 800px; color: #888; border-radius: 6px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; list-style: none; padding: 0; max-width: 1200px; margin: 0 auto; }
        .card { background: #1f1f2e; border-radius: 8px; padding: 15px; transition: transform 0.2s, background 0.2s; border: 1px solid #2d2d3f; }
        .card:hover { transform: translateY(-3px); background: #2a2a3d; border-color: #e62429; }
        .card a { color: #ffffff; text-decoration: none; font-weight: 600; display: block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    </style>
</head>
<body>
    <header>
        <h1>Marvel Database</h1>
        <p class="subtitle">Base de données automatisée des fiches et comics Marvel</p>
    </header>
    <div class="ad-space">
        <p>Espace Publicitaire (AdSense)</p>
    </div>
    <div class="search-box">
        <input type="text" id="searchInput" onkeyup="filterPages()" placeholder="🔍 Rechercher un comic...">
    </div>
    <p style="text-align: center; color: #aaa;">Pages disponibles : <strong>__NB_PAGES__</strong></p>
    <ul class="grid" id="pagesList">
__LIENS_PAGES__
    </ul>
    <div class="ad-space" style="margin-top: 40px;">
        <p>Espace Publicitaire (AdSense)</p>
    </div>
    <script>
        function filterPages() {
            let input = document.getElementById('searchInput').value.toLowerCase();
            let cards = document.getElementsByClassName('card');
            for (let i = 0; i < cards.length; i++) {
                let text = cards[i].innerText.toLowerCase();
                cards[i].style.display = text.includes(input) ? "" : "none";
            }
        }
    </script>
</body>
</html>
"""

final_html = template_html.replace("__NB_PAGES__", str(len(fichiers)))
final_html = final_html.replace("__LIENS_PAGES__", liens_html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("Index.html créé avec succès !")
