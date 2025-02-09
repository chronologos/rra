from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
load_dotenv()


async def main():
    agent = Agent(
        task="Go to Google, search for Carbone restaurant reservation, click on the link that allows reservation, try to book a spot for March 10th 2025.",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
