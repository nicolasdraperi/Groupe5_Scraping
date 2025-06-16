from scraping import get_barcode
from auchan import get_price_from_auchan
from carrefour import get_price_from_carrefour
from selenium import webdriver
import csv
import os
from datetime import datetime



liste_produits = []

while True:
    nom = input("nom du produit (laisser vide pour lancer la recherche) : ").strip()
    if nom == "":
        break
    try:
        quantite = int(input(f"quantité souhaitée pour '{nom}' : ").strip())
    except:
        print("quantité invalide, on passe à 1 par défaut.")
        quantite = 1
    liste_produits.append((nom, quantite))

driver = webdriver.Chrome()
driver.get("https://world.openfoodfacts.org/")


total_auchan = 0.0
total_carrefour = 0.0
produits_compares = []

print("DEBUT DE LA COMPARAISON")

for produit, qte in liste_produits:
    print(f"\n--- {produit} x{qte} ---")
    nom, barcode = get_barcode(driver, produit)
    if not barcode:
        print(f"echec récupération code-barres pour {produit}.")
        continue

    print(f"Produit : {produit} (code-barres : {barcode})")

    prix_auchan = get_price_from_auchan(barcode, produit)
    prix_carrefour = get_price_from_carrefour(barcode, produit)

    print(f"Auchan → {prix_auchan}")
    print(f"Carrefour → {prix_carrefour}")

    try:
        pa_main, pa_unitaire = [x.strip() for x in prix_auchan.split("|")]
    except:
        pa_main, pa_unitaire = prix_auchan.strip(), "prix unitaire non trouvé"

    try:
        pc_main, pc_unitaire = [x.strip() for x in prix_carrefour.split("|")]
    except:
        pc_main, pc_unitaire = prix_carrefour.strip(), "prix unitaire non trouvé"

    try:
        p_auchan = float(pa_main.replace("€", "").replace(",", "."))
        total_auchan += p_auchan * qte
    except:
        print("prix principal Auchan ignoré")

    try:
        p_carrefour = float(pc_main.replace("€", "").replace(",", "."))
        total_carrefour += p_carrefour * qte
    except:
        print("prix principal Carrefour ignoré")

    produits_compares.append((produit, qte, pa_main, pa_unitaire, pc_main, pc_unitaire))

driver.quit()

print("RÉSUMÉ")
for p, q, pa, pua, pc, puc in produits_compares:
    print(f"\n{p} x{q}")
    print(f"Auchan : {pa} (unitaire : {pua})")
    print(f"Carrefour : {pc} (unitaire : {puc})")

print("\ntotaux :")
print(f"total chez Auchan : {total_auchan:.2f} €")
print(f"total chez Carrefour : {total_carrefour:.2f} €")

if total_auchan < total_carrefour:
    economie = total_carrefour - total_auchan
    print(f"\nvous économisez {economie:.2f} € en allant chez Auchan.")
elif total_carrefour < total_auchan:
    economie = total_auchan - total_carrefour
    print(f"\nvous économisez {economie:.2f} € en allant chez Carrefour.")
else:
    print("\nles deux magasins proposent les mêmes prix.")

print("\ncomparaison terminée.")
dossier = "historique_courses"
os.makedirs(dossier, exist_ok=True)

now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
fichier = f"{dossier}/liste_course_{now}.csv"

with open(fichier, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Nom",
        "Prix unitaire Auchan",
        "Prix/L ou Kg Auchan",
        "Prix unitaire Carrefour",
        "Prix/L ou Kg Carrefour",
        "Quantité",
        "Total",
        "Recommandation"
    ])

    for produit, quantite, p_auchan, pu_auchan, p_carrefour, pu_carrefour in produits_compares:
        try:
            val_auchan = float(p_auchan.replace("€", "").replace(",", "."))
        except:
            val_auchan = 0.0

        try:
            val_carrefour = float(p_carrefour.replace("€", "").replace(",", "."))
        except:
            val_carrefour = 0.0

        total = min(val_auchan, val_carrefour) * quantite

        if val_auchan < val_carrefour:
            reco = "Auchan"
        elif val_carrefour < val_auchan:
            reco = "Carrefour"
        else:
            reco = "Égalité"

        writer.writerow([
            produit,
            p_auchan,
            pu_auchan,
            p_carrefour,
            pu_carrefour,
            quantite,
            f"{total:.2f} €",
            reco
        ])

print(f"\nrésumé exporté dans : {fichier}")