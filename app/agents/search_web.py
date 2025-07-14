# intents/search_web.py
from playwright.async_api import async_playwright
from controller.intent_registry import intent

@intent("search_web")
async def handle_search_web(entities):
    query = entities.get("query")
    if not query:
        raise ValueError("Missing 'query' in search_web intent")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://www.google.com")
        await page.fill("#APjFqb", query)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(5000)
        await browser.close()

    return f"Searched Google for '{query}'."
