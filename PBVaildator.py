from pydantic_ai import Agent
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from pydantic_ai.toolsets.fastmcp import FastMCPToolset


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

system_message = """
You are a Service Dispatch Assistant responsible for extracting machine service data
and validating customer records.
"""
fastmcp_server1 = os.getenv("FASTMCP_SERVER")
fastmcp_server2 = "https://learn.microsoft.com/api/mcp"
toolset1 = FastMCPToolset(fastmcp_server1)
toolset2 = FastMCPToolset(fastmcp_server2)
BPValidaotor_agent = Agent(
    model,
    #system_prompt=system_message,
    toolsets=[toolset1, toolset2]
    
)

app = BPValidaotor_agent.to_a2a()

""" 
if __name__ == "__main__":
    import asyncio
 
    async def main():
        result = await BPValidaotor_agent.run(
            "what tools do you have? names only",
        )
        print(result.output)
        #print((result.output.status))
 
    asyncio.run(main())
"""