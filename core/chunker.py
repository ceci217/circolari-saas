import tiktoken

def chunk_text(text, max_tokens=1200):
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)

    return [
        enc.decode(tokens[i:i+max_tokens])
        for i in range(0, len(tokens), max_tokens)
    ]
