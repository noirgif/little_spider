#!/data/data/com.termux/files/usr/bin/python 
# -*- coding: utf-8 -*-
'This is a toy web spider for web class'

import re
import os
import sys
import codecs
import requests
import bs4


__author__ = 'gloit'

pool = []

class url_site(object):
    def __init__(self, url):
        self.raw = url
        print(url)
        m = re.match('(http|https)://(.+)/?', self.raw)
        self.valid = m != None
        if self.valid is not False:
            self.name = m.groups()[1]
        else:
            self.name = None

class node(object):
    def __init__(self, url, depth = 0):
        self.url = url
        self.depth = depth
    def exec(self, max_depth= 2):
        if self.depth == max_depth:
            return
        print('crawling: %s', self.url.raw)
        r = requests.get(self.url.raw)
        if r.status_code != 200:
            raise Exception('Error occured when request for %s', self.url.raw)
        f = os.open(self.url.name.replace('/','\\'), os.O_CREAT | os.O_RDWR)
        os.write(f, r.content)
        os.close(f)
        urls = []
        site = bs4.BeautifulSoup(r.content.decode(), 'html5lib')
        for i in site.find_all('a'):
            urls.append(i.get('href'))
        

        for url in urls:
            if url == None:
                continue
            st = url_site(url)
            if st.valid == False:
                print('not valid: %s' % url)
                continue
            else:
                if url in pool:
                    print('duplicated: %s' % url)
                    continue
                else:
                    print('valid: %s' % url)
                    pool.append(url)
                    n = node(st, self.depth + 1)
                    n.exec(max_depth)

if __name__ == '__main__':
    if(len(sys.argv) == 1):
        print("usage: python spider.py [url]")
        sys.exit(0)
    else:
        try:
            assert(len(sys.argv) > 1)
        except AssertionError:
            print('Error: too many parameters. Specify one url at a time!')

    st = url_site(sys.argv[1])
    if st.valid == False:
        print('Error: please give a valid url!')
        print(st.raw)
        sys.exit(-1)

    n = node(st)
    pool.append(st.name)
    n.exec()



            
