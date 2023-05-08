from datasets import load_dataset as load_dataset2
from tqdm import tqdm
from collections import Counter        
import pickle
import os
import time

def load_dataset():
    """
    Returns an indexable dataset object
    """
    dataset = load_dataset2("wikitext", "wikitext-103-v1")

    return dataset['train']

# print(type(load_dataset()))
# print(load_dataset()[0])
dataset = load_dataset()

# dataset is a list of dictionaries with the key text, iterate through the dataset, split each text by whitespaces, and keep a counter of all text

# Check if word_counter.pkl exists
if not os.path.exists("word_counter.pkl"):
    # Create a counter to count and store the frequency of words
    word_counter = Counter()

    # Iterate through the dataset, split each text by whitespaces, and update the counter
    for i in tqdm(range(len(dataset))):
        entry = dataset[i]
        words = entry['text'].split()
        word_counter.update(words)
        
    # Save the word_counter object using pickle
    with open("word_counter.pkl", "wb") as f:
        pickle.dump(word_counter, f)

# Load the word_counter object using pickle
with open("word_counter.pkl", "rb") as f:
    word_counter = pickle.load(f)

# Display the counter results
# print(word_counter)
# print total number of unique words
# print(f"Total number of unique words: {len(word_counter)}")
# print(f"Most common words: {word_counter.most_common(10)}")
# print(f"Total number of words: {sum(word_counter.values())}")

tokens = set()
for w in word_counter:
    for char in w:
        tokens.add(char)

print('initial tokens: ', tokens)
print('number of initial tokens: ', len(tokens))

VOCAB_SIZE = 5000
for _ in tqdm(range(VOCAB_SIZE - len(tokens))):
    # find the most common pair of tokens and merge them
    possible_tokens_counter = Counter({a+b: 0 for a in tokens for b in tokens if (a+b) not in tokens})
    assert sum(possible_tokens_counter.values()) == 0 
    for word, frequency in word_counter.items():
        for start in range(len(word)-1):
            for end in range(start+1, len(word)):
                if word[start:end] in possible_tokens_counter:
                    possible_tokens_counter[word[start:end]] += frequency

    most_common_token = possible_tokens_counter.most_common(1)[0][0]
    print('added token: ', most_common_token)
    tokens.add(most_common_token)
    
    
