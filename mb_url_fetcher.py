from playwright.sync_api import sync_playwright
from common import connect_to_mongodb, insert_document, check_if_document_exist, clean_url, format_date
import re
from datetime import datetime


def section_fetcher(url):

    section_list = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        response = page.goto(url, wait_until="domcontentloaded", timeout=60000)
        
        if response.status==200:
            try:
                page.wait_for_selector('div.outer', timeout=60000)
                items = page.query_selector_all('div.outer')
            except Exception as e:
                print(e)
            else:
                for item in items:
                    section_url = item.query_selector('a').get_attribute('href')
                    if '/category/' in section_url:
                        section_list.append(section_url)

        browser.close()
    return section_list

def url_fetcher(url):
    url_list = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        for i in range(1, 11):
            response = page.goto(f'{url}?page={i}', wait_until="domcontentloaded", timeout=60000)
            # press END twice
            page.keyboard.press("End")
            page.keyboard.press("End")
            if response.status == 200:
                try:
                    page.wait_for_selector('div.mb-latest-news-list', timeout=60000)  # wait for the element to load
                    items = page.query_selector_all('div.mb-latest-news-list')                
                except Exception as e:
                    print(f'page {i} - {e}')
                else:
                    print(f'fetching links from {url}')
                    for item in items:
                        # get url                        
                        _url = item.query_selector('div.desc').query_selector('a').get_attribute('href')
                        date_parts = _url.split('/')[3:6]
                        _date = datetime.strptime("-".join(date_parts), "%Y-%m-%d")
                        # get publication date
                        # datestr = item.query_selector('span.tie-date').inner_text()
                        # _date = datetime.strptime(datestr, "%b %d, %Y")
                        url_list.append([datetime.now(), _date, _url])
                    
        browser.close()
    return url_list
    
if __name__ == '__main__':
    section_list = section_fetcher('https://mb.com.ph/sitemap/')
    for section in section_list:
        url_list = url_fetcher(section)
        for i in url_list:
            print(i)
        client = connect_to_mongodb()
        db = client['fetcher']
        collection = db['collected_url']

        for url in url_list:
            cleanurl = clean_url(url[-1])        
            document = {"publication_date":url[1], "url":cleanurl}
            status = check_if_document_exist(db, collection, document)
            document = {"collected_date":url[0], "publication_date":url[1], "url":cleanurl}
            if status == 0:
                insert_document(db, collection, document)