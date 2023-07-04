def count_chars(text_url_map):
    return sum([len(text) for ulr, texts in text_url_map.items() for text in texts])

def count_words(text_url_map):
    return sum([len(text.split()) for ulr, texts in text_url_map.items() for text in texts])