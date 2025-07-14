# intents/send_email.py
from playwright.async_api import async_playwright
from controller.intent_registry import intent

@intent("send_email")
async def handle_send_email(entities):
    to = entities.get("to")
    subject = entities.get("subject", "")
    body = entities.get("body", "")

    if not to:
        raise ValueError("Missing recipient ('to') in send_email intent")

# intents/send_email.py
from playwright.async_api import async_playwright
from controller.intent_registry import intent

@intent("send_email")
async def handle_send_email(entities):
    to = entities.get("to")
    subject = entities.get("subject", "")
    body = entities.get("body", "")

    if not to:
        raise ValueError("Missing recipient ('to') in send_email intent")

    with async_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 🔐 Requires the user to be already logged into Gmail.
        page.goto("https://mail.google.com")
        print("Make sure you're logged in manually or use a saved session/context.")

        page.wait_for_selector("div[gh='cm']", timeout=60000)
        page.click("div[gh='cm']")  # Click Compose
        page.fill("textarea[name='to']", to)
        page.fill("input[name='subjectbox']", subject)
        page.fill("div[aria-label='Message Body']", body)
        page.click("div[aria-label*='Send']")

        page.wait_for_timeout(3000)
        browser.close()

    return f"Email sent to {to}."
