from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

def get_price_from_auchan(produit, nom=None):
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
        print(f"recherche lancée pour : {produit}")
    except:
        print("barre de recherche non trouvée.")
        driver.quit()
        return "erreur"
    no_result = driver.find_elements(By.CSS_SELECTOR, "img.no-result__image")
    if no_result:
        print("Aucun résultat trouvé avec le code-barres.")
    else:
        try:
            try:
                list_container = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.list__container"))
                )
                first_product = list_container.find_element(By.CSS_SELECTOR, "div.product-price.bolder.text-dark-color")
                price = first_product.text.strip()
            except:
                price = "prix non trouvé"
            driver.quit()
            return price
        except:
            pass

    # test avec le nom
    if nom:
        print(f"aucun résultat pour {produit}, tentative avec : {nom}")
        try:
            search_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input.mainHeaderSearchInput"))
            )
            time.sleep(1.2)
            search_input.click()
            time.sleep(0.5)
            search_input.clear()
            time.sleep(0.5)
            search_input.send_keys(nom)
            search_input.send_keys(Keys.ENTER)
            print(f"recherche lancée pour : {nom}")

            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "img.no-result__image"))
            )
            price = "produit non trouvé"
        except:
            try:
                sort_select = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "sort"))
                )
                select = Select(sort_select)
                select.select_by_value("asc_price_pos")
                time.sleep(1.5)

                list_container = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.list__container"))
                )
                first_product = list_container.find_element(By.CSS_SELECTOR, "div.product-price.bolder.text-dark-color")
                price = first_product.text.strip()
            except:
                price = "prix non trouvé"
    else:
        price = "produit non trouvé"
    driver.quit()
    return price

#print(get_price_from_auchan("5449000147417","coca 20"))