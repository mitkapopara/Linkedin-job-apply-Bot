from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchDriverException
import time

EMAIL = ""
PASS = ""
PHONE = ""

service = Service("C:/Users/meet/Desktop/Development/chromedriver.exe")
driver = webdriver.Chrome(service=service)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

driver.get("https://www.linkedin.com/jobs/search/?f_LF=f_AL&geoId=102257491&keywords=python%20developer&location"
           "=London%2C%20England%2C%20United%20Kingdom&redirect=false&position=1&pageNum=0")

sign_in_button = driver.find_element(by="css selector", value=".btn-secondary-emphasis, "
                                                              ".btn-secondary-emphasis:visited, "
                                                              ".btn-secondary-emphasis:focus")
sign_in_button.click()
email = driver.find_element(by="id", value="username")

email.send_keys(EMAIL)
password = driver.find_element(by="id", value="password")
password.send_keys(PASS)
sign_in = driver.find_element(by="css selector", value="button.from__button--floating")
sign_in.click()

time.sleep(2)

all_listings = driver.find_elements(by="css selector", value=".job-card-container--clickable")

for listing in all_listings:
    print("called")
    listing.click()
    time.sleep(1)

    #try to locate the apply button, if can't locate then skip the job.
    try:
        apply_button = driver.find_element(by="css selector", value=".jobs-s-apply button")
        apply_button.click()
        time.sleep(2)

        #If phone field is empty, then fill your phone number.
        phone = driver.find_element(by="css selector", value=".artdeco-text-input--input")
        if phone.text == "":
            phone.send_keys(PHONE)

        submit_button = driver.find_element(by="css selector", value="footer button")

        #if the submit button is a "Next" button, then this is a multistep application, so skip.
        if submit_button.get_attribute("data-control-name") == "continue_unify":
            close_button = driver.find_element(by="class", value="artdeco-modal__dismiss")
            close_button.click()
            time.sleep(2)
            discard_button = driver.find_element(by="class", value="artdeco-modal__confirm-dialog-btn")
            discard_button.click()
            print("Complex application, skipped.")
            continue
        else:
            submit_button.click()

        #Once application completed, close the pop-up window.
        time.sleep(2)
        close_button = driver.find_element(by="css selector", value=".artdeco-button--circle")
        close_button.click()

    #If already applied to job or job is no longer accepting applications, then skip.
    except NoSuchDriverException:
        print("No application button, skipped.")
        continue

time.sleep(3)
driver.quit()
