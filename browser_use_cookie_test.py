import traceback
import json
import asyncio
import os
from pathlib import Path
from typing import Optional
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from browser_use import Browser, Agent

# Constants
COOKIES_PATH = Path(__file__).parent / "cookies.json"
WINDOW_SIZE = {'width': 1280, 'height': 1100}
USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36')


def load_cookie_from_env() -> Optional[str]:
    """Load cookie data from environment variable."""
    cookie_data = os.getenv('CHC_RESY_COOKIE')
    if cookie_data:
        try:
            with COOKIES_PATH.open('w') as f:
                f.write(cookie_data)
            return str(COOKIES_PATH)
        except IOError as e:
            print(f"Error writing cookie file: {e}")
            return None
    return str(COOKIES_PATH)


def create_browser_config(cookies_file: str) -> BrowserContextConfig:
    """Create browser configuration."""
    return BrowserContextConfig(
        cookies_file=cookies_file,
        wait_for_network_idle_page_load_time=3.0,
        browser_window_size=WINDOW_SIZE,
        locale='en-US',
        user_agent=USER_AGENT,
        highlight_elements=True,
        viewport_expansion=500,
    )


async def run_search(context: BrowserContext) -> None:
    """Execute the search task using the browser agent."""
    try:
        task = (
            'Book a table at \"Han Dynasty Long Island City\"'
            'At the reservation booking website, search for the restaurant name'
            'Click onto the restaurant page to show all availabilities'
            'Then, enter the details as follow: Feb 12 5pm local time, party size: 2 people'
        )
        agent = Agent(
            browser_context=context,
            task=task,
            llm=ChatOpenAI(model="gpt-4o"),
        )
        result = await agent.run()
        print(result)
    except Exception as e:
        print("Error occurred during search:")
        print(traceback.format_exc())


async def main() -> None:
    """Main execution function."""
    load_dotenv()

    cookies_file = load_cookie_from_env()
    if not cookies_file:
        return

    config = create_browser_config(cookies_file)
    browser = Browser()
    context = BrowserContext(browser=browser, config=config)

    try:
        await run_search(context)
    finally:
        await browser.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print("Error occurred while running asyncio:")
        print(traceback.format_exc())
