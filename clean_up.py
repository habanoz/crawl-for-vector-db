import re

def remove_duplicate_text(url_text_map):
    result = {}
    observed_text = set()

    for url, text_list in url_text_map.items():
        text_list = [t for t in text_list if t not in observed_text]

        observed_text.update(text_list)

        # add to new dict
        result[url] = text_list

    return result


def to_refined_text_map(url_text_map, max_length):
    result = {}

    for url, text_list in url_text_map.items():
        # refine texts
        refined_text_list = refine_text_list(text_list, max_length)

        # remove duplicates
        refined_text_list = list(set(refined_text_list))

        # add to new dict
        result[url] = refined_text_list

    return result

def refine_text_list(texts, minimum_text_length):
    texts = [re.sub(r'(\r\n)+','\n', t) for t in texts] # simplify new lines
    texts = [re.sub(r'\n+','\n',t) for t in texts] # simplify new lines
    texts = [re.sub(r'[ \t\r]+',' ', t) for t in texts] # minimize empty spaces
    texts = [re.sub(r'\s*\n\s*','\n', t) for t in texts] # minimize empty spaces
    texts = [t for t in texts if len(t.strip())>minimum_text_length] # minimum text length filter
    return texts