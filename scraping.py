from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialisation du navigateur UNE SEULE FOIS
driver = webdriver.Chrome()
driver.get("https://world.openfoodfacts.org/")

def get_barcode(nom_produit):
    try:
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "search_terms"))
        )
        search_input.click()
        time.sleep(0.5)
        search_input.clear()
        time.sleep(0.5)
        search_input.send_keys(nom_produit)
        time.sleep(0.5)
        search_input.send_keys(Keys.ENTER)
        time.sleep(2.5)
        product_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "products_match_all"))
        )
        premier_produit = product_list.find_element(By.TAG_NAME, "li")
        time.sleep(1.2)
        premier_produit.click()
        print(f"produit '{nom_produit}' cliqué")

        barcode_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "barcode"))
        )
        name_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h2.title-1"))
        )
        barcode = barcode_elem.text.strip()
        name_item = name_elem.text.strip()
        driver.get("https://world.openfoodfacts.org/")
        return name_item, barcode

    except Exception as e:
        print(f"Erreur sur '{nom_produit}' : {e}")
        driver.get("https://world.openfoodfacts.org/")
        return None

# boucle des produit
user_input = input("entrez les produits à rechercher (séparés par des virgules) : ")
produits = [p.strip() for p in user_input.split(",") if p.strip()]
for produit in produits:
    name, code = get_barcode(produit)
    print(f"résultat pour '{name}' : {code}\n")

driver.quit()
