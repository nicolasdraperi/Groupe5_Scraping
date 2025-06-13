from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://world.openfoodfacts.org/")

search_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "search_terms"))
)

search_input.click()
time.sleep(0.5)
search_input.clear()
time.sleep(0.5)
search_input.send_keys("oasis")
time.sleep(0.5)
search_input.send_keys(Keys.ENTER)
time.sleep(2.5)
product_list = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "products_match_all"))
)

premier_produit = product_list.find_element(By.TAG_NAME, "li")
time.sleep(1.2)
premier_produit.click()

print("produit cliqué avec succès.")

input("appuie sur Entrée pour fermer...")
driver.quit()
