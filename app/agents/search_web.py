# intents/search_web.py
from playwright.async_api import async_playwright
from controller.intent_registry import intent
import base64
import os

@intent("search_web")
async def handle_search_web(entities):
    query = entities.get("query")
    user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome")
    profile = "Default" 
    if not query:
        raise ValueError("Missing 'query' in search_web intent")

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
        user_data_dir=os.path.join(user_data_dir, profile),
        headless=False,
        channel="chrome",  
        )
        page = await browser.new_page()
        await page.goto("https://www.google.com")
        await page.fill("#APjFqb", query)
        before_ss = await page.screenshot(type="png")
        before_b64 = base64.b64encode(before_ss).decode("utf-8")
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(5000)
        after_ss = await page.screenshot(type="png")
        after_b64 = base64.b64encode(after_ss).decode("utf-8")

    return {
        "message": f"Searched Google for '{query}'.",
        "screenshots": [before_b64, after_b64]
    }
