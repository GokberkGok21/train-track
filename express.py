from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from stations import get_tcdd_stations

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://ebilet.tcddtasimacilik.gov.tr/istasyon-tren-danisma")
time.sleep(3)  # Sayfanın yüklenmesini bekle

stations=get_tcdd_stations()

expresses = {}

try:
    for station in stations:
        # Dropdown butonunu bul ve tıkla (Eğer her seferinde kapanıyorsa tekrar açmak gerekebilir)
        dropdown_button = driver.find_element(By.CLASS_NAME, "dropDownInputArea")
        dropdown_button.click()
        time.sleep(1)

        # Açılan input alanını bul ve içine yazı yaz
        input_field = driver.find_element(By.CLASS_NAME, "searchArea")
        input_field.clear()  # Önceki girdiyi temizle
        input_field.send_keys(station)  # Yeni arama terimini yaz
        time.sleep(1)

        # express ismini key saatlerini(dataframe) value olarak alınacak


except Exception as e:
    print("Something went wrong:", e)

driver.quit()

for key, value in expresses.items():
    print(f"Aranan: {key} -> Bulunan: {value}")

