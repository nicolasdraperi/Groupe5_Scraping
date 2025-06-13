from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://www.carrefour.fr/")

try:
    # Attendre la barre de recherche
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "header-search-bar"))
    )
    time.sleep(1.2)
    search_input.click()
    time.sleep(0.5)
    search_input.clear()
    time.sleep(0.5)
    search_input.send_keys("3124480191182")
    time.sleep(0.5)
    search_input.send_keys(Keys.ENTER)
    print("Recherche lancée pour l'article...")

    # Attendre que le bloc contenant le prix apparaisse
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "product-price__amount--main"))
    )

    # Récupérer les parties du prix
    price_container = driver.find_element(By.CLASS_NAME, "product-price__amount--main")
    parts = price_container.find_elements(By.CLASS_NAME, "product-price__content")
    
    # Fusionner les parties pour reconstituer le prix
    full_price = ''.join([part.text.strip() for part in parts])
    print("Prix trouvé :", full_price)

except Exception as e:
    print("Erreur :", e)

input("Appuie sur Entrée pour quitter...")
driver.quit()
