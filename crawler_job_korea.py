# -*- coding: utf-8 -*-

import csv
import time
import random

from tqdm import tqdm
from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager


@dataclass
class JobPost:
    company_name: str = None
    posting_title: str = None

    def __int__(self, company_name, posting_title):
        self.company_name = company_name
        self.posting_title = posting_title

    def to_list(self):
        return [self.company_name, self.posting_title]


# ========================== configure ==========================
PATH_CSV = '/Users/ask4git/Desktop/job_posting_by_jobkorea.csv'
COLUMN_CSV = ['company_name', 'job_posting_title']

HOST = 'https://www.jobkorea.co.kr'
# KEYWORD = '라이브커머스'
KEYWORD = '쇼호스트'
TIMEOUT = 3
SLEEP_MIN = 1.4
SLEEP_MAX = 1.8


# ===============================================================


def print_post_to_csv(posts):
    with open(PATH_CSV, 'w', encoding='utf-8-sig') as fout:
        writer = csv.writer(fout)
        writer.writerow(COLUMN_CSV)
        for post in posts:
            writer.writerow(post.to_list())


def navigate(driver):
    posts = []
    url = f'{HOST}/Search/?stext={KEYWORD}'
    driver.get(url)
    driver.implicitly_wait(TIMEOUT)

    total_num_of_post_list = int(driver.find_element(By.CLASS_NAME, 'dev_tot').text)
    total_num_of_post_list = int(total_num_of_post_list / 20)

    for _ in tqdm(range(total_num_of_post_list)):
        try:

            # crawling
            list_post = driver.find_element(By.CLASS_NAME, 'list-default').find_elements(By.CLASS_NAME, 'list-post')
            for post in list_post:
                company_name = post.find_element(By.CLASS_NAME, 'name.dev_view').get_attribute('title')
                posting_title = post.find_element(By.CLASS_NAME, 'title.dev_view').get_attribute('title')
                posts.append(JobPost(company_name=company_name, posting_title=posting_title))

            # waiting
            wait = WebDriverWait(driver, timeout=TIMEOUT)
            el_next_button = wait.until(
                expected_conditions.element_to_be_clickable((By.CLASS_NAME, 'tplBtn.btnPgnNext')))

            # click next page
            el_next_button.click()
            time.sleep(random.uniform(SLEEP_MIN, SLEEP_MAX))

        except Exception as error:
            print_post_to_csv(posts)
            break


def execute():
    # Setup webdriver options
    options = Options()
    options.add_argument("disable-infobars")
    options.add_argument("disable-extensions")
    options.add_argument('disable-gpu')
    service = Service(ChromeDriverManager().install())

    # Load Selenium 4.0 webdriver
    driver = webdriver.Chrome(service=service, options=options)
    navigate(driver)
    driver.close()


if __name__ == '__main__':
    execute()
