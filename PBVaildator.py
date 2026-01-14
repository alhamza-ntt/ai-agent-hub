import os
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.toolsets.fastmcp import FastMCPToolset

from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

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

fastmcp_server1 = os.getenv("FASTMCP_SERVER")
fastmcp_server2 = "https://learn.microsoft.com/api/mcp"

toolset1 = FastMCPToolset(fastmcp_server1) if fastmcp_server1 else None
toolset2 = FastMCPToolset(fastmcp_server2)

toolsets = [ts for ts in [toolset1, toolset2] if ts is not None]

BPValidaotor_agent = Agent(
    model=model,
    toolsets=toolsets,
)

app = BPValidaotor_agent.to_a2a()


def _base_url_from_request(request: Request) -> str:
    """
    Derive the public base URL reliably.
    On Azure App Service you typically get correct scheme/host, but if you use a proxy,
    ensure forwarded headers are configured.
    """
    proto = request.headers.get("x-forwarded-proto")
    host = request.headers.get("x-forwarded-host") or request.headers.get("host")

    if proto and host:
        return f"{proto}://{host}/"

    return str(request.base_url).rstrip("/") + "/"


async def microsoft_agent_card(request: Request) -> Response:

    base_url = _base_url_from_request(request)

    card = {
        "name": "BPValidator Agent",
        "description": "Extracts machine service data and validates business partner records.",
        "version": "1.0.0",

        "url": base_url,

        "preferredTransport": "JSONRPC",
        "protocolVersion": "0.3",

        "capabilities": {
            "streaming": True,
            "pushNotifications": False,
        },
        "defaultInputModes": ["text/plain"],
        "defaultOutputModes": ["text/plain"],

        "skills": [
            {
                "id": "bp_validator",
                "name": "Business Partner Validation",
                "description": "Validates and extracts service dispatch fields; can use MCP tools.",
                "tags": ["validation", "dispatch", "mcp", "service"],
                "examples": [
                    "List the types of resources, courses, and learning paths available in MS Learn.",
                    "Extract customer name, BP number, machine number, and issue description from this ticket.",
                ],
            }
        ],
    }

    return JSONResponse(card)


app.router.routes.insert(0, Route("/.well-known/agent.json", microsoft_agent_card, methods=["GET"]))
app.router.routes.insert(0, Route("/.well-known/agent-card.json", microsoft_agent_card, methods=["GET"]))


if __name__ == "__main__":
    import asyncio

    async def main():
        result = await BPValidaotor_agent.run("what tools do you have? names only")
        print(result.output)

    asyncio.run(main())
