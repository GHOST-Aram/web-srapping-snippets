from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get('https://www.upwork.com/freelance-jobs/web-scraping/')
load_more = driver.find_element(By.LINK_TEXT,'Load More Jobs')
while True:
    job_titles = driver.find_elements(By.CLASS_NAME,'job-title')
    job_descriptions = driver.find_elements(By.CLASS_NAME,'job-description')

    with open('jobs.txt', 'a') as jobs:
        for i in range(len(job_descriptions)):
            jobs.write(f'Job title: {job_titles[i].text}\n')
            jobs.write(f'Job description: {job_descriptions[i].text}\n\n')
    if not load_more.is_displayed():
        break
    load_more.click()
    print(load_more.is_displayed)

driver.quit()