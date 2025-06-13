from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://www.carrefour.fr/")

try:
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
    print("recherche lancée pour item")
except:
    print("barre de recherche non trouvée.")

input("appuie sur Entrée pour quitter...")
driver.quit()
