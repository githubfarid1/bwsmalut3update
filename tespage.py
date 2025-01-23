from playwright.sync_api import sync_playwright
import time
posts = ['https://playwright.dev/','https://playwright.dev/python/',]

def scrape_post_info(context, post):
    page = context.new_page()
    page.goto(post)
    print(page.title())
    # do whatever scraping you need to
    page.close()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    for post in posts:
        scrape_post_info(context, post)
        # some time delay
        time.sleep(2)
    breakpoint()
    browser.close()