import pandas as pd
import datetime as dt
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def read_csv(file_name):
    df = pd.read_csv(file_name)
    return df


def message_formate(name):
    message = """Hello {}, I hope you are doing well!
    This is a test message sent using Python WhatsApp automation.
    Thank you.""".format(name)

    return message

def send_message(driver, phone, message, name, send_hour, send_minute):
    try:
        driver.get(f"https://web.whatsapp.com/send?phone=91{phone}")

        message_box = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, '//footer//div[@contenteditable="true"]')
            )
        )

        message_box.click()
        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)

        print(f"Message process completed for {name}")

    except Exception as e:
        print(f"Error sending to {name}: {e}")


def main():

    file_name = "people_contacts_5.csv"
    data = read_csv(file_name)

    # Use existing Chrome profile
    options = webdriver.ChromeOptions()
    options.add_argument(r"C:\Users\shrey\AppData\Local\Google\Chrome\User Data\Default")
    options.add_argument("profile-directory=Default")
    driver = webdriver.Chrome(options=options)
    driver.get("https://web.whatsapp.com/")

    current_time = dt.datetime.now() + dt.timedelta(minutes=1)
    send_hour = current_time.hour
    send_minute = current_time.minute

    try:

        for index, row in data.iterrows():

            name = row["name"]
            phone = str(row["phone"]).split(".")[0]

            message = message_formate(name)

            print(f"Sending message to {name}...")

            success = send_message(driver, phone, message, name, send_hour, send_minute)

            # Increase scheduled minute by 1
            send_minute += 1

            if send_minute >= 60:
                send_hour += 1
                send_minute = 0

            if send_hour >= 24:
                send_hour = 0

            # Delay before next contact
            time.sleep(15)

    finally:
        # Close browser after all contacts
        driver.quit()


if __name__ == "__main__":
    main()
