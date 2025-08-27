from playwright.sync_api import sync_playwright


def url_fetcher(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        for i in range(1, 11):
            page.goto(f'https://www.technewsphilippines.com/page/{i}/')
            page.wait_for_selector('article')  # wait for the element to load
            items = page.query_selector_all('article')
            for item in items:
                # _title = item.query_selector('h2.post-box-title').inner_text()
                # _date = item.query_selector('.tie-date').inner_text()
                _url = item.query_selector('a').get_attribute('href')
                # print(_title)
                # print(_date)
                print(_url)
        browser.close()
    
