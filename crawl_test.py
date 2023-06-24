from clean_up import to_refined_text_map, remove_duplicate_text
from dfs_div_crawler import dfs_crawl

def count_chars(text_url_map):
    return sum([len(text) for ulr, texts in text_url_map.items() for text in texts])

def count_words(text_url_map):
    return sum([len(text.split()) for ulr, texts in text_url_map.items() for text in texts])

def main():
    main_page_url = "https://en.wikipedia.org/wiki/Turkey"
    urls_read_set = set()
    url_text_map = {}

    exclusion_filters = [lambda path: path.startswith("cdn"), lambda path: ".aspx" in path]
    dfs_crawl(main_page_url, urls_read_set, url_text_map, exclusion_filters, max_depth=1, max_urls=50)

    print(count_chars(url_text_map)) # prints 2419445
    print(count_words(url_text_map)) # prints 322837

    refined_url_text_map = to_refined_text_map(url_text_map, 60)
    print(count_chars(refined_url_text_map)) # prints 2285403
    print(count_words(refined_url_text_map)) # prints 309943

    removed_duplicates_text = remove_duplicate_text(refined_url_text_map)
    print(count_chars(removed_duplicates_text)) # prints 1759770
    print(count_words(removed_duplicates_text)) # prints 233556

if __name__ == '__main__':
    main()