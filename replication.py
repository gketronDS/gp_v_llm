import logging
import os
import pandas as pd
import json
from LLM.llmutils import verify_response, sanitize_input
import openai

client = openai.AzureOpenAI(
    azure_endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT'),
    api_key = os.environ.get('AZURE_OPENAI_API_KEY'),
    api_version = "2024-02-01"
)
conversation = [
    {"role": "system", "content": ""},
    {"role": "user", "content": "Testing"}
]

response = client.chat.completions.create(
    model='gpt-4o',
    messages = conversation,
    seed=42,
    temperature = 0.7
)

print(response.choices[0].message.content)