from pydantic_ai import Agent
from pydantic import BaseModel
from dotenv import load_dotenv
import os

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

BPValidaotor_agent = Agent(
    model,
    system_prompt=system_message,
    output_type=BPValidatorOutput,
)

# THIS is what Azure will run
app = BPValidaotor_agent.to_a2a()
