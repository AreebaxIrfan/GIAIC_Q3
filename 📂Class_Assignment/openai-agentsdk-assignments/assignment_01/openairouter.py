from agents import Agent , OpenAIChatCompletionsModel, Runner, set_tracing_disabled, AsyncOpenAI
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

if not os.getenv('OPENROUTER_API_KEY'):
    raise ValueError('OPENAI_API_KEY is not set')
if not os.getenv('BASE_URL'):
    raise ValueError('BASE_URL is not set')

MODEL = "google/gemini-2.0-flash-001"

client = AsyncOpenAI(
    api_key=os.getenv('OPENROUTER_API_KEY'),
    base_url=os.getenv('BASE_URL'),

)


set_tracing_disabled(disabled=True)
async def main():
    agent = Agent(
        name='Assistant',
        instructions='You can should generated a poetry in roman urdu in every user input according to the user input',
        model=OpenAIChatCompletionsModel(model=MODEL,openai_client=client),
    )
    input_user= input('Enter your query:')
    result = await Runner.run(
        agent,
        "hi"
    )
    print(result.final_output)

if __name__ == '__main__':
    asyncio.run(main())
