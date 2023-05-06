from datasets import load_dataset

def ld(k):
    """
    Returns an indexable dataset object
    """
    dataset = load_dataset("wikitext", "wikitext-103-v1")

    return dataset[k]

SPACE = 32

def visualize_bytearray(arr):
    return bytes(arr).decode("utf-8")

def accumulate(x):
    encoded = x.encode("utf-8")
    buffer = []
    
    segments = []
    for c in encoded:
        if c == SPACE:
            if buffer: segments.append(bytes(buffer))
            buffer = []
        buffer.append(c)
    if buffer: segments.append(bytes(buffer))
    return segments

from collections import defaultdict
from tqdm import tqdm 

def collect_tokens(it):
    result_dict = defaultdict(lambda : 0)
    singletons = set()
    for sample in tqdm(it):
        if sample['text']:
            segments = accumulate(sample['text'])
            for s in segments:
                result_dict[s] += 1
            for c in sample['text'].encode("utf-8"): singletons.add(c)
    tokenizer = {bytes([v]):k for k,v in dict(enumerate(singletons)).items()}
    reverse_token_mapping = {k:v for v,k in tokenizer.items()}
    max_token = max(tokenizer.values())
    return result_dict, tokenizer, reverse_token_mapping, max_token

def infer(s, tokenizer, reverse_token_mapping, max_token):
    tokens = []
    token_ids = []
    remaining = s
    
    token_dict = sorted(list(tokenizer.items()), key = lambda x: len(x[0]))
    
    while remaining:
        curr_idx = len(token_dict) - 1
        while curr_idx >= 0:
            token = token_dict[curr_idx][0]
            token_id = token_dict[curr_idx][1]
            #if (len(token) > 1): print(token, token_id, remaining)
            if remaining.startswith(token.decode('latin-1')):
                new_remaining = remaining[len(token):]
                tokens.append(token)
                token_ids.append(token_id)
                remaining = new_remaining
                break
            else:
                curr_idx -= 1
    return tokens, token_ids

def get_max_occurences(train_tokens, tokenizer, reverse_token_mapping, max_token):
    occurences = defaultdict(lambda : 0)
    
    for j, (chunk, weight) in tqdm(enumerate(train_tokens.items()), total = len(train_tokens)):
        #print(j)
        #print(repr(chunk))
        _, token_idx = infer(chunk.decode('latin-1'), tokenizer, reverse_token_mapping, max_token)
        for i in range(len(token_idx) - 1):
            byte_pair = (token_idx[i], token_idx[i+1])
            occurences[byte_pair] += weight
            
    return occurences

def vis_byte_pair(bp, reverse_token_mapping):
    return (reverse_token_mapping[bp[0]] + reverse_token_mapping[bp[1]]).decode('latin-1')

def train(train_tokens, tokenizer, reverse_token_mapping, max_token, it):
    for i in range(it):
        max_occurences = get_max_occurences(train_tokens, tokenizer, reverse_token_mapping, max_token)
        bp = max(max_occurences, key=max_occurences.get)
        max_token += 1
        token = reverse_token_mapping[bp[0]] + reverse_token_mapping[bp[1]]
        tokenizer[token] = max_token
        reverse_token_mapping[max_token] = token
        print(f"Found {token} at iteration {i}")
    return tokenizer, reverse_token_mapping, max_token

if __name__ == "__main__":
    ds = ld('test')
    print('datset loaded')
    train_tokens, tokenizer, reverse_token_mapping, max_token = collect_tokens(ds)
    print('tokens collected')
    tokenizer, reverse_token_mapping, max_token = train(train_tokens, tokenizer, reverse_token_mapping, max_token, 10)
    print(infer("The quick brown fox jumps over the lazy dog", tokenizer, reverse_token_mapping, max_token))