import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel, AsyncOpenAI, RunContextWrapper, TResponseInputItem, InputGuardrailTripwireTriggered, input_guardrail, GuardrailFunctionOutput
from agents.run import RunConfig
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Get Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found, please check your .env file.")

# Configure external client for Gemini API
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

# Configure the model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Configure the run settings
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Pydantic models
class UserInfo(BaseModel):
    name: str
    member_id: int

class Book(BaseModel):
    name: str
    author: str

class LibraryOutput(BaseModel):
    is_library_output: bool
    reasoning: str

# Define guardrail agent
guardrail_agent = Agent(
    name='Guardrail Check',
    instructions='Check if the user is asking about library-related questions. Return is_library_output=True if the query is about books or library services, otherwise False with reasoning.',
    output_type=LibraryOutput
)

@input_guardrail
async def library_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_library_output  # Trip if not library-related
    )

# Define is_enabled function for book_agent
async def is_book_agent_enabled(self, context: RunContextWrapper[UserInfo]) -> bool:
    return isinstance(context, RunContextWrapper) and isinstance(context.context, UserInfo) and bool(context.context.member_id)

@function_tool(is_enabled=is_book_agent_enabled)
async def book_agent(wrapper: RunContextWrapper[UserInfo]) -> list[Book]:
    """Return a list of available books with their authors."""
    return [
        Book(name='Atomic Habits', author='James Clear'),
        Book(name='Rich Dad Poor Dad', author='Robert T. Kiyosaki'),
        Book(name='Think and Grow Rich', author='Napoleon Hill'),
        Book(name='The 10X Rule', author='Grant Cardone'),
    ]

# Define main librarian agent
main_agent = Agent(
    name="Librarian Agent",
    instructions="You are a librarian agent. Handle all queries related to the library and use the book_agent tool to find books when needed.",
    model=model,
    tools=[book_agent],
    # input_guardrails=[library_guardrail]
)

# Main async function
async def main():
    user_input = input("Enter your question: ")
    user_context = UserInfo(name='Areeba Irfan', member_id=231)
    
    try:
        result = await Runner.run(
            main_agent,
            user_input,
            run_config=config,
            context=user_context
        )
        print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("Query is not library-related. Please ask about books or library services.")

# Ensure Pydantic models are rebuilt to avoid schema errors
Book.model_rebuild()
UserInfo.model_rebuild()
LibraryOutput.model_rebuild()

if __name__ == "__main__":
    asyncio.run(main())