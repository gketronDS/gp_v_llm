import logging
import os
import pandas as pd
import json
from llmutils import verify_response, sanitize_input
import openai

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_client(client_name):
    """Returns an instance of the client handler."""
    # Set up your OpenAI API key and endpoint
    match client_name:
        case "AzureOpenAI":
            return AzureAPIHandler()
        case _:
            raise ValueError(f"Invalid client name: {client_name}")

class AzureAPIHandler:
    def __init__(self, dataset_name=None, api_key=None, base_url=None, 
                api_version=None, deployment_name=None):
        self.api_key = os.environ.get('AZURE_OPENAI_API_KEY')
        self.base_url = os.environ.get('AZURE_OPENAI_ENDPOINT')
        self.api_version = "2024-02-01"
        self.model = "gketron-4o"
        self.client = openai.AzureOpenAI(
            azure_endpoint=os.environ.get('AZURE_OPENAI_ENDPOINT'),
            api_key=os.environ.get('AZURE_OPENAI_API_KEY'),
            api_version="2024-02-01"
        )

    def submit_question(self, submission, iteration=42):
        conversation = [
                {"role": "system", "content":""},
                {"role": "user", "content": submission}
            ]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=conversation,
            seed = iteration, 
            temperature=0.7,
        )
        return response.choices[0].message.content