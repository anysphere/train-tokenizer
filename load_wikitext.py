from datasets import load_dataset

def load_dataset():
    """
    Returns an indexable dataset object
    """
    dataset = load_dataset("wikitext", "wikitext-103-v1")

    return dataset['train']


