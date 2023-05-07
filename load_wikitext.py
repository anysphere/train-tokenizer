from datasets import load_dataset

def load_dataset():
    """
    Returns an indexable dataset object
    """
    dataset = load_dataset("wikitext", "wikitext-103-v1")

    return dataset['train']


data = "the fat cat walked over the hill"

vocab = [chr(i) for i in range(ord('a'), ord('z')+1)] + [' ']
# class Node:
#     def __init__(self, data):
#         self.data = data
#         self.next = None

# tokens = Node(data[0])
# current_node = tokens
# for c in data[1:]:
#     new_node = Node(c)
#     current_node.next = new_node
#     current_node = new_node


indices_dict = {}
for index, character in enumerate(data):
    indices_dict[character].append(index)

freq_dict = {char : {char : 0 for char in vocab} for char in vocab}
for i, _ in enumerate(data[:-1]):
    freq_dict[data[i]][data[i+1]]+=1

# Convert freq_dict entries to a set
all_freq_entries = set()
for outer_key in freq_dict:
    for inner_key in freq_dict[outer_key]:
        all_freq_entries.add((outer_key, inner_key, freq_dict[outer_key][inner_key]))

"""
t1 t2 = t3

[t1][t2] -> 0
[t3] = # of t2s that follow a t1
[t2] = 

"""

def get_token(idx):
    pass

while len(vocab) < 2:
    t1, t2, _ = max(all_freq_entries, key=lambda x: x[2]) 

    freq_dict[t1+t2] = {}
    
    for i in indices_dict[t1]:
        if get_token(i + len(t1)) == t2:
            all_freq_entries.remove((t1, t2, freq_dict[t1][t2]))
            all_freq_entries.add((t1, t2, freq_dict[t1][t2] - 1))
            freq_dict[t1][t2] -= 1




