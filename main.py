from scraping import get_barcode
from auchan import get_price_from_auchan
from selenium import webdriver

user_input = input("entrez les produits à rechercher (séparés par des virgules) : ")
produits = [p.strip() for p in user_input.split(",") if p.strip()]

driver = webdriver.Chrome()

for produit in produits:
    print("\n---")
    name, barcode = get_barcode(driver, produit)
    if not barcode:
        print(f"{produit} : échec récupération code-barres.")
        continue
    print(f"Produit trouvé : {name} (code-barres : {barcode})")

    # Recherche du prix sur Auchan
    prix = get_price_from_auchan(barcode)
    print(f"{name} → {prix}")

driver.quit()
