"""
This code parses random wikipedia article
"""
import re
from hash_map import HashMap
from urllib.request import urlopen
from bs4 import BeautifulSoup


def count_words(html_txt: str, hash_map: HashMap):
    """
    Counts words in wikipedia article.
    Hash map is used to count words. Key is a word and value is number of the word in article
    :param html_txt: html text of wiki article
    :param hash_map: hash map to write results
    :return: None
    """
    soup = BeautifulSoup(html_txt, 'html.parser')
    main_txt = soup.find(id="mw-content-text").div
    splitters = (r'\s', r'\[', r'\]', r',', r';', r'\.', r'\(', r'\)', r'\n', r'\\', r' ')
    splitters = r'|'.join(splitters)
    for block in main_txt.find_all('p'):
        words = re.split(splitters, block.get_text())  # \s|\[|\]|,|;|\.|\(|\)|\n|\\|
        for word in words:
            if word != '':
                lower_word = word.lower()
                hash_map[lower_word] = hash_map.get(lower_word, 0) + 1
    for head in range(2, 5):
        for headlines in main_txt.find_all('h'+str(head)):
            words = re.split(splitters, headlines.get_text())
            for word in words:
                if word != '':
                    lower_word = word.lower()
                    hash_map[lower_word] = hash_map.get(lower_word, 0) + 1


if __name__ == "__main__":
    # WIKI_RANDOM = "https://ru.wikipedia.org/wiki/Special:Random"
    WIKI_RANDOM = "https://ru.wikipedia.org/wiki/%D0%9E%D0%B1%D0%B0%D0%BC%D0%B0,_%D0%91%D0%B0%D1%80%D0%B0%D0%BA"
    # Barack Obama article for test
    WIKI_DOMAIN = "https://ru.wikipedia.org"
    response = urlopen(WIKI_RANDOM)
    response_bytes = response.read()
    txt = response_bytes.decode("utf8")
    main_words = HashMap()
    count_words(txt, main_words)
    print(main_words.sort(reverse=True))
