import asyncio
from prompt_toolkit import PromptSession
from dotenv import load_dotenv
import os
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel, AsyncOpenAI, RunContextWrapper, TResponseInputItem, InputGuardrailTripwireTriggered, input_guardrail, GuardrailFunctionOutput
from agents.run import RunConfig
from agents.model_settings import ModelSettings
from pydantic import BaseModel
from typing import List

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

# Configure model settings (removed unsupported parameters)
model_settings = ModelSettings(
    temperature=0.7,  # Balanced creativity and coherence
    parallel_tool_calls=True  # Allow multiple tool calls in one query
)

# Configure the run settings
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=False,
    model_settings=model_settings
)

# Book database
BOOK_DATABASE = {
    "Atomic Habits": {"author": "James Clear", "copies": 3},
    "Rich Dad Poor Dad": {"author": "Robert T. Kiyosaki", "copies": 2},
    "Think and Grow Rich": {"author": "Napoleon Hill", "copies": 0},
    "The 10X Rule": {"author": "Grant Cardone", "copies": 5}
}

# Pydantic models
class UserInfo(BaseModel):
    name: str
    member_id: int
    # conversation_history: List[str] = []  # Uncomment for conversation history

class Book(BaseModel):
    name: str
    author: str
    copies: int

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
        tripwire_triggered=not result.final_output.is_library_output
    )

# Search Book Tool
@function_tool
async def search_book_tool(book_name: str) -> dict:
    """Check if a book exists in the library database."""
    # Case-insensitive search
    book_name_lower = book_name.lower()
    matched_book = next((name for name in BOOK_DATABASE if name.lower() == book_name_lower), None)
    book_exists = matched_book is not None
    return {
        "book_name": matched_book or book_name,
        "exists": book_exists,
        "message": f"The book '{matched_book or book_name}' {'is' if book_exists else 'is not'} available in the library."
    }

# Check Availability Tool
@function_tool
async def check_availability_tool(book_name: str) -> dict:
    """Check the number of available copies for a book."""
    # Case-insensitive search
    book_name_lower = book_name.lower()
    matched_book = next((name for name in BOOK_DATABASE if name.lower() == book_name_lower), None)
    copies = BOOK_DATABASE.get(matched_book, {"copies": 0})["copies"] if matched_book else 0
    return {
        "book_name": matched_book or book_name,
        "copies_available": copies,
        "message": f"There {'are' if copies > 0 else 'are no'} {copies} copies of '{matched_book or book_name}' available."
    }

# Define is_enabled function for book_agent
async def is_book_agent_enabled(self, context: RunContextWrapper[UserInfo]) -> bool:
    return isinstance(context, RunContextWrapper) and isinstance(context.context, UserInfo) and bool(context.context.member_id)

@function_tool(is_enabled=is_book_agent_enabled)
async def book_agent(wrapper: RunContextWrapper[UserInfo]) -> list[Book]:
    """Return a list of all books with their authors and available copies."""
    return [
        Book(name=name, author=info["author"], copies=info["copies"])
        for name, info in BOOK_DATABASE.items()
    ]

# Dynamic instructions for main agent
def dynamic_instructions(context: RunContextWrapper[UserInfo], agent: Agent[UserInfo]) -> str:
    return (
        f"Hello {context.context.name}, I am your librarian assistant. "
        "Handle all queries related to the library, such as finding books or checking their availability. "
        "Use the search_book_tool to check if a book exists, check_availability_tool to see how many copies are available, "
        "and book_agent to list all books. For queries about a book's existence and availability, use both tools as needed. "
        "Ensure book names are matched case-insensitively."
    )

# Define main librarian agent
main_agent = Agent(
    name="Librarian Agent",
    instructions=dynamic_instructions,
    model=model,
    tools=[book_agent, search_book_tool, check_availability_tool],
    input_guardrails=[library_guardrail]
)

async def get_user_input():
    session = PromptSession("Enter your question (type 'exit' to quit): ")
    return await session.prompt_async()

async def main():
    user_context = UserInfo(name='Areeba Irfan', member_id=231)
    
    while True:
        user_input = await get_user_input()
        
        # Check for exit condition
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
            
        try:
            result = await Runner.run(
                main_agent,
                user_input,
                run_config=config,
                context=user_context
            )
            print(result.final_output)
            # Optionally store conversation history
            # user_context.conversation_history.append(user_input)
        except InputGuardrailTripwireTriggered:
            print("Query is not library-related. Please ask about books or library services.")
        except Exception as e:
            if "429" in str(e):
                print("API quota exceeded. Please check your Gemini API plan and billing details at https://cloud.google.com/vertex-ai/docs/quotas.")
            elif "400" in str(e):
                print("Invalid API request. Please check the model configuration and try again.")
            else:
                print(f"An error occurred: {e}")

# Rebuild Pydantic models if necessary
Book.model_rebuild()
UserInfo.model_rebuild()
LibraryOutput.model_rebuild()

if __name__ == "__main__":
    asyncio.run(main())
