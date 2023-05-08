from datasets import load_dataset as load_dataset2
from tqdm import tqdm
from collections import Counter        
import pickle
import os
import time
from heapq import heappush, heappop, heapify


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

possible_tokens_counter = Counter()
for word, frequency in tqdm(word_counter.items()):
    for start in range(len(word)-2):
        # we don't need to count the frequency of single character tokens
        for end in range(start+2, len(word)):
            possible_tokens_counter[word[start:end]] += frequency

print('counted tokens')

heap = [(-possible_tokens_counter[a+b], a+b) for a in tokens for b in tokens]
already_added = set([h[1] for h in heap])
heapify(heap)

VOCAB_SIZE = 5000
for _ in tqdm(range(VOCAB_SIZE - len(tokens))):
    # find the most common pair of tokens and merge them
    most_common_token = heappop(heap)[1]
    print('added token: ', most_common_token)
    tokens.add(most_common_token)
    # update the heap
    for token in tokens:
        for new_token in [token+most_common_token, most_common_token+token]:
            if new_token not in already_added:
                already_added.add(new_token)
                heappush(heap, (-possible_tokens_counter[new_token], new_token))

    
    
