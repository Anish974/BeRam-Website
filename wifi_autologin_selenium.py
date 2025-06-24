from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time

# Setup Firefox headless mode
options = Options()
options.add_argument('--headless')

driver = webdriver.Firefox(options=options)

def login():
    try:
        driver.get("http://172.16.158.1:1000")
        time.sleep(2)

        # Wait for redirect to login page
        if "login?" in driver.current_url:
            print(f"[*] Reached login page: {driver.current_url}")
            
            # Enter credentials
            username_input = driver.find_element(By.NAME, "username")
            password_input = driver.find_element(By.NAME, "password")
            username_input.send_keys("bhandarkartr")
            password_input.send_keys("Tejas@#05rknec")

            # Submit form
            password_input.submit()

            time.sleep(3)
            page_source = driver.page_source

            if "signed in" in page_source.lower():
                print("[+] Login successful!")
            else:
                print("[!] Login attempt may have failed.")
        else:
            print("[!] Unexpected redirect or already logged in.")

    except Exception as e:
        print(f"[X] Error during login: {e}")
    finally:
        driver.quit()

while True:
    try:
        # Ping to check internet
        import requests
        r = requests.get("http://clients3.google.com/generate_204", timeout=3)
        print("[✓] Already connected. Monitoring...")
    except:
        print("[!] Not connected. Logging in...")
        login()
    time.sleep(60)  # Check every 60 seconds
