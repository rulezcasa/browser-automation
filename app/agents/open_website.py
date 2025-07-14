# intents/open_website.py
from playwright.async_api import async_playwright
from controller.intent_registry import intent

@intent("open_website")
async def handle_open_website(entities):
    url = entities.get("url")
    if not url:
        raise ValueError("Missing 'url' in open_website intent")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_timeout(5000)
        await browser.close()

    return f"Opened website: {url}"
