from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_price_from_auchan(produit):
    url = "https://www.auchan.fr/magasins/drive/auchan-drive-la-trinite-nice-cote-d-azur/s-869"
    driver = webdriver.Chrome()
    driver.get(url)
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-reject-all-handler"))
        ).click()
    except:
        pass
    try:
        btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.store-info__button"))
        )
        time.sleep(1.2)
        btn.click()
    except:
        print("bouton drive non trouvé.")

    # Recherche du produit
    try:
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.mainHeaderSearchInput"))
        )
        time.sleep(1.2)
        search_input.click()
        time.sleep(0.5)
        search_input.clear()
        time.sleep(0.5)
        search_input.send_keys(produit)
        search_input.send_keys(Keys.ENTER)
        print(f"recherche lancée pour {produit}")
    except:
        print("barre de recherche non trouvée.")
        driver.quit()
        return "erreur"

    # Vérification des résultats
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img.no-result__image"))
        )
        price = "produit non trouvé"
    except:
        try:
            price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-price.bolder.text-dark-color"))
            )
            price = price_element.text.strip()
            print(f"prix détecté : {price}")
        except:
            price = "prix non trouvé"
            print(price)

    driver.quit()
    return price


