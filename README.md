# Training Tokenizer

Your goal is to implement a BPE Tokenizer with reasonable training and efficient inference

## Background
BPE means byte pair encoding. The algorithm is relatively simple and involves the following steps:

1. Split up all words by whitespace. The sentence: "The fat cat walked over the hill." should be: `['The', ' fat', ' cat', ' walked', ' over', ' the', ' hill']`. Note that spaces are kept in front of words when appropriate.
2. Our initial set of tokens will be all characters in our corpus of text.
3. For each pair tokens (in the beginning, these are just characters), find the most common pair. For the original sentence, this would be 'he' or 'at'. Merge these pair of tokens to create a new token.
4. Repeat step 3 until your vocabulary size is sufficiently large. Try to get a vocab size of 1000-5000 for now.

## Dataset
You can get a sizeable corpus of text from `load_wikitext.py`. You will need to run `pip install -r requirements.txt` before using it. You may use whatever fraction of the dataset you deem appropriate to train the tokenizer.

Note that too large a size may take far too long to train and too small a size may not result in wide enough token coverage.

## Requirements
You should provide a function that can train the BPE model, and stores/saves the tokens you've learned to disk

You should provide a function that loads the stored tokens and can efficiently encode and decode strings of text

You can choose to spend more time on optimizing inference or training. The choice is yours.
