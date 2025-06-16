from scraping import get_barcode
from auchan import get_price_from_auchan
from carrefour import get_price_from_carrefour
from selenium import webdriver

user_input = input("Entrez les produits à rechercher (séparés par des virgules) : ")
produits = [p.strip() for p in user_input.split(",") if p.strip()]

driver = webdriver.Chrome()
driver.get("https://world.openfoodfacts.org/")

for produit in produits:
    print("\n---")
    nom, barcode = get_barcode(driver, produit)
    if not barcode:
        print(f"{produit} : échec récupération code-barres.")
        continue

    print(f"Produit demandé : {produit} (code-barres : {barcode})")

    prix_auchan = get_price_from_auchan(barcode, produit)
    prix_carrefour = get_price_from_carrefour(barcode, produit)

    print(f"Prix de {produit} chez Auchan → {prix_auchan}")
    print(f"Prix de {produit} chez Carrefour → {prix_carrefour}")

driver.quit()
