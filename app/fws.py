
"""
    A Python program that crawls a website and recursively checks links to map all internal and external links
"""

from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from urllib.parse import urlparse
from collections import deque
import re
import sys
import os
import subprocess
import argparse

def crawler(domain, mute):
    filename =urlparse(domain).netloc
    if 'www' in filename:
        filename=filename.replace('www.','')
    ofile='data'+filename+'.txt'
    print('starting  ',domain)
    try:
        # a queue of urls to be crawled
        new_urls = deque([domain])
        print(new_urls)
        # a set of urls that we have already crawled
        processed_urls = set()
        # a set of domains inside the target website
        local_urls = set()
        local_urls_html=set()
        # a set of domains outside the target website
        foreign_urls = set()
        # a set of broken urls
        broken_urls = set()

        # process urls one by one until we exhaust the queue
        while len(new_urls):

            # move next url from the queue to the set of processed urls
            url = new_urls.popleft()
            processed_urls.add(url)
            # get url's content
            print("detected url  %s" % url)
            # try:
            #     response = requests.head(url)
            # except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
            #     # add broken urls to it's own set, then continue
            #     broken_urls.add(url)
            #     continue


            try:
                response = requests.get(url)
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
                # add broken urls to it's own set, then continue
                broken_urls.add(url)
                continue
            if 'content-type' in response.headers:
                content_type = response.headers['content-type']
                if not 'text/html' in content_type:
                    continue   
                if '4' in str(response.status_code):
                    broken_urls.add(url)
                    print('url is broken',url)

                    continue                    
            # extract base url to resolve relative links
            parts = urlsplit(url)
            base = "{0.netloc}".format(parts)
            strip_base = base.replace("www.", "")
            base_url = "{0.scheme}://{0.netloc}".format(parts)
            path = url[:url.rfind('/')+1] if '/' in parts.path else url

            # create a beutiful soup for the html document
            text = BeautifulSoup(response.text, "html.parser")
            # print('raw html',text)
            hrefs = {i.get("href") for i in text.find_all(
                href=True)}
            srcs = {i.get("src") for i in text.find_all(
                src=True)}
            print('count href link',len(hrefs))
            print('count srcs link',len(srcs))

            # Loop over the URLs in the current page
            for anchor in hrefs | srcs:
            # for link in text.find_all('a'):
                # extract link url from the anchor
                # anchor = link.attrs["href"] if "href" in link.attrs else ''
                # print('---',anchor)
                if any(anchor.startswith(i) for i in ["mailto:", "data:image","tel:", "javascript:", "#content-middle", "about:blank", "skype:"]):
                    continue
                if any(anchor.endswith(i) for i in [".js", ".css",".png", ".webp", ".jpg", ".jpeg", ".txt",".json",".svg"]):
                    continue                
                if anchor == "#" or "linkedin" in anchor or "\\" in anchor:
                    continue
                if anchor.startswith('//'):
                    local_link = anchor
                    local_urls.add(local_link)                
                elif anchor.startswith('/'):
                    local_link = base_url + anchor
                    local_urls.add(local_link)
                elif strip_base in anchor:
                    local_urls.add(anchor)
                elif not anchor.startswith('http'):
                    local_link = path + anchor
                    local_urls.add(local_link)
                else:
                    if not filename in anchor:

                        foreign_urls.add(anchor)




            for i in local_urls:
                if not i in new_urls and not i in processed_urls:
                    if filename in i:

                        new_urls.append(i)

            # print('=======\n',local_urls)
        print("post Processing",len(local_urls))
        local_urls=list(set(local_urls))
        print("post Processing",len(local_urls))

        for idx,url in enumerate(local_urls):
            print(idx,'url',url)
            if url.startswith('//'):
                pass
            else:
                try:
                    response = requests.head(url)

                    if 'content-type' in response.headers:
                        content_type = response.headers['content-type']
                        if not 'text/html' in content_type:
                            continue          
                        if '4' in str(response.status_code):
                            broken_urls.add(url)
                            continue   
                        else:
                            if filename in url:
                                local_urls_html.add(url)  
                            
                except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
                    # add broken urls to it's own set, then continue
                    broken_urls.add(url)
                    continue

        # if mute is False:
        #     if ofile is not None:
        #         report_file(ofile, processed_urls, local_urls, foreign_urls, broken_urls)
        #     else:
        #         report(processed_urls, local_urls, foreign_urls, broken_urls)
        # else:
        #     if ofile is not None:
        #         mute_report_file(ofile, local_urls)
        #     else:
        #         mute_report(local_urls)
    
        return local_urls_html

    except KeyboardInterrupt:
        local_urls_html=[]
        return local_urls_html

def limit_crawler(domain, ofile, limit, mute):
    try:
        # a queue of urls to be crawled
        new_urls = deque([domain])
        # a set of urls that we have already crawled
        processed_urls = set()
        # a set of domains inside the target website
        limit_urls = set()
        # a set of domains outside the target website
        limit_urls = set()
        # a set of broken urls
        broken_urls = set()

        # process urls one by one until we exhaust the queue
        while len(new_urls):

            # move next url from the queue to the set of processed urls
            url = new_urls.popleft()
            processed_urls.add(url)
            # get url's content
            print("Processing %s" % url)
            try:
                response = requests.get(url)
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
                # add broken urls to it's own set, then continue
                broken_urls.add(url)
                continue

            # extract base url to resolve relative links
            parts = urlsplit(url)
            base = "{0.netloc}".format(parts)
            strip_base = base.replace("www.", "")
            base_url = "{0.scheme}://{0.netloc}".format(parts)
            path = url[:url.rfind('/')+1] if '/' in parts.path else url

            # create a beutiful soup for the html document
            soup = BeautifulSoup(response.text, "lxml")

            for link in soup.find_all('a'):
                # extract link url from the anchor
                anchor = link.attrs["href"] if "href" in link.attrs else ''
                print(anchor)

                if limit in anchor:
                    limit_urls.add(anchor)
                else:
                    pass

            for i in limit_urls:
                if not i in new_urls and not i in processed_urls:
                    new_urls.append(i)

        print()
        if mute is False:
            if ofile is not None:
                return limit_report_file(limit, ofile, processed_urls, limit_urls, broken_urls)
            else:
                return limit_report(limit, processed_urls, limit_urls, broken_urls)
        else:
            if ofile is not None:
                return limit_mute_report_file(limit, ofile, limit_urls)
            else:
                return limit_mute_report(limit, limit_urls)

    except KeyboardInterrupt:
        sys.exit()


def limit_report_file(limit, ofile, processed_urls, limit_urls, broken_urls):
    with open(ofile, 'w') as f:
        print(
            "--------------------------------------------------------------------", file=f)
        print("All found URLs:", file=f)
        for i in processed_urls:
            print(i, file=f)
        print(
            "--------------------------------------------------------------------", file=f)
        print("All " + limit + "URLs:", file=f)
        for j in limit_urls:
            print(j, file=f)
        print(
            "--------------------------------------------------------------------", file=f)
        print("All broken URL's:", file=f)
        for z in broken_urls:
            print(z, file=f)


def limit_report(limit, processed_urls, limit_urls, broken_urls):
    print("--------------------------------------------------------------------")
    print("All found URLs:")
    for i in processed_urls:
        print(i)
    print("--------------------------------------------------------------------")
    print("All " + limit + " URLs:")
    for j in limit_urls:
        print(j)
    print("--------------------------------------------------------------------")
    print("All broken URL's:")
    for z in broken_urls:
        print(z)


def limit_mute_report_file(limit, ofile, limit_urls):
    with open(ofile, 'w') as f:
        print(
            "--------------------------------------------------------------------", file=f)
        print("All " + limit + " URLs:", file=f)
        for j in limit_urls:
            print(j, file=f)


def limit_mute_report(limit, limit_urls):
    print("--------------------------------------------------------------------")
    print("All " + limit + "URLs:")
    for i in limit_urls:
        print(i)

def report_file(ofile, processed_urls, local_urls, foreign_urls, broken_urls):
    with open(ofile, 'w') as f:
        print(
            "--------------------------------------------------------------------", file=f)
        print("All found URLs:", file=f)
        for i in processed_urls:
            print(i, file=f)
        print(
            "--------------------------------------------------------------------", file=f)
        print("All local URLs:", file=f)
        for j in local_urls:
            print(j, file=f)
        print(
            "--------------------------------------------------------------------", file=f)
        print("All foreign URLs:", file=f)
        for x in foreign_urls:
            print(x, file=f)
        print("--------------------------------------------------------------------", file=f)
        print("All broken URL's:", file=f)
        for z in broken_urls:
            print(z, file=f)


def report(processed_urls, local_urls, foreign_urls, broken_urls):
    print("--------------------------------------------------------------------")
    print("All found URLs:")
    for i in processed_urls:
        print(i)
    print("--------------------------------------------------------------------")
    print("All local URLs:")
    for j in local_urls:
        print(j)
    print("--------------------------------------------------------------------")
    print("All foreign URLs:")
    for x in foreign_urls:
        print(x)
    print("--------------------------------------------------------------------")
    print("All broken URL's:")
    for z in broken_urls:
        print(z)


def mute_report_file(ofile, local_urls):
    with open(ofile, 'w') as f:
        print(
            "--------------------------------------------------------------------", file=f)
        print("All local URLs:", file=f)
        for j in local_urls:
            print(j, file=f)


def mute_report(local_urls):
    print("--------------------------------------------------------------------")
    print("All local URLs:")
    for i in local_urls:
        print(i)

domain_pattern = re.compile(
    r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
    r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
    r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
    r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
)


def isvaliddomain(value, raise_errors=True):
    """
    Return whether or not given value is a valid domain.
    If the value is valid domain name this function returns ``True``, otherwise
    :class:`~validators.ValidationFailure` or False if raise_errors muted.
    Examples::
        >>> domain('example.com')
        True
        >>> domain('example.com/')
        ValidationFailure(func=domain, ...)
    Supports IDN domains as well::
        >>> domain('xn----gtbspbbmkef.xn--p1ai')
        True
    :param value: domain string to validate
    :param raise_errors: raise errors or return False
    """
    print(domain_pattern.match(value))
    if domain_pattern.match(value) is None:
        # if raise_errors:
        #     # raise ValidationFailure("{} is not valid domain".format(value))

        # else:
        #     return False
        return False
    return True