# #
# MIT License
#
# Copyright (c) 2023 Hüseyin ABANOZ
# huseyinabanox@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#

from urllib.parse import urlsplit
import time
import requests
from lxml import etree
from lxml.etree import HTMLParser
from requests.exceptions import SSLError


def dfs_crawl(url_to_read, urls_read_set, url_text_map, path_exclusion_filters=None, depth=0, max_depth=50,
              max_urls=1000, sleep_time=0.3):
    if depth > max_depth:
        return

    cnt = len(urls_read_set)
    if cnt > max_urls:
        return

    if path_exclusion_filters is None:
        path_exclusion_filters = []

    print(f"C{cnt} L{depth} {url_to_read}")
    time.sleep(sleep_time)

    split_url = urlsplit(url_to_read)
    base_url = split_url[0] + "://" + split_url[1]

    urls_read_set.add(url_to_read)

    try:
        html_doc = requests.get(url_to_read)
    except SSLError:
        html_doc = requests.get(url_to_read, verify=False)

    # soup = BeautifulSoup(html_doc.text, 'html.parser')

    try:
        dom = etree.HTML(html_doc.text, parser=HTMLParser(remove_comments=True))
    except ValueError as e:
        print("Value error during dom parsing", e)
        return

    # url_text_map[url_to_read] = html_to_text_list(html_doc.text)
    url_text_map[url_to_read] = dom_to_text_list(dom)

    # for anchor in soup.find_all('a', href=True):
    for href in dom.xpath('//a/@href'):
        # href = anchor['href']
        if href is None or href == '' or href == '/' or href[0] == '#' or '.' in href[-5:] or href.startswith(
                'javascript:') or href.startswith('tel:'):
            continue  # avoid self, files and js code.

        if href.startswith('http') and not href.startswith(base_url):
            continue  # avoid visiting external pages

        url_found = (href if href.startswith('http') else base_url + ('' if href.startswith('/') else '/') + href)

        if url_found in urls_read_set:
            continue  # avoid re-visiting

        url_path = url_found[len(base_url) + 1:]

        for f in path_exclusion_filters:
            if f(url_path):
                break  # avoid if one of the exclude filters trigger
        else:
            dfs_crawl(url_found, urls_read_set, url_text_map, path_exclusion_filters=path_exclusion_filters,
                      depth=depth + 1, max_depth=max_depth, max_urls=max_urls, sleep_time=sleep_time)


def dom_to_text_list(dom):
    atexts = ['']
    tree_to_text_list(dom.xpath('body')[0], atexts, 0)

    # refine text can be called here to reduce memory usage
    # refine_text_list(text_list, max_length)

    return atexts

def tree_to_text_list(root, texts, idx):
    """
    Traverse all children elements.
    Put text to current index of texts list.
    If a div is found, put text to next index in the texts list.

    e.g.

    <div><This is a paragraph> Hello <This is another paragraph></div>
    <div><span>This is a span block</span></div>

    turns into

    ['This is a paragraph Hello This is another paragraph','This is a span block']


    <div><This is a paragraph> <div>Hello <This is another paragraph></div> </div>
    <div><span>This is a span block</span></div>

    turns into

    ['This is a paragraph','Hello This is another paragraph','This is a span block']

    """
    for el in root.iterchildren():

        if el.tag in ['style', 'script', 'link', 'meta']:
            continue  # ignore non text elements

        elif el.tag == 'div':  # a div block contain a separate text tree
            if el.text: texts.append(el.text)
            else: texts.append('')

            # increase index so that new text added to a new place in the list
            next_idx = len(texts) - 1
            tree_to_text_list(el, texts, next_idx)

            if el.tail: texts[idx] = texts[idx] + el.tail

            # remove empty texts
            texts[next_idx] = texts[next_idx].strip()
            if not texts[next_idx]:
                texts.pop(next_idx)

        else:  # non div block text is added to text found in the current div block
            # prepend text
            if el.text: texts[idx] = texts[idx] + el.text

            # find text to add iteratively
            tree_to_text_list(el, texts, idx)  #

            # append text
            if el.tail: texts[idx] = texts[idx] + el.tail

            h_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
            stops = ['.', ':', '?', ';', '!']

            # if headers does not end with a stop then append a semicolon
            if texts[idx].strip() and el.tag in h_tags and texts[idx].strip()[-1] not in stops:
                texts[idx] = texts[idx].strip() + ': '
