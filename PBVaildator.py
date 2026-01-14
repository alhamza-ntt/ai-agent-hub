from pydantic_ai import Agent
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from pydantic_ai.toolsets.fastmcp import FastMCPToolset

from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import Response

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
toolset1 = FastMCPToolset(fastmcp_server1)
toolset2 = FastMCPToolset(fastmcp_server2)

BPValidaotor_agent = Agent(
    model,
    toolsets=[toolset1, toolset2],
)

app = BPValidaotor_agent.to_a2a()



async def agent_json_alias(request: Request) -> Response:
    return await app._agent_card_endpoint(request)  

app.router.routes.insert(
    0,
    Route("/.well-known/agent.json", endpoint=agent_json_alias, methods=["GET"]),
)

if __name__ == "__main__":
    import asyncio

    async def main():
        result = await BPValidaotor_agent.run("what tools do you have? names only")
        print(result.output)

    asyncio.run(main())
