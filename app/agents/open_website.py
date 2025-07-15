# intents/open_website.py
from playwright.async_api import async_playwright
from controller.intent_registry import intent
import base64

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
        screenshot_bytes = await page.screenshot(type="png")
        base64_image = base64.b64encode(screenshot_bytes).decode("utf-8")


    return {
        "message": f"Opened website: {url}",
        "screenshot": base64_image
    }
