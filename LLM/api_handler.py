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

class AzureAPIHandler:
    def __init__(self, dataset_name, api_key=None, base_url=None, 
                api_version=None, deployment_name=None):
        self.api_key = os.environ.get('AZURE_OPENAI_API_KEY')
        self.base_url = os.environ.get('AZURE_OPENAI_ENDPOINT')
        self.api_version = "2024-02-01"
        self.model = "gpt-4o"
        self.client = openai.AzureOpenAI(
            azure_endpoint=os.environ.get('AZURE_OPENAI_ENDPOINT'),
            api_key=os.environ.get('AZURE_OPENAI_API_KEY'),
            api_version="2024-02-01"
        )
        self.name = dataset_name

    def submit_question(self, question, csv_path, portion, iteration = 42, prompt='chen_equals'):
        self.iteration = iteration
        # Sanitize the input and log the action
        question_out = sanitize_input(question[0])
        #logging.info("Submitting question to OpenAI API: %s", question)

        # Read CSV data
        df = pd.read_csv(csv_path)
        #json
        indexing = {}
        for i in range(len(df)):
            indexing.update({i: f'Example {i}'})
        
        df = df.rename(index=indexing)
        context = df.to_json(orient="index")

        assertstring = ""
        #assert text
        for i in range(len(df)):
            assertstring += "assert my_func("
            for j in range(len(df.columns)):
                if df.columns[j][0] == 'i':
                    value = df.iloc[i, j]
                    assertstring += f'{value}'
                    if df.columns[j+1][0] == 'o':
                        assertstring += ') == '
                    else:
                        assertstring += ','
                else:
                    value = df.iloc[i, j]
                    assertstring += f'{value}'
                    if j+1 != len(df.columns):
                        assertstring += ','
                    else:
                        assertstring += '\n'
                    
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

        returnstring = ""
        #assert text
        for i in range(len(df)):
            returnstring += "my_func("
            for j in range(len(df.columns)):
                if df.columns[j][0] == 'i':
                    value = df.iloc[i, j]
                    returnstring += f'{value}'
                    if df.columns[j+1][0] == 'o':
                        returnstring += ') returns '
                    else:
                        returnstring += ','
                else:
                    value = df.iloc[i, j]
                    returnstring += f'{value}'
                    if j+1 != len(df.columns):
                        returnstring += ','
                    else:
                        returnstring += '\n'

        #pure text
        textstring = "```" + df.columns.values + "\n"
        for i in range(len(df)):
            for j in range(len(df.columns)):
                textstring += f'{df.iloc[i, j]}'
                if j+1 != len(df.columns):
                            textstring += ','
                else:
                    textstring += '\n'
        textstring += "```"

        #context text
        contextstring = "```\n| "
        for j in range(len(df.columns)):
            contextstring += df.columns[j]
            if j+1 != len(df.columns):
                        contextstring += ' | '
            else:
                contextstring += ' |\n'
        contextstring += "|----------------------------|\n"
        for i in range(len(df)):
            contextstring += '| '
            for j in range(len(df.columns)):
                value = df.iloc[i, j]
                contextstring += f'{value}'
                if j+1 != len(df.columns):
                    contextstring += ' | '
                else:
                    contextstring += ' |\n'
        contextstring += "```"

        match prompt:
            case 'chen_returns':
                submission_prompt =  f'```python\ndef my_func({question[3]}): \n    \
                """Alter this python function "my_func" to accept inputs containing \
                {question[1]}. The function should output {question[2]} that replicates the underlying \
                mechanism of the following examples. Do not import packages other than \
                numpy or math. Examples: {returnstring}.\n\
                """\n```' #Inline request
            case 'chen_equals':
                submission_prompt =  f'```python\ndef my_func({question[3]}): \n    \
                """Alter this python function "my_func" to accept inputs containing \
                {question[1]}. The function should output {question[2]} that replicates the underlying \
                mechanism of the following examples. Do not import packages other than \
                numpy or math. Examples: {noassertstring}.\n\
                """\n```' #Inline request
            case 'chen_equals_text_only':
                submission_prompt =  f'```python\n{question_out}\ndef my_func({question[3]}): \n    \
                """Alter this python function "my_func" to accept inputs containing \
                {question[1]}. The function should output {question[2]}. Do not import packages other than \
                numpy or math.\n \
                """\n```'
            case 'shalinbars':
                submission_prompt =  f'{contextstring} \n Write a python function "my_func" \
                that best fits the data within the triple barticks. The \
                data consists of inputs containing {question[1]}. The function should \
                output {question[2]}. Do not import packages other than numpy or math.'
            case 'sharlincsv':
                submission_prompt =  f'{textstring}\nWrite a python function "my_func" \
                that best fits the data in CSV format within the triple barticks. The \
                data consists of inputs containing {question[1]}. The function should \
                output {question[2]}. Do not import packages other than numpy or math.'  #before w/o explian steps
            case 'austin':
                submission_prompt = f'Write a python function "my_func" \
                that best fits the examples with inputs containing \
                {question[1]}. The function should output {question[2]}. Do not import packages other \
                than numpy or math. Your code should satisfy these tests: {assertstring}'  #before w/o explian steps
        
        conversation = [
                {"role": "system", "content":""},
                {"role": "user", "content": submission_prompt}
            ]
        
        #print(submission_prompt)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=conversation,
            seed = self.iteration, #allows for reproducable variations with 100 runs
            temperature=0.7,
            #top_p=0.95
        )

        # Print the response
        print(response.model_dump_json(indent=2))
        print(response.choices[0].message.content)
        response_json = response.choices[0].message.content
        validation_flag, function_response = verify_response(response_json)
        #print(validation_flag)
        #print(function_response)
        if validation_flag:
            self.save_response(question, context, function_response, portion, prompt)
            #logging.info("Response saved successfully.")
        else:
            logging.warning(
                "Response from '%s' did not contain valid executable code.", 
                question
            )
        return function_response

    def save_response(self, question, context, response_json, portion, prompt):

        if not os.path.exists(f"datasets/{self.name}/{portion}/responses"):
            os.makedirs(f"datasets/{self.name}/{portion}/responses")
        try:
            with open(f"datasets/{self.name}/{portion}/responses/{self.name}_{self.iteration}_"+prompt+"_responses.json", "a") as file:
                entry = {
                    "question": question,
                    "context": context,
                    "response": response_json
                }
                file.write(json.dumps(entry) + "\n")
            #logging.info("Response logged to file.")
        except Exception as err:
            logging.error("Failed to save response: %s", err)