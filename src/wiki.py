"""
This code parses random wikipedia article.
1. Counts how many times each word appears in the article.
2. In text finds links to other wikipedia articles and does (1.) with each.
"""
import re
from hash_map import HashMap
from urllib.request import urlopen
from bs4 import BeautifulSoup


def count_words(html_txt: str, hash_map: HashMap) -> HashMap:
    """
    Counts words in wikipedia article.
    Hashmap is used to count words. Key is a word and value is number of the word in article
    :param html_txt: html text of wiki article
    :param hash_map: hash map to write results
    :return: hashmap with (key, value) -> (word, word quantity)
    """
    soup = BeautifulSoup(html_txt, 'html.parser')
    main_txt = soup.find(id="mw-content-text").div
    splitters = (r'\s', r'\.', r'\!', r'\?', r',', r';',
                 r'править \| править код',
                 r'\[', r'\]', r'\(', r'\)', r'\n', r'\\', r'\|')
    splitters = r'|'.join(splitters)
    words = re.split(splitters, main_txt.get_text())  # \s|\[|\]|,|;|\.|\(|\)|\n|\\|
    for word in words:
        if word != '' and word.isalpha():  # to count number also, isalpha should be changed to isalnum
            lower_word = word.lower()
            hash_map[lower_word] = hash_map.get(lower_word, 0) + 1
    return hash_map


def get_urls(html_txt: str, max_urls=-1) -> set:
    """
    In given wikipedia article finds links to other wikipedia articles
    :param html_txt: html text of wiki article
    :param max_urls: amount of urls required (default '-1' means 'all')
    :return: set of urls
    """
    url_list = set()
    urls = 0
    soup = BeautifulSoup(html_txt, 'html.parser')
    main_txt = soup.find(id="mw-content-text").div
    for link in main_txt.find_all('a'):
        article_link = link.get('href')
        if article_link is not None and url_is_valid(article_link):
            if WIKI_DOMAIN + article_link not in url_list:  # adds only unique urls
                urls += 1
            url_list.add(WIKI_DOMAIN + article_link)
            if urls >= max_urls >= 0:
                return url_list
    return url_list


def get_html(url: str) -> str:
    """
    Gets html code of website
    :param url: link
    :return: decoded html
    """
    response = urlopen(url)
    if url[-6:len(url)] == 'Random':
        print(response.geturl())
    response_bytes = response.read()
    return response_bytes.decode("utf8")


def counted_words_sum(words: [list, HashMap]) -> int:
    """
    Calculates how many words were counted
    :param words: iterables that yield LinkedElems which data consists of [word, quantity]
    :return: total number of words in article (with repeats)
    """
    total = 0
    for word in words:
        total += word.data[1]
    return total


def url_is_valid(url: str) -> bool:
    """
    Checks if URL leads to other wikipedia article
    :param url: url
    :return: true if url is valid / false if not
    """
    if not url.startswith('/wiki/'):
        return False
    black_list = ['gif', 'jpg', 'svg']
    if url[-3:len(url)] in black_list:
        return False
    if 'Edit' in url:
        return False
    return True


if __name__ == "__main__":

    WIKI_RANDOM = "https://ru.wikipedia.org/wiki/Special:Random"
    WIKI_DOMAIN = "https://ru.wikipedia.org"
    NEXT_URLS_NUM = 10

    txt = get_html(WIKI_RANDOM)
    main_words = HashMap()  # hashmap for words in main article

    count_words(txt, main_words)
    main_words = main_words.sort(reverse=True)
    print(main_words)
    print(counted_words_sum(main_words))
    print('----------------------------')

    secondary_words = []  # list of hashmaps for secondary articles
    for new_hashmap_num in range(NEXT_URLS_NUM):
        secondary_words.append(HashMap())

    file = 'C:\\Users\\minga\\Desktop\\test.txt'
    url_num = 0
    for url in get_urls(txt, NEXT_URLS_NUM):
        print(url)
        count_words(get_html(url), secondary_words[url_num])
        secondary_words[url_num].write_in_file(file)
        # print(secondary_words[url_num].sort(reverse=True))  # sorted list of words
        print(counted_words_sum(secondary_words[url_num]))
        url_num += 1
        print('----------------------------')
