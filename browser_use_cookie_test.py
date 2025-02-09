import traceback
import json
import asyncio
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from browser_use import Browser
from browser_use import Agent

load_dotenv()


# async def main():
#     agent = Agent(
#         task="Go to Resy.com. Go to my account status page.",
#         llm=ChatOpenAI(model="gpt-4o"),
#     )
#     result = await agent.run()
#     print(result)

try:
    with open("/Users/iantay/Documents/repos/rra/cookies.json", "r") as f:
        json.load(f)
except Exception as e:
    print("Error occurred while running json:")
    print(traceback.format_exc())

config = BrowserContextConfig(
    cookies_file="/Users/iantay/Documents/repos/rra/cookies.json",
    wait_for_network_idle_page_load_time=3.0,
    browser_window_size={'width': 1280, 'height': 1100},
    locale='en-US',
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    highlight_elements=True,
    viewport_expansion=500,
    # allowed_domains=['google.com', 'resy.com', 'about:blank'],
)

browser = Browser()
context = BrowserContext(browser=browser, config=config)


async def run_search():
    try:
        agent = Agent(
            browser_context=context,
            task='Go to resy.com. Go to my account status page.',
            llm=ChatOpenAI(model="gpt-4o-mini"),)
        result = await agent.run()
        print(result)
    except Exception as e:
        print("Error occurred during search:")
        print(traceback.format_exc())

try:
    asyncio.run(run_search())
except Exception as e:
    print("Error occurred while running asyncio:")
    print(traceback.format_exc())
