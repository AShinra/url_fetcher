from playwright.sync_api import sync_playwright
from common import connect_to_mongodb, insert_document, check_if_document_exist, clean_url, format_date, get_url_response
import re
from datetime import datetime
import json
import time


def url_fetcher1(fetcher_url, fetcher_title_selector, fetcher_url_selector):
    url_list = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        for i in range(1, 21):
            response = get_url_response(page, f'{fetcher_url}{i}')
            if response.status == 200:
                try:
                    page.wait_for_selector(fetcher_title_selector, timeout=60000)  # wait for the element to load
                    items = page.query_selector_all(fetcher_title_selector)                
                except Exception as e:
                    print(f'page {i} - {e}')
                else:
                    for item in items:
                        # get url
                        try:
                            url = item.query_selector(fetcher_url_selector).query_selector('a').get_attribute('href')
                        except:
                            url = item.query_selector('a').get_attribute('href')
                        finally:
                            url_list.append([datetime.now(), url])
                    
        browser.close()
    return url_list


def url_fetcher2(fetcher_url, fetcher_title_selector, fetcher_url_selector):
    url_list = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        response = get_url_response(page, f'{fetcher_url}')

        for i in range(1, 21):
            page.keyboard.press("End")
            time.sleep(5)

        if response.status == 200:
            try:
                page.wait_for_selector(fetcher_title_selector, timeout=60000)  # wait for the element to load
                items = page.query_selector_all(fetcher_title_selector)                
            except Exception as e:
                print(f'page {i} - {e}')
            else:
                for item in items:
                    # get url
                    try:
                        url = item.query_selector(fetcher_url_selector).query_selector('a').get_attribute('href')
                    except:
                        url = item.query_selector('a').get_attribute('href')
                    finally:
                        url_list.append([datetime.now(), url])
                    
        browser.close()
    return url_list
    

# def fetcher(fetcher_data, fetcher_number):
def fetcher(fetcher_data):

    _fetcher_url = fetcher_data['fetcher_url']
    fetcher_title_selector = fetcher_data['selector_container']
    fetcher_url_selector = fetcher_data['selector_title']
    fetcher_type = fetcher_data['fetcher_no']

    if fetcher_type==1:
        url_list = url_fetcher1(_fetcher_url, fetcher_title_selector, fetcher_url_selector)
    elif fetcher_type==2:
        url_list = url_fetcher2(_fetcher_url, fetcher_title_selector, fetcher_url_selector)

    url_count = len(url_list)
    print(f'Collected {url_count} links')
    # for url_data in url_list:
    #     print(url_data[-1])
    client = connect_to_mongodb()
    db = client['fetcher']
    collection = db['collected_url']
    print('Filtered Links')
    url_count = 0
    for url in url_list:
        cleanurl = clean_url(url[-1])        
        document = {"url":cleanurl}
        status = check_if_document_exist(db, collection, document)
        document = {
            "collected_date":url[0],
            "url":cleanurl
            }
        if status == 0:
            insert_document(db, collection, document)
            url_count += 1
    
    print(f'Inserted to database - {url_count} url')