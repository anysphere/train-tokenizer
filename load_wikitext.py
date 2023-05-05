from datasets import load_dataset
import heapq

def my_load_dataset():
    """
    Returns an indexable dataset object
    """
    dataset = load_dataset("wikitext", "wikitext-103-v1")
    return dataset["train"]

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

# turn each character into a node
def create_linked_list(string):
    head = Node(None)
    current = head
    for char in string:
        current.next = Node(char)
        current = current.next
    return head

# create linked list from dataset
train = my_load_dataset()
train = train["text"][:1000]
giant_string = "\n".join(train)

# create linked list from giant string
head = create_linked_list(giant_string)
counter = {} # dictionary to keep track of counts of each value

# iterate through linked list and count each value
current = head.next
while current:
    if current.value in counter:
        counter[current.value] += 1
    else:
        counter[current.value] = 1
    current = current.next

character_set = len(set(counter.keys()))

# create heap from counter
heap = []
for key, value in counter.items():
    heapq.heappush(heap, (-1*value, key))

# print top 10 most common characters
for i in range(10):
    print(heapq.heappop(heap))

# pair_counter is heap
pair_counter = {}
current = head.next
while current.next:
    pair = current.value + current.next.value
    if pair in pair_counter:
        pair_counter[pair] += 1
    else:
        pair_counter[pair] = 1
    current = current.next

# create heap from pair_counter
heap = []
for key, value in pair_counter.items():
    heapq.heappush(heap, (-1*value, key))

# merge the most common pair without popping it
while character_set < 1000:
    most_common_pair = heap[0][1]
    print("<|START|>"+most_common_pair+"<|END|>")
    # print 10 most common pairs from heap
    print("10 most common pairs:")
    heap_copy = heap.copy()
    for i in range(10):
        print(heapq.heappop(heap_copy))
    current = head.next
    last = Node("\n")
    last.next = current
    while current.next:
        pair = current.value + current.next.value
        if pair == most_common_pair:
            # update pair_counter
            if pair in pair_counter:
                # remove pair from heap
                heap.remove((-1*pair_counter[pair], pair))
                pair_counter[pair] -= 1
                heapq.heappush(heap, (-1*pair_counter[pair], pair))
            prev_old_pair = last.value + current.value
            next_old_pair = current.next.value + current.next.next.value if current.next.next else None
            if prev_old_pair in pair_counter:
                heap.remove((-1*pair_counter[prev_old_pair], prev_old_pair))
                pair_counter[prev_old_pair] -= 1
                heapq.heappush(heap, (-1*pair_counter[prev_old_pair], prev_old_pair))
            if next_old_pair in pair_counter:
                heap.remove((-1*pair_counter[next_old_pair], next_old_pair))
                pair_counter[next_old_pair] -= 1
                heapq.heappush(heap, (-1*pair_counter[next_old_pair], next_old_pair))
            prev_pair = last.value + pair if last else None
            next_pair = pair + current.next.next.value
            if prev_pair is not None:
                if prev_pair in pair_counter:
                    heap.remove((-1*pair_counter[prev_pair], prev_pair))
                    pair_counter[prev_pair] += 1
                    heapq.heappush(heap, (-1*pair_counter[prev_pair], prev_pair))
                else:
                    pair_counter[prev_pair] = 1
                    heapq.heappush(heap, (-1*pair_counter[prev_pair], prev_pair))
            if next_pair in pair_counter:
                heap.remove((-1*pair_counter[next_pair], next_pair))
                pair_counter[next_pair] += 1
                heapq.heappush(heap, (-1*pair_counter[next_pair], next_pair))
            else:
                pair_counter[next_pair] = 1
                heapq.heappush(heap, (-1*pair_counter[next_pair], next_pair))
            last = current    
            current.value = pair
            current.next = current.next.next
        else:
            last = current 
            current = current.next
    character_set += 1

print("done")
print(heap[:100])
print(len(pair_counter))
print(pair_counter[most_common_pair])
for pair in pair_counter:
    if most_common_pair in pair:
        print(pair)

# keep track of character set and iterate till 1000