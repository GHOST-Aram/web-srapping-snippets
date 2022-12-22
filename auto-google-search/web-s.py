from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

driver.get('https://google.com')

textbox = driver.find_element(By.CSS_SELECTOR, 'input.gLFyf')
textbox.send_keys('Selenium')
textbox.send_keys(Keys.RETURN)
def collect_sources():
    while True:
        headings = driver.find_elements(By.TAG_NAME, 'h3')
        cites = driver.find_elements(By.TAG_NAME, 'cite')
        
        with open('sources.txt', 'a') as sources:
            for i in range(len(headings)):
                sources.write(f'{headings[i].text}\n')
                sources.write(f'{cites[i].text}\n\n')
        try:
            next = driver.find_element(By.CSS_SELECTOR, 'a#pnnext')
            next.click()
        except:
            break


if __name__ == "__main__":
    collect_sources()
    driver.close()
