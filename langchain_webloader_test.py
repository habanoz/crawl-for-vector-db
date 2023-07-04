from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from numpy import mean
from langchain.text_splitter import TokenTextSplitter

from clean_up import to_refined_text_map, remove_duplicate_text
import os

from word_utils import count_words

MIN_LENGTH_CHAR = 0
MIN_LENGTH_WORD = 2
CHUNK_SIZE = 500
OVERLAP = 50

def main():
    main_page_url = "https://www.bbc.com/"
    news1 = "https://www.bbc.com/news/live/world-middle-east-66085089"
    news2 = "https://www.bbc.com/news/world-europe-66094744"
    news3 = "https://www.bbc.com/news/av/world-middle-east-66093147"

    news4 = "https://www.bbc.com/future/article/20230703-why-our-voices-change-with-age"
    news5 = "https://www.bbc.com/culture/article/20230702-11-of-the-best-tv-shows-to-watch-this-july"
    news6 = "https://www.bbc.com/sport/football/65889461"

    loader = WebBaseLoader([main_page_url, news1, news2, news3, news4, news5, news6])
    #loader = WebBaseLoader([main_page_url, news1, news2, news3])
    #loader = WebBaseLoader([main_page_url])
    data = loader.load()

    url_text_map = {page.metadata['source']: [page.page_content] for page in data}

    print("MIN_LENGTH_CHAR {}, MIN_LENGTH_WORD {}, CHUNK_SIZE {}, OVERLAP {}".format(MIN_LENGTH_CHAR, MIN_LENGTH_WORD, CHUNK_SIZE, OVERLAP))
    print("Page text words: ", count_words(url_text_map))

    refined_url_text_map = to_refined_text_map(url_text_map, MIN_LENGTH_CHAR, MIN_LENGTH_WORD)
    print("Words after refining: ", count_words(refined_url_text_map))

    removed_duplicates_text = remove_duplicate_text(refined_url_text_map)
    print("Words after duplicate removal: ", count_words(removed_duplicates_text))

    #text_splitter = RecursiveCharacterTextSplitter(
    #    chunk_size=CHUNK_SIZE,
    #    chunk_overlap=OVERLAP
    #)

    #text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    #    chunk_size=CHUNK_SIZE, chunk_overlap=OVERLAP
    #)

    text_splitter = TokenTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=OVERLAP
    )

    docs = text_splitter.create_documents([text for url, texts in removed_duplicates_text.items() for text in texts], [{'source':url} for url, texts in removed_duplicates_text.items() for text in texts])

    print("Number of documents: ", len(docs))
    print("Total words after split: ", sum([len(doc.page_content.split()) for doc in docs]))
    print("Average doc words: ", mean([len(doc.page_content.split()) for doc in docs]))

    script_name = os.path.splitext(os.path.basename(__file__))[0]

    with open(script_name+"_texts.txt", "w") as f:
        for doc in docs:
            f.write(doc.page_content.replace("\n", " - "))
            f.write("\n")

    with open(script_name+"_texts_url.txt", "w") as f:
        for doc in docs:
            f.write(doc.metadata['source']+" - "+doc.page_content.replace("\n", " - "))
            f.write("\n")


if __name__ == '__main__':
    main()
