from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


def get_tcdd_stations():
    options = Options()
    options.add_argument("--headless")  # Tarayıcıyı arka planda çalıştır
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = "https://ebilet.tcddtasimacilik.gov.tr/"
    driver.get(url)

    try:
        # Açılır menüyü açmak için ilgili butona tıklama
        dropdown_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "dropDownInputArea"))
        )
        dropdown_button.click()
        time.sleep(2)  # Menü açılmasını bekle

        # İstasyonları çek
        station_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".textLocation"))
        )

        stations = [station.text.strip() for station in station_elements if station.text.strip()]

    except Exception as e:
        print("Something went wrong:", e)
        stations = []

    driver.quit()
    return stations

