import pandas as pd
import csv
import os

PSB2_DATASETS = ['basement', 'bouncing-balls', 'bowling', 'camel-case', 
                 'coin-sums', 'cut-vector', 'dice-game', 'find-pair', 
                 'fizz-buzz', 'fuel-cost', 'gcd',  'indices-of-substring',  
                 'leaders', 'luhn', 'mastermind',  'middle-character',  
                 'paired-digits', 'shopping-list', 'snow-day',  'solve-boolean',
                   'spin-words', 'square-digits','substitution-cipher', 
                   'twitter', 'vector-distance']

FULL_QUERY = ['Given a vector of integers, return the first index such that \
            the sum of all integers from the start of the vector to that \
            index (inclusive) is negative.', 'Given a starting height and \
            a height after the first bounce of a dropped ball, calculate \
            the bounciness index (height of first bounce / starting height). \
            Then, given a number of bounces, use the bounciness index to \
            calculate the total distance that the ball travels across those \
            bounces.', 'Given a string representing the individual bowls in a \
            10-frame round of 10 pin bowling, return the score of that round.',
            'Take a string in kebab-case and convert all of the words to \
            camelCase. Each group of words to convert is delimited by "-", \
            and each grouping is separated by a space. For example: \
            "camel-case example-test-string"->"camelCase exampleTestString".', 
            'Given a number of cents, find the fewest number of US coins \
            (pennies, nickles, dimes, quarters) needed to make that amount, \
            and return the number of each type of coin as a separate output.',
            'Given a vector of positive integers, find the spot where, \
            if you cut the vector, the numbers on both sides are either equal, \
            or the difference is as small as possible. Return the two resulting\
             subvectors as two outputs.', 'Peter has an n sided die and Colin \
            has an m sided die. If they both roll their dice at the same time, \
            return the probability that Peter rolls strictly higher than Colin.',
            'Given a vector of integers, return the two elements that sum to a \
            target integer.', 'Given an integer x, return "Fizz" if x is \
            divisible by 3, "Buzz" if x is divisible by 5, "FizzBuzz" if x \
            is divisible by 3 and 5, and a string version of x if none of the \
            above hold.', 'Given a vector of positive integers, divide each by \
            3, round the result down to the nearest integer, and subtract 2. \
            Return the sum of all of the new integers in the vector.', 
            'Given two integers, return the largest integer that divides each \
            of the integers evenly.', 'Given a text string and a target string,\
             return a vector of integers of the indices at which the target \
            appears in the text. If the target string overlaps itself in the \
            text, all indices (including those overlapping) should be returned.',
            'Given a vector of positive integers, return a vector of the \
            leaders in that vector. A leader is defined as a number that is \
            greater than or equal to all the numbers to the right of it. The \
            rightmost element is always a leader.', 'Given a vector of 16 \
            digits, implement Luhn\'s algorithm to verify a credit card number,\
             such that it follows the following rules: double every other digit\
             starting with the second digit. If any of the results are over 9, \
            subtract 9 from them. Return the sum of all of the new digits.',
            'Based on the board game Mastermind. Given a Mastermind code and a \
            guess, each of which are 4-character strings consisting of 6 \
            possible characters, return the number of white pegs (correct \
            color, wrong place) and black pegs (correct color, correct place) \
            the codemaster should give as a clue.', 'Given a string, return \
            the middle character as a string if it is odd length; return the \
            two middle characters as a string if it is even length.',
            'Given a string of digits, return the sum of the digits whose \
            following digit is the same.', 'Given a vector of floats \
            representing the prices of various shopping goods and another \
            vector of floats representing the percent discount of each of \
            those goods, return the total price of the shopping trip after \
            applying the discount to each item.', 'Given an integer \
            representing a number of hours and 3 floats representing how much \
            snow is on the ground, the rate of snow fall, and the proportion \
            of snow melting per hour, return the amount of snow on the ground \
            after the amount of hours given. Each hour is considered a \
            discrete event of adding snow and then melting, not a continuous \
            process.', 'Given a string representing a Boolean expression \
            consisting of T, F, |, and &, evaluate it and return the resulting \
            Boolean.', 'Given a string of one or more words (separated by \
            spaces), reverse all of the words that are five or more letters \
            long and return the resulting string.', 'Given a positive integer, \
            square each digit and concatenate the squares into a returned \
            string.', 'This problem gives 3 strings. The first two represent a \
            cipher, mapping each character in one string to the one at the \
            same index in the other string. The program must apply this cipher \
            to the third string and return the deciphered message.',
            'Given a string representing a tweet, validate whether the tweet \
            meets Twitter\'s original character requirements. If the tweet has \
            more than 140 characters, return the string "Too many characters". \
            If the tweet is empty, return the string "You didn\'t type \
            anything". Otherwise, return "Your tweet has X characters", where \
            the - is the number of characters in the tweet.', 'Given two \
            n-dimensional vectors of floats, return the Euclidean distance \
            between the two vectors in n-dimensional space.']

EMPTY_QUERY = [['','a vector of integers of length [1, 20] with each integer in [−100, 100]','an integer', 'input1', 0],
            ['', 'a float in [1.0, 100.0], float in [1.0, 100.0], integer in [1, 20]', 'a float', 'input1:float, input2:float, input3:int', 0], 
            ['', 'a string in form of completed bowling card, with one character per roll','an integer', 'input1:str', 0], 
            ['', 'a string of length [1, 20]', 'a string', 'input1:str', 0], 
            ['', 'an integer in [1, 10000]','4 integers', 'input1:int', 0], 
            ['', 'a vector of integers of length [1, 20] with each integer in [1, 10000]', '2 vectors of integers', 'input1', 0],
            ['','2 integers in [1, 1000]','a float', 'input1:int, input2:int', 0],
            ['','a vector of integers of length [2, 20] with each integer in [-10000, 10000], integer in [-20000, 20000]','2 integers', 'input1, input2:int', 0],
            ['','an integer in [1, 1000000]','a string', 'input1:int', 0],
            ['','a vector of integers of length [1, 20] with each integer in [6, 100000]','an integer', 'input1', 0],
            ['','2 integers in [1, 1000000]','an integer', 'input1:int, input2:int', 0],
            ['','2 strings of length [1, 20]','a vector of integers', 'input1:str, input2:str', 0],
            ['','a vector of integers of length [0, 20] with each integer in [0, 1000]','a vector of integers', 'input1', 0],
            ['','a vector of integers of length 16 with each integer in [1, 9]','an integer', 'input1', 0],
            ['','2 strings of length 4 made of B, R, W, Y, O, G','2 integers', 'input1:str, input2:str', 0], 
            ['','a string of length [1, 100]','a string', 'input1:str', 0],
            ['','a string of digits of length [2, 20]','an integer', 'input1:str', 0], 
            ['','a vector of floats of length [1, 20] with each float in [0.0, 50.0], a vector of floats of length [1, 20] with each float in [0.0, 100.0] where both vectors must be the same length',' a float', 'input1, input2', 0],
            ['','an integer in [0, 20],a float in [0.0, 20.0],a float in [0.0, 10.0],a float in [0.0, 1.0]','a float', 'input1:int, input2:float, input3:float, input4:float', 0],
            ['','a string of length [1, 20] made of characters from {t, f, |, &}','a Boolean', 'input1:str', 0],
            ['','a string of length [0, 20]','a string', 'input1:str', 0],
            ['','an integer in [0, 1000000]','a string', 'input1:int', 0],
            ['','3 strings of length [0, 26]','a string', 'input1:str, input2:str, input3:str',0 ],
            ['','string of length [0, 200]','a string', 'input1:str', 0],
            ['','2 vectors of floats of length [1, 20] with each float in [-100.0, 100.0]','a float', 'input1, input2', 0]]



def generate_training_test_data(data_dir, dataset_name, rand_seed, portion):
    '''
    Read from two csv files corresponding to a dataset containg 'edge cases' and 'random cases'.
    Create dataframes X_train and Y_train of size 200 that includes all egde cases and, if neddeed, rest from random cases dataset. 
    X_test and Y_test contain 2000 cases from random cases.

    Parameters:
    data_dir: str: directory containing the dataset
    dataset_name: str: name of the dataset
    rand_seed: int: random seed for reproducibility

    Returns:
    X_train, y_train, X_test, y_test: DataFrames: training and testing data
    '''

    edge_case = pd.read_csv(f"{data_dir}/{dataset_name}/{dataset_name}-edge.csv")
    random_cases = pd.read_csv(f"{data_dir}/{dataset_name}/{dataset_name}-random.csv")

    # Ensure we have 200 training cases
    train = pd.concat([edge_case, random_cases.sample(n=int(portion) - len(edge_case), 
                                                      random_state=rand_seed)])
    train = train.sample(frac=1).reset_index(drop=True)
    input_cols = [col for col in train.columns if col.startswith("input")]
    train.to_csv(f"{data_dir}/{dataset_name}/{str(portion)}/{dataset_name}_{rand_seed}_train.csv", 
                 index=False)
    X_train = train[input_cols]
    y_train = train.drop(columns=input_cols)
    
    # Ensure we have 2000 test cases
    val_test = random_cases.sample(n=2200, random_state=rand_seed)
    val = val_test.iloc[:200]
    test = val_test.iloc[200:]
    input_cols = [col for col in val.columns if col.startswith("input")]
    val.to_csv(f"{data_dir}/{dataset_name}/{str(portion)}/{dataset_name}__{rand_seed}_val.csv",
                 index=False)
    X_val = val[input_cols]
    y_val = val.drop(columns=input_cols)

    test.to_csv(f"{data_dir}/{dataset_name}/{str(portion)}/{dataset_name}__{rand_seed}_test.csv",
                 index=False)
    X_test = test[input_cols]
    y_test = test.drop(columns=input_cols)

    return X_train, y_train, X_test, y_test


def write_prompt_text(data_dir, dataset_name, text_to_write, file_name):
    file_path = f"{data_dir}/{dataset_name}/{file_name}.txt"
    if os.path.exists(file_path):
        print(f"File '{file_path}' exists.")
        with open(f"{data_dir}/{dataset_name}/{file_name}.txt", "w") as file:
            file.write(text_to_write)
            file.close()
    else:
        # Create the file if it doesn't exist
        with open(file_path, 'w') as file:
            file.write(text_to_write)
            file.close()
        print(f"File '{file_path}' created.")


'''
for i, names in enumerate(PSB2_DATASETS):
    text_to_write = FULL_QUERY[i]
    write_prompt_text('source', names, text_to_write, "prompt")
    text_to_write = EMPTY_QUERY[i]
    write_prompt_text('source', names, text_to_write[1], "input")
    write_prompt_text('source', names, text_to_write[2], "output")
    write_prompt_text('source', names, text_to_write[3], "function")
    print(names)
    print("DONE")
'''
'''
for i, names in enumerate(PSB2_DATASETS):
    for j in [200, 100, 50]:
        for k in ["GP", "IO", "Prompt"]:
            for l in ["logs", "data"]:
                if not os.path.exists(f"{l}/{names}/{j}/{k}"):
                    os.makedirs(f"{l}/{names}/{j}/{k}")
    print(names)
    print("DONE")
'''
'''
for i, names in enumerate(PSB2_DATASETS):
    for j in [200, 100, 50]:
        if not os.path.exists(f"source/{names}/{j}"):
            os.makedirs(f"source/{names}/{j}")
    print(names)
    print("DONE")
'''
'''
def list_folders(directory):
    """Lists all folders in a given directory.

    Args:
        directory: The path to the directory.

    Returns:
        A list of folder names in the directory.
    """
    return [item for item in os.listdir(directory) if os.path.isdir(os.path.join(directory, item))]

# Example usage:
directory_path = "./source/basement"  # Current directory
folders = list_folders(directory_path)
print(folders)
'''
"""
for names in PSB2_DATASETS:
    for i in [200, 50]:
        X_train, y_train, X_test, y_test = generate_training_test_data(data_dir=\
            'benchmark_problems', dataset_name=names, rand_seed=42, portion=i)
        print(X_train, y_train, X_test, y_test, i)
    print(names)
    print("DONE")
"""
