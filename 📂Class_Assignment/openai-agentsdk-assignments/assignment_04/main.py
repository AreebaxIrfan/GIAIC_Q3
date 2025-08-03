import os
import asyncio
from typing import Any, List, Optional
from agents import (
    Agent,
    RunConfig,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Runner,
    function_tool,
    RunContextWrapper,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    output_guardrail,
)
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent
from pydantic import BaseModel
from dataclasses import dataclass

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in .env file.")

provider = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/",
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)
run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=False,
)

#  Pydantic BaseModel
class UserInfo(BaseModel):
    name: str
    is_premium: bool
    issue_type: Optional[str] = None

# Product dataclass
@dataclass
class Product:
    name: str
    price: int
    quantity: int
    description: str

# Tool no 1
@function_tool
async def stationary_items(wrapper: RunContextWrapper[UserInfo]) -> List[Product]:
    """Provide information about available stationary products."""
    return [
        Product(name="pencil", price=250, quantity=140, description="Pencil is available in just 2 colors"),
        Product(name="eraser", price=29, quantity=50, description="We have Dollar brand of eraser only"),
        Product(name="notebook", price=290, quantity=20, description="We have 500, 600, or 900 pages notebook available only"),
    ]

# Tool no 2 refund tool is enabled
def check_is_premium(self, context: Any) -> bool:
    """Check if the user is premium to enable the refund tool."""
    if isinstance(context, RunContextWrapper):
        return context.context.is_premium
    elif isinstance(context, UserInfo):
        return context.is_premium
    return False

# Tool no 3 is_premium == True for checking
@function_tool(is_enabled=check_is_premium)
async def refund_tool(wrapper: RunContextWrapper[UserInfo]) -> str:
    """Process a refund for the user."""
    if not wrapper.context.is_premium:
        return "Error: Refunds are only available for premium users."
    return f"Refund processed for {wrapper.context.name} (Premium user)."

# guardrail output model
class RoutingGuardrailOutput(BaseModel):
    is_correct_routing: bool
    reasoning: str
    expected_agent: str

# Guardrail agent to check routing logic
guardrail_agent = Agent(
    name="RoutingGuardrailAgent",
    instructions=(
        "Analyze the output of the SupportAgent to determine if it correctly routes the query. "
        "If the user query contains 'refund', the output should indicate a handoff to the BillingAgent. "
        "If the query is about product information (e.g., name, price, quantity, description), "
        "the output should indicate a handoff to the ItemInfoAgent. "
        "Return whether the routing is correct, the reasoning, and the expected agent."
    ),
    output_type=RoutingGuardrailOutput,
    model=model,
)

@output_guardrail
async def routing_guardrail(
    ctx: RunContextWrapper[UserInfo], agent: Agent, output: str
) -> GuardrailFunctionOutput:
    # Extract the user query from the context (if available)
    user_query = ctx.context.issue_type if ctx.context else "unknown"
    # Run the guardrail agent to analyze the output
    result = await Runner.run(
        guardrail_agent,
        input=f"User query issue type: {user_query}\nSupportAgent output: {output}",
        context=ctx.context,
        run_config=run_config
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_correct_routing,
    )
# Agent 1
item_info_agent = Agent(
    name="ItemInfoAgent",
    instructions=(
        "Handle all queries related to product information, such as name, price, quantity, or description. "
        "Use the stationary_items tool to retrieve product details and answer the user's query."
    ),
    tools=[stationary_items],
    model=model,
)
# Agent 2
# Billing Agent for refund-related queries
billing_agent = Agent(
    name="BillingAgent",
    instructions=(
        "Handle billing-related queries, including refunds for premium users only. "
        "Use the refund_tool to process refunds when appropriate. "
        "If user is not a premium user, politely say this feature is only for premium users."
    ),
    tools=[refund_tool],
    model=model,
)
# Agent 3
# Support Agent to triage queries and hand off to specialized agents
support_agent = Agent(
    name="SupportAgent",
    instructions=(
        "Handle all user queries. "
        "For refund-related queries, hand off to the BillingAgent. "
        "For product-related queries (e.g., product name, price, quantity, description), hand off to the ItemInfoAgent. "
        "If the user is not a premium user and requests a refund, politely say this feature is only for premium users."
    ),
    tools=[refund_tool, stationary_items],
    handoffs=[billing_agent, item_info_agent],
    output_guardrails=[routing_guardrail],  # Attach the output guardrail
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
            context=user_context,
            run_config=run_config
        )

        # Stream raw response events
        try:
            print("Agent: ", end="", flush=True)
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    print(event.data.delta, end="", flush=True)

            # Get the final output...
            final_result = result
            if final_result.final_output:
                print(f"\n\nFinal Response: {final_result.final_output}")
            else:
                print("\n\nNo final output received.")
        except OutputGuardrailTripwireTriggered as e:
            print(f"\n\nError: Output guardrail tripped - Incorrect routing detected: {e}")
            print("Please try again or contact support for assistance.")
        except Exception as e:
            print(f"\n\nError: An unexpected error occurred - {str(e)}")

        print("=== Request Complete ===")

if __name__ == "__main__":
    asyncio.run(main())
