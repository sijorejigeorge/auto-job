from playwright.sync_api import sync_playwright

def get_page_content(url):
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url)
    content = page.content()
    return content, page, browser

def perform_search(page, query):
    # Example for Google
    search_box = page.query_selector('input[name="q"]')
    if search_box:
        search_box.fill(query)
        search_box.press('Enter')
