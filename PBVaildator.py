from pydantic_ai import Agent
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from pydantic_ai.toolsets.fastmcp import FastMCPToolset

from starlette.responses import JSONResponse
from starlette.routing import Route

load_dotenv()

class BPValidatorOutput(BaseModel):
    customer_name: str
    business_partner_number: str
    location: str
    machine_number: str
    problem_description: str
    status: str

def create_model(llm_model: str = "gpt-5-chat"):
    from pydantic_ai.models.openai import OpenAIResponsesModel
    from pydantic_ai.providers.openai import OpenAIProvider

    return OpenAIResponsesModel(
        model_name=llm_model,
        provider=OpenAIProvider(
            base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        ),
    )

model = create_model()

toolset1 = FastMCPToolset(os.getenv("FASTMCP_SERVER"))
toolset2 = FastMCPToolset("https://learn.microsoft.com/api/mcp")

BPValidaotor_agent = Agent(model, toolsets=[toolset1, toolset2])

# FastA2A app (Starlette)
app = BPValidaotor_agent.to_a2a()

async def microsoft_friendly_agent_card(request):
    base_url = str(request.base_url).rstrip("/") + "/"

    card = {
        "name": "BP Validator Agent",
        "description": "Extracts and validates machine service dispatch data and customer records.",
        "version": "1.0.0",

        "url": base_url,

        "preferredTransport": "JSONRPC",

        "capabilities": {
            "streaming": True,
            "pushNotifications": False
        },
        "defaultInputModes": ["text/plain"],
        "defaultOutputModes": ["text/plain"],

        "skills": [
            {
                "id": "bp-validator",
                "name": "Business Partner Validation",
                "description": "Validates customer and machine service details; can use MCP tools.",
                "tags": ["validation", "service", "dispatch"],
                "examples": ["Validate BP 123456 for machine 987 and summarize the issue."]
            }
        ],
    }

    return JSONResponse(card)

# Override both discovery paths
app.router.routes.insert(0, Route("/.well-known/agent.json", microsoft_friendly_agent_card, methods=["GET"]))
app.router.routes.insert(0, Route("/.well-known/agent-card.json", microsoft_friendly_agent_card, methods=["GET"]))
