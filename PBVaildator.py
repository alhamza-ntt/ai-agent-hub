import uvicorn
#from utils import create_model
from pydantic_ai.toolsets.fastmcp import FastMCPToolset
from dotenv import load_dotenv
import os
load_dotenv()
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel, OpenAIResponsesModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai import Agent
from pydantic_ai.toolsets.fastmcp import FastMCPToolset
from dotenv import load_dotenv
import os
load_dotenv()



from pydantic import BaseModel

class BPValidatorOutput(BaseModel):
    customer_name: str
    business_partner_number: str
    location: str
    machine_number: str
    problem_description: str
    status: str


def create_model(llm_model: str = 'gpt-5-chat'):
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
Task:
1. Extract the following fields from the user input:
customer_name, 
business_partner_number,
location, 
machine_number, 
and problem_description
2. Validate: If a business_partner_number is found, immediately use the get_business_partner tool to verify the ID. 
3. Analyze: Check if any of the five fields are null or "missing".
Status Assignment (MANDATORY):
- You MUST set the status field.
- If all five fields are present and valid, set status exactly to "READY_FOR_PROCESSING".
- If ANY field is missing, empty, or invalid, set status exactly to "DRAFTING_EMAIL".
- Never leave status empty.

"""

"""
fastmcp_server = os.getenv("FASTMCP_SERVER")

toolset = FastMCPToolset(fastmcp_server)
toolsets=[toolset]
"""
BPValidaotor_agent = Agent(model, system_prompt=system_message, output_type=BPValidatorOutput)

if __name__ == "__main__":
    app = BPValidaotor_agent.to_a2a()
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)


"""
if __name__ == "__main__":
    import asyncio

    async def main():
        result = await BPValidaotor_agent.run(
            ''' business partner number is 10300001, located in New York.
            The machine number is M12345 and the problem description is 'The machine is overheating frequently.'
            '''
        )
        print(result.output)
        #print((result.output.status))

    asyncio.run(main())
 """