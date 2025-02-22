from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
from stations import get_tcdd_stations


options = webdriver.ChromeOptions()
#options.add_argument("--headless")
options.add_argument("disable-dev-shm-usage")
service=Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://ebilet.tcddtasimacilik.gov.tr/istasyon-tren-danisma")

stations=get_tcdd_stations()
expresses = {}
try:
    for station in stations:
        #station="ADAPAZARI , SAKARYA"
        #SCROLLBAR EKLENECEK
        # Dropdown butonunu bul ve tıkla (Eğer her seferinde kapanıyorsa tekrar açmak gerekebilir)
        dropdown_button = driver.find_element(By.CLASS_NAME,"dropDownInputArea")
        dropdown_button.click()
        #time.sleep(1)

        #Açılan input alanını bul ve içine yazı yaz
        input_field = driver.find_element(By.NAME, "İstasyon")
        time.sleep(1)
        input_field.send_keys(Keys.CONTROL+"a"+Keys.BACKSPACE)
        time.sleep(0.1)
        input_field.send_keys(station+Keys.ARROW_DOWN+Keys.ENTER)
        #time.sleep(1)

        #arama butonuna bas
        sorgula_button=driver.find_element(By.CLASS_NAME,"btnSearch")
        sorgula_button.click()
        time.sleep(1)

        #varış istasyonu:"istasyon" tıkla
        arrival_station_button=driver.find_element(By.ID,"tab-arrivalStation")
        arrival_station_button.click()
        #time.sleep(1)

        #hat bilgisi(for loop koy)
        line_info_buttons=driver.find_elements(By.CLASS_NAME,"btnAdditionalService")
        time.sleep(0.5)
        for line_info_button in line_info_buttons:
            line_info_button.click()
            time.sleep(0.5)

            express_name=driver.find_element(By.CLASS_NAME,"tableSeferInformation").find_element(By.TAG_NAME,"caption").text.strip()


            station_info_table=driver.find_element(By.CLASS_NAME,"tableLineInformation")
            headers_row=station_info_table.find_element(By.TAG_NAME,"thead").find_element(By.TAG_NAME,"tr")
            headers = [header.text.strip() for header in headers_row.find_elements(By.TAG_NAME,"th")]
            rows = station_info_table.find_elements(By.TAG_NAME, "tr")

            data=[]
            for row in rows[1:]:  # Skip header row
                station_name= row.find_element(By.TAG_NAME,"th").text.strip()
                cells = row.find_elements(By.TAG_NAME, "td")
                data.append([station_name]+[cell.text.strip() for cell in cells])

            df = pd.DataFrame(data, columns=headers)
            expresses.update({express_name:df})

            actions = ActionChains(driver)
            #DİNAMİK KAPATMA EKLENECEK
            actions.move_by_offset(10, 10).click().perform()
            time.sleep(0.2)

except Exception as e:
    print("Something went wrong:", e)

driver.quit()

#for key, value in expresses.items():
 #   print(f"Aranan: {key} -> Bulunan: {value}")

