# Comparing PushGP and GPT-4o on Program Synthesis with only Input-Output Examples

This repository contains code and materials for "Comparn. Below is a detailed README file explaining the 
structure, usage, and other important aspects of this project.

## Introduction
This study analyzed the program synthesis capabilities of genetic
programming and large language models when both are provided
with user intent consisting of input-output examples. We evaluated the
program synthesis performance of PushGP and OpenAI’s GPT-4o
on tasks from the PSB2 suite.

## Installation
To install the required dependencies for running the experiments:

1. Clone this repository.
2. Install Python 3.10 or higher.
3. Install required packages:
```bash
pip install -r requirements.txt
```

## Experiments
A preliminary experiment identify a suitable
prompt from a set of five gathered from existing literature on LLM-
based program synthesis.

After selecting the best prompt, we use the 25 PSB2 tasks to evaluate three program synthesizers: PushGP, GPT-4o with data-only prompts, and GPT-4o with
text-only prompts. 

## How to Run Experiments

## Results and Interpret

PushGP solved 10 tasks, GPT-4o with data-only
prompts solved 8 tasks, and GPT-4o with text-only prompts solved
7 tasks.
Both PushGP and GPT-4o solve overlapping and distinct tasks, suggesting that
neither consistently outperforms the other. Given 7 of the 25
tasks were solved by GPT-4o irrespective of the type of prompt
used, this indicates that GPT-4o is able to retrieve the relevant
information in its training corpus related to the task using both
text-based and data-based prompts. The preference for one
synthesizer over the other may depend on the information available
for a given task.

# Contributions

Contributions are welcome! Please send any suggestions or pull requests to 
[GitHub Issue Tracker](https://github.com/theaksaini/gp_v_llm/issues) or via 
[email](jose.hernandez8@cshs.org).

# License
The code in this repository is distributed under the MIT License. 
See LICENSE.txt for details.

# Citation

```
@conference{theaksainigp_v_llm,
    title = {Comparing PushGP and GPT-4o on Program Synthesis with only 
    Input-Output Examples},
    author = {Jose G Hernandez and Anil K Saini and Gabriel L Ketron 
    and Jason H Moore },
    year = 2025,
    month = {July},
    booktitle = {Proceedings of the Genetic and Evolutionary Computation Conference 
    (GECCO 2025)},
    address = {Malaga, Spain}
    publisher = {ACM},
    doi = {}
}
```

