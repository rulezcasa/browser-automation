# login_with_real_chrome_profile.py
import asyncio
import os
from playwright.async_api import async_playwright
import platform

async def launch_with_existing_profile():
    chrome_user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome")

    profile_name = "Default"  # or 'Profile 1' if you're using another
    full_profile_path = os.path.join(chrome_user_data_dir, profile_name)

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=full_profile_path,
            headless=False,
            channel="chrome",  # ✅ Uses real installed Chrome
            args=["--disable-blink-features=AutomationControlled"]
        )

        # Use first tab, or open Gmail if none
        pages = browser.pages
        page = pages[0] if pages else await browser.new_page()
        await page.goto("https://mail.google.com/")

        print("📬 Please interact with Gmail manually if needed...")
        await page.wait_for_selector("div.T-I.T-I-KE.L3", timeout=300000)  # Wait for Compose button

        print("✅ Gmail ready. You can now automate this session later.")
        await asyncio.sleep(5)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(launch_with_existing_profile())
