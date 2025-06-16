from scraping import get_barcode
from auchan import get_price_from_auchan
from carrefour import get_price_from_carrefour
from selenium import webdriver

user_input = input("Entrez les produits à rechercher (séparés par des virgules) : ")
produits = [p.strip() for p in user_input.split(",") if p.strip()]

driver = webdriver.Chrome()
driver.get("https://world.openfoodfacts.org/")

total_auchan = 0.0
total_carrefour = 0.0
produits_compares = []

for produit in produits:
    print("\n---")
    nom, barcode = get_barcode(driver, produit)
    if not barcode:
        print(f"{produit} : échec récupération code-barres.")
        continue

    print(f"produit demandé : {produit} (code-barres : {barcode})")

    prix_auchan = get_price_from_auchan(barcode, produit)
    prix_carrefour = get_price_from_carrefour(barcode, produit)

    print(f"prix de {produit} chez Auchan → {prix_auchan}")
    print(f"prix de {produit} chez Carrefour → {prix_carrefour}")

    # Nettoyer les prix pour addition
    try:
        p_auchan = float(prix_auchan.replace("€", "").replace(",", ".").strip())
        total_auchan += p_auchan
    except:
        print("Prix ignoré")

    try:
        p_carrefour = float(prix_carrefour.replace("€", "").replace(",", ".").strip())
        total_carrefour += p_carrefour
    except:
        print("Prix ignoré")

    produits_compares.append(produit)

driver.quit()

print("\n========== Résumé ==========")
print(f"produits comparés : {', '.join(produits_compares)}")
print(f"Total chez Auchan : {total_auchan:.2f} €")
print(f"total chez Carrefour : {total_carrefour:.2f} €")

if total_auchan < total_carrefour:
    economie = total_carrefour - total_auchan
    print(f"vous économisez {economie:.2f} € en allant chez Auchan.")
elif total_carrefour < total_auchan:
    economie = total_auchan - total_carrefour
    print(f"vous économisez {economie:.2f} € en allant chez Carrefour.")
else:
    print("Les deux magasin possede les meme prix")
