
import asyncio
from playwright.async_api import async_playwright
from controller.intent_registry import intent
import os
import base64

@intent("send_email")
async def send_email_via_browser(entities):
    to = entities.get("recipient")
    subject = entities.get("subject")
    body = entities.get("body")
    user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome")
    profile = "Default"  

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=os.path.join(user_data_dir, profile),
            headless=False,
            channel="chrome",  # Launches actual Chrome, not bundled Chromium
        )
        page = await browser.new_page()

        # Open Gmail and wait for it to load
        await page.goto("https://mail.google.com/mail/u/0/#inbox", timeout=60000)
        await page.wait_for_selector("div.T-I.T-I-KE.L3", timeout=30000)  # Compose button

        # Click Compose
        await page.click("div.T-I.T-I-KE.L3")

        # Wait for compose popup to appear reliably
        compose_popup = page.locator("div[role='dialog']")
        await compose_popup.wait_for(state="visible", timeout=15000)

        # Now locate the 'To' field inside that popup
        to_field = compose_popup.locator("input[aria-label='To recipients']")
        await to_field.wait_for(state="visible", timeout=10000)
        await to_field.type(to, delay=50)
        await to_field.press("Enter")  # Gmail expects Enter to complete the address

        await page.keyboard.press("Enter")

        to_ss = await page.screenshot(type="png")
        to_64 = base64.b64encode(to_ss).decode("utf-8")

        # Fill in subject
        subject_field = page.locator('input[name="subjectbox"]')
        await subject_field.wait_for(state="visible", timeout=10000)
        await subject_field.type(subject, delay=50)

        subject_ss = await page.screenshot(type="png")
        subject_64 = base64.b64encode(subject_ss).decode("utf-8")

        # Fill in message body
        body_field = page.locator('div[aria-label="Message Body"]')
        await body_field.wait_for(state="visible", timeout=10000)
        await body_field.type(body, delay=30)

        body_ss = await page.screenshot(type="png")
        body_64 = base64.b64encode(body_ss).decode("utf-8")

        # Click Send
        await page.click("div[aria-label*='Send'][role=button]")

        await asyncio.sleep(5)

        return {
        "message": f"Sent email to {to}",
        "screenshots": [to_64, subject_64, body_64]
        }

       

