import os
import json
import re
import time
from selenium.common.exceptions import StaleElementReferenceException

import config
from database import DataBase
from driver import get_driver


def parse_competitions(filename):
    urls = []
    button = '.button.ui-state-default.rc-l'
    with open (filename, 'r', encoding = 'utf-8') as f_imp:
        driver = get_driver()
        for competition in f_imp:
            driver.get(competition)
            while True:
                elements = driver.find_elements_by_css_selector('.result-1')
                try:
                    links = [elem.get_attribute('href') for elem in elements]
                except StaleElementReferenceException:
                    print('Stale element error, try increasing wait time')
                    driver.quit()
                    quit(-1)
                last_link = None
                for link in links:
                    if last_link != link:
                        urls.append(link)
                        last_link = link
                        print(f'added {link}')
                title = driver.find_element_by_css_selector(button).get_attribute('title')
                if title == 'No data for previous month':
                    break
                else:
                    driver.find_element_by_css_selector(button).click()
                    time.sleep(0.5)
    driver.quit()
    return urls

def upload_links(urls):
    db = DataBase()
    for url in urls:
        game_id = int(re.search('/(\d*)/L', url).groups()[0])
        record = {'url':url,'game_id':game_id}
        db.set_record('urls',record)
        print('uploaded', url)
    db.commit()


if __name__ == '__main__':
    urls = parse_competitions('competitions.txt')
    upload_links(urls)

