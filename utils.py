from pydantic_ai.models.openai import OpenAIChatModel, OpenAIResponsesModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai import Agent
from pydantic_ai.toolsets.fastmcp import FastMCPToolset
from dotenv import load_dotenv
import os
load_dotenv()


fastmcp_server = "https://pacbusinesspartner.cfapps.eu10-005.hana.ondemand.com/mcp"
toolset = FastMCPToolset(fastmcp_server)

def create_model(llm_model: str = 'gpt-5-chat'):
    return OpenAIResponsesModel(
        model_name=llm_model,
        provider=OpenAIProvider(
            base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        ),
    )

model = create_model()

fastmcp_server = "https://pacbusinesspartner.cfapps.eu10-005.hana.ondemand.com/mcp"
toolset = FastMCPToolset(fastmcp_server)

""" 
async def main():
    result = await agent.run('check business partner with id 10000019')
    print(result)
    print()
    print(result.output)
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
"""