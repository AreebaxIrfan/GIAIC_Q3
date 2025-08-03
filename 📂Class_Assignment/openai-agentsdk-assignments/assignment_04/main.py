import os
import asyncio
from typing import Any, List, Optional
from agents import Agent, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, function_tool, RunContextWrapper
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent
from pydantic import BaseModel
from dataclasses import dataclass

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.")

# Set up the provider for Gemini API
provider = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/",
)

# Define the model for Gemini
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",  # Corrected to a valid model
    openai_client=provider,
)

# Run configuration
run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=False,
)



# Define the context object using Pydantic
class UserInfo(BaseModel):
    name: str
    is_premium: bool
    issue_type: Optional[str] = None

# Define Product dataclass
@dataclass
class Product:
    name: str
    price: int
    quantity: int
    description: str

# Tool for retrieving stationary items
@function_tool
async def stationary_items(wrapper: RunContextWrapper[UserInfo]) -> List[Product]:
    """Provide information about available stationary products."""
    return [
        Product(name="pencil", price=250, quantity=140, description="Pencil is available in just 2 colors"),
        Product(name="eraser", price=29, quantity=50, description="We have Dollar brand of eraser only"),
        Product(name="notebook", price=290, quantity=20, description="We have 500, 600, or 900 pages notebook available only"),
    ]

# Function to check if the refund tool is enabled
def check_is_premium(self, context: Any) -> bool:
    """Check if the user is premium to enable the refund tool."""
    if isinstance(context, RunContextWrapper):
        return context.context.is_premium
    elif isinstance(context, UserInfo):
        return context.is_premium
    return False

# Tool for processing refunds, conditionally enabled based on is_premium
@function_tool(is_enabled=check_is_premium)
async def refund_tool(wrapper: RunContextWrapper[UserInfo]) -> str:
    """Process a refund for the user."""
    if not wrapper.context.is_premium:
        return "Error: Refunds are only available for premium users."
    return f"Refund processed for {wrapper.context.name} (Premium user)."

# Item Info Agent for product-related queries
item_info_agent = Agent(
    name="ItemInfoAgent",
    instructions=(
        "Handle all queries related to product information, such as name, price, quantity, or description. "
        "Use the stationary_items tool to retrieve product details and answer the user's query."
    ),
    tools=[stationary_items],
    model=model,
)

# Billing Agent for refund-related queries
billing_agent = Agent(
    name="BillingAgent",
    instructions=(
        "Handle billing-related queries, including refunds for premium users only. "
        "Use the refund_tool to process refunds when appropriate."
        "if user not a premium user, slightly say no this feature only for premium user"
    ),
    tools=[refund_tool],
    model=model,
)

# Support Agent to triage queries and hand off to specialized agents
support_agent = Agent(
    name="SupportAgent",
    instructions=(
        "Handle all user queries. "
        "For refund-related queries, use the refund_tool only if user not a premium user slightly say no this feature only for premium user "
        "other then refund things you should used the billing agent "
        "For product-related queries (e.g., product name, price, quantity, description), hand off to the ItemInfoAgent."
    ),
    tools=[refund_tool, stationary_items],
    handoffs=[billing_agent, item_info_agent],
    model=model,
)

async def main():
    user_context = UserInfo(name="Jane Smith", is_premium=False)

    print("💬 Billing Support Agent")
    print("Type 'quit' to exit.\n")

    while True:
        prompt = input("\nHow can I assist you today? ")
        if prompt.lower() == "quit":
            print("👋 Exiting chat. Goodbye!")
            break

        # Update issue type for context
        user_context.issue_type = "billing" if "refund" in prompt.lower() else "product"

        print(f"\nIssue Type Detected: {user_context.issue_type}")
        print("=== Processing Request ===")

        # Run the agent with streaming
        result = Runner.run_streamed(
            support_agent,
            input=prompt,
            context=user_context if user_context.issue_type == "billing" else None,
            run_config=run_config
        )

        # Stream raw response events
        try:
            print("Agent: ", end="", flush=True)
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    print(event.data.delta, end="", flush=True)

            # Get final output
            final_result = result
            if final_result.final_output:
                print(f"\n\nFinal Response: {final_result.final_output}")
            else:
                print("\n\nNo final output received.")
        except Exception as e:
            print(f"\n\nError: An unexpected error occurred - {str(e)}")

        print("=== Request Complete ===")

if __name__ == "__main__":
    asyncio.run(main())
