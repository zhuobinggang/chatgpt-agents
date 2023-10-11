import chromadb

def get_client():
    client = chromadb.PersistentClient(path='./survival_game')
    return client

def save_text(text, collection, prefix = '', suffix = ''):
    index = collection.count()
    collection.add(ids = [str(index)], documents = [f'{prefix} {text} {suffix}'])

def query(text, collection, n_results = 3):
    results = collection.query(query_texts = [text], n_results = 3)
    return results


