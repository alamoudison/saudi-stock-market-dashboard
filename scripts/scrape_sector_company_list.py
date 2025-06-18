from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os

# Initialize Edge WebDriver
driver = webdriver.Edge()

# Open Saudi Exchange Historical Reports page
url = "https://www.saudiexchange.sa/wps/portal/saudiexchange/newsandreports/reports-publications/historical-reports?locale=en"
driver.get(url)
wait = WebDriverWait(driver, 20)

# Wait for market dropdown and select "Main Market"
wait.until(EC.presence_of_element_located((By.ID, "marketOrIndices")))
Select(driver.find_element(By.ID, "marketOrIndices")).select_by_visible_text("Main Market")
time.sleep(2)

# Set start and end date
# Set start and end date using JavaScript to bypass read-only input
driver.execute_script("document.getElementById('startTimePeriod').value = '01-01-2020';")
driver.execute_script("document.getElementById('endTimePeriod').value = '31-05-2025';")
driver.execute_script("document.getElementById('startTimePeriod').dispatchEvent(new Event('change'))")
driver.execute_script("document.getElementById('endTimePeriod').dispatchEvent(new Event('change'))")
time.sleep(2)


# Output directory
os.makedirs("historical_data", exist_ok=True)

# Loop over sectors
sectors = Select(wait.until(EC.presence_of_element_located((By.ID, "sectors"))))
for i in range(1, len(sectors.options)):  # Skip first (placeholder) option
    sectors.select_by_index(i)
    time.sleep(3)

    # Loop over entities (companies) in this sector
    entities = Select(wait.until(EC.presence_of_element_located((By.ID, "entity"))))
    for j in range(1, len(entities.options)):
        entities.select_by_index(j)
        time.sleep(3)

        # Wait for table data
        time.sleep(4)
        all_rows = []

        while True:
            try:
                table_rows = driver.find_elements(By.XPATH, '//table//tbody//tr')
                for row in table_rows:
                    cols = row.find_elements(By.TAG_NAME, 'td')
                    if cols:
                        all_rows.append([col.text for col in cols])

                # Try clicking "next" page
                next_button = driver.find_element(By.ID, "pageing_next")
                if "disabled" in next_button.get_attribute("class"):
                    break
                next_button.click()
                time.sleep(2)
            except:
                break  # Exit pagination loop

        # Save to CSV
        sector_name = sectors.options[i].text.strip().replace(" ", "_")
        entity_name = entities.options[j].text.strip().replace(" ", "_")
        filename = f"historical_data/{sector_name}_{entity_name}.csv"
        df = pd.DataFrame(all_rows)
        df.to_csv(filename, index=False)
        print(f"Saved: {filename}")

driver.quit()
