import os
import pandas as pd
import numpy as np
import csv
from itertools import product
import json
import logging
import llmutils
from assemble_prompt import assemble_prompt
import argparse
import api_handler
from datautils import generate_training_test_data

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

parser = argparse.ArgumentParser(description="Connect to your API using an LLM.")
parser.add_argument('--llm', type=str, default='AzureOpenAI')
parser.add_argument('--test', type=bool, default='False')
parser.add_argument('--problemfolder', type=str)
parser.add_argument('--codefolder', type=str)


# Parse arguments
args = parser.parse_args()
llm_name = args.llm
test = args.test
problem_folder = args.problemfolder
code_folder = args.codefolder

# Example usage:
if not test:
    first_path = llmutils.list_folders(problem_folder)  # Current directory
    second_path = ['200', '50']#llmutils.list_folders(problem_folder+"/basement")
    prompt_types = ["Prompt", "IO"]
    iterations = 100
else: 
    first_path = ['basement', 'bouncing-balls', 'bowling', 'camel-case', 
                 'coin-sums', 'cut-vector', 'dice-game', 'find-pair', 
                 'fizz-buzz', 'fuel-cost', 'gcd',  'indices-of-substring',  
                 'leaders', 'luhn', 'mastermind',  'middle-character',  
                 'paired-digits', 'snow-day',  'solve-boolean',
                   'spin-words', 'square-digits','substitution-cipher'] # Current directory
    second_path = ['200', '50']
    prompt_types = ["Prompt", "IO"]
    iterations = 100


def main(problem_names, train_length, prompt_types, iterations):
    """Direct arguements form a script and give to the loop function."""
    client = api_handler.get_client(llm_name)
    print(problem_names)
    print(train_length)
    print(prompt_types)
    loop_through(problem_names, train_length, prompt_types, iterations, client)
    print('Run Finished')


def loop_through(problem_names, train_length, prompt_types, iterations, client):
    """Assemble prompts, submit to the api, and save the result."""
    for problem_name in problem_names:
        for train_count in train_length:
            for prompt_type in prompt_types:
                for i in range(iterations):
                    generate_training_test_data(problem_folder, problem_name, 
                                                rand_seed=i, portion=train_count)
                    submission = assemble_prompt(problem_name, train_count, 
                                                 prompt_type, i)
                    print(submission)
                    response = client.submit_question(submission, i)
                    print(response)
                    save_response(submission, response, 
                                  problem_name, 
                                  train_count, 
                                  prompt_type, 
                                  i)
                    print(f"{i} Complete")
                print(f"{prompt_type} Complete")
            print(f"{train_count} Complete")
        print(f"{problem_name} Complete")

def save_response(submission, response, problem_name, train_count, prompt_type, i):
    """Save the response."""
    if not os.path.exists(code_folder+f"/{problem_name}/{train_count}/{prompt_type}"):
        os.makedirs(code_folder+f"/{problem_name}/{train_count}/{prompt_type}")
    try:
        with open(code_folder+f"/{problem_name}/{train_count}/{prompt_type}/response_{i}.json", "a") as file:
            entry = {"submission": submission, "response": response}
            file.write(json.dumps(entry) + "\n")
    except Exception as err:
        logging.error("Failed to save response: %s", err)

if __name__ == "__main__":
    main(first_path, second_path, prompt_types, iterations)