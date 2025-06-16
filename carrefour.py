from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_price_from_carrefour(produit, nom=None):
    driver = webdriver.Chrome()
    driver.get("https://www.carrefour.fr/")

    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-reject-all-handler"))
        ).click()
    except:
        pass

    try:
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "header-search-bar"))
        )
        time.sleep(1.2)
        search_input.click()
        time.sleep(0.5)
        search_input.clear()
        time.sleep(0.5)
        search_input.send_keys(produit)
        time.sleep(0.5)
        search_input.send_keys(Keys.ENTER)
        print(f"recherche lancée pour : {produit}")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "data-plp_produits"))
        )
        ul = driver.find_element(By.ID, "data-plp_produits")
        items = ul.find_elements(By.CLASS_NAME, "product-list-grid__item")

        premier_article_valide = None
        for item in items:
            try:
                item.find_element(By.CLASS_NAME, "advertising-placeholder-flagship")
                continue
            except:
                premier_article_valide = item
                break

        if premier_article_valide:
            price_container = premier_article_valide.find_element(By.CLASS_NAME, "product-price__amount--main")
            parts = price_container.find_elements(By.CLASS_NAME, "product-price__content")
            prix = ''.join([part.text.strip() for part in parts])
            try:
                price_per_unit_span = premier_article_valide.find_element(
                    By.CSS_SELECTOR,
                    "span.product-list-card-plp-grid__per-unit-label"
                )
                prix_unitaire = price_per_unit_span.text.strip()
            except:
                prix_unitaire = "prix unitaire non trouvé"

            prix = f"{prix} | {prix_unitaire}"
        else:
            prix = "aucun article non sponsorisé trouvé"

    except:
        if nom:
            print(f"aucun résultat avec le code-barres. Nouvelle tentative avec : {nom}")
            try:
                driver.get("https://www.carrefour.fr/")
                search_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "header-search-bar"))
                )
                time.sleep(1.2)
                search_input.click()
                time.sleep(0.5)
                search_input.clear()
                time.sleep(0.5)
                search_input.send_keys(nom)
                time.sleep(0.5)
                search_input.send_keys(Keys.ENTER)
                print(f"recherche lancée pour : {nom}")

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "data-plp_produits"))
                )
                ul = driver.find_element(By.ID, "data-plp_produits")
                items = ul.find_elements(By.CLASS_NAME, "product-list-grid__item")

                premier_article_valide = None
                for item in items:
                    try:
                        item.find_element(By.CLASS_NAME, "advertising-placeholder-flagship")
                        continue
                    except:
                        premier_article_valide = item
                        break

                if premier_article_valide:
                    price_container = premier_article_valide.find_element(By.CLASS_NAME, "product-price__amount--main")
                    parts = price_container.find_elements(By.CLASS_NAME, "product-price__content")
                    prix = ''.join([part.text.strip() for part in parts])

                    try:
                        price_per_unit_span = premier_article_valide.find_element(
                            By.CSS_SELECTOR,
                            "span.product-list-card-plp-grid__per-unit-label"
                        )
                        prix_unitaire = price_per_unit_span.text.strip()
                    except:
                        prix_unitaire = "prix unitaire non trouvé"

                    prix = f"{prix} | {prix_unitaire}"
                else:
                    prix = "aucun article non sponsorisé trouvé"
            except:
                prix = "produit non trouvé"
        else:
            prix = "produit non trouvé"

    driver.quit()
    return prix

#print(get_price_from_carrefour("5449000147417", "coca"))
