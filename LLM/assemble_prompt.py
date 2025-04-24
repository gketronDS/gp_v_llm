import os
import pandas as pd
import numpy as np
import csv
import json
import logging
import llmutils

def assemble_prompt(problem_name, train_length, prompt_type, iteration):

    prompt_path = f"./benchmark_problems/{problem_name}/prompt.txt"
    input_path = f"./benchmark_problems/{problem_name}/input.txt"
    output_path = f"./benchmark_problems/{problem_name}/output.txt"
    function_path = f"./benchmark_problems/{problem_name}/function.txt"
    question = []
    for i in [prompt_path, input_path, output_path, function_path]:
        with open(i, "r") as file:
            next = file.read()
            question.append(next)
    # Sanitize the input and log the action
    question_out = llmutils.sanitize_input(question[0])
    #logging.info("Submitting question to OpenAI API: %s", question)
    # Read CSV data
    df = pd.read_csv(f"./benchmark_problems/{problem_name}/{train_length}/{problem_name}_{iteration}_train.csv")
    #json
    indexing = {}
    for i in range(len(df)):
        indexing.update({i: f'Example {i}'})
    
    df = df.rename(index=indexing)
    context = df.to_json(orient="index")
    """Assemble the prompt."""
    noassertstring = ""
    #assert text
    for i in range(len(df)):
        noassertstring += "my_func("
        for j in range(len(df.columns)):
            if df.columns[j][0] == 'i':
                value = df.iloc[i, j]
                noassertstring += f'{value}'
                if df.columns[j+1][0] == 'o':
                    noassertstring += ') == '
                else:
                    noassertstring += ','
            else:
                value = df.iloc[i, j]
                noassertstring += f'{value}'
                if j+1 != len(df.columns):
                    noassertstring += ','
                else:
                    noassertstring += '\n'
    if prompt_type == 'IO':
        submission = f'```python\ndef my_func({question[3]}):\n\
            """Alter this python function "my_func" to accept inputs containing \
            {question[1]}. The function should output {question[2]} that replicates the underlying \
            mechanism of the following examples. Only use base python functions \
            and do not import any packages. Do not include print statements, \
            unit tests, in-line comments or multi-line comments. \
            Examples: {noassertstring}."""```' #Inline request
        return submission
    if prompt_type == 'Prompt':
        submission = f'```python\n{question_out}\ndef my_func({question[3]}):\n\
            """Alter this python function "my_func" to accept inputs containing \
            {question[1]}. The function should output {question[2]}.\
            Only use base python functions and do not import any packages.\
            Do not include print statements, unit tests, in-line comments or\
            multi-line comments."""```'
        return submission
    if prompt_type == 'PromptIO':
        submission = f'```python\n{question_out}\ndef my_func({question[3]}):\n\
            """Alter this python function "my_func" to accept inputs containing\
            {question[1]}. The function should output {question[2]} that replicates the underlying \
            mechanism of the following examples. Only use base python functions \
            and do not import any packages. Do not include print statements, \
            unit tests, in-line comments or multi-line comments. \
            Examples: {noassertstring}."""```' #Inline request
        return submission
    
