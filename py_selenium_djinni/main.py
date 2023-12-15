import os
import json
from time import sleep
from random import randint

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from database.ddl import add_vacancy


#* CONSTANT 
NOT_ERROR = True
NUM_PAGE = 0
FILE_JSON = "database/vacancies.json"

#* settings selenium
option = webdriver.FirefoxOptions()
option.set_preference("dom.webdriver.enabled", False) # Anti webdriver
option.set_preference("dom.webnotifications.enabled", False) # False notifications
option.set_preference("media.volume_scale", "0.0") # Mute sound
option.set_preference("general.useragent.override", "examle :)") # UserAgent
option.headless = True # Demon mode

#* settings .env
config = dotenv_values(".env")

sleep(randint(3,5))
print("Загрузка...")

# site djinni
browser = webdriver.Firefox(options=option)
browser.get("https://djinni.co/my/dashboard/")

sleep(randint(3,5))
print("Авторизовуюся...")

# input email
xpath_email = "/html/body/div[1]/div[2]/div/div/div[2]/form/div[1]/div[1]/input"
browser.find_element(By.XPATH, xpath_email).send_keys(config["DJINNI_LOGIN"])

# input password
xpath_password = "/html/body/div[1]/div[2]/div/div/div[2]/form/div[1]/div[2]/input"
browser.find_element(By.XPATH, xpath_password).send_keys(config["DJINNI_PASSWORD"])

# click sign-in 
xpath_buttton = "/html/body/div[1]/div[2]/div/div/div[2]/form/div[1]/div[3]/button"
browser.find_element(By.XPATH, xpath_buttton).click()

sleep(randint(3,5))
print("Успішно! Всі вакансії вже в базі даних")


while NOT_ERROR:
    NUM_PAGE += 1
    
    print(f"Обробляю {NUM_PAGE} сторінку...")
    
    # create url
    url = f"https://djinni.co/jobs/?page={NUM_PAGE}"
    browser.get(url)
    
    # check url 
    current_url = browser.current_url
    if url == current_url or NUM_PAGE == 1:
        # download html code
        html_content = browser.page_source
        
        # create object bs4
        soup = BeautifulSoup(html_content, 'lxml')

        ul_element = soup.find('ul', class_='list-unstyled list-jobs mb-4')
        li_elements = ul_element.find_all('li', class_='list-jobs__item job-list__item')
        for link in li_elements:
            # company
            try:
                company_name = link.find('a', class_='mr-1').get_text(strip=True)
            except AttributeError:
                company_name = "None"
            # job title
            job_title = link.find('a', class_='h3 job-list-item__link').get_text(strip=True)
            # job link
            job_link = link.find('a', class_='h3 job-list-item__link')['href']
            # employee name
            employee_name = link.find('a', class_='link-muted mr-2').get_text(strip=True)
            # date post
            date_element = soup.find('span', class_='mr-2 nobr')['data-original-title']
            
            data = {
                "company": company_name,
                "job_title": job_title,
                "job_link": f"https://djinni.co{job_link}",
                "employee": employee_name,
                "date": date_element
            }
            
            add_vacancy(data)
            
            if os.path.exists(FILE_JSON):
                
                with open(FILE_JSON, "r", encoding="utf-8") as file:
                    vacancies = json.load(file)
                
                vacancies.append(data)
                    
                with open(FILE_JSON, "w", encoding="utf-8") as file:
                    json.dump(vacancies, file, ensure_ascii=False, indent=4)
                    
            else:
                with open(FILE_JSON, "w", encoding="utf-8") as file:
                    vacancies = [data]
                    json.dump(vacancies, file, ensure_ascii=False, indent=4)
        
    else:
        print("Завантаження вакансій завершено!")
        NOT_ERROR = False
        
    sleep(randint(3,5))

browser.quit()