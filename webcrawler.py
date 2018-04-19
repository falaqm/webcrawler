import time
import urllib

import requests
from bs4 import BeautifulSoup as BS

start_url = "https://en.wikipedia.org/wiki/Special:Random"
target_url = "https://en.wikipedia.org/wiki/Philosophy"

def find_first_link(url):
# get the HTML from "url", use the requests library
# feed the HTML into Beautiful Soup
# find the first link in the article
# return the first link as a string, or return None if there is no link
response=requests.get(url)
html=response.text
soup=BS(html,'html.parser')


# This div contains the article's body
# (June 2017 Note: Body nested in two div tags)
content_div=soup.find(id="mw-content-text").find(class_="mw-parser-output")

# stores the first link found in the article, if the article contains no
# links this value will remain None
article_link = None
# Find all the direct children of content_div that are paragraphs

for element in content_div.find_all('p',recursive=False):
    # Find the first anchor tag that's a direct child of a paragraph.
    # It's important to only look at direct children, because other types
    # of link, e.g. footnotes and pronunciation, could come before the
    # first link to an article. Those other link types aren't direct
    # children though, they're in divs of various classes.
    if element.find('a',recursive=False):
        article_link=element.find('a',recursive=False).get('href')
        break
if not article_link:
    return

first_link=urllib.parse.urljoin('https://en.wikipedia.org/',article_link)
return first_link


def continue_crawl(search_history,target_url,max_steps=25):
search_set=set(search_history)
if target_url == search_history[-1]:
    print('found it')
    return False
elif len(search_history)>max_steps:
    print('too long,ABORT!!!')
    return False
elif search_history[-1]== search_history[:-1]:
    print('duplicates found')
    return False
else:
    print('continue')
    return True



article_chain=[start_url]

while continue_crawl(article_chain,target_url):
print(article_chain[-1])
# download html of last article in article_chain
# find the first link in that html
first_link=find_first_link(article_chain[-1])
# add the first link to article_chain
article_chain.append(first_link)
# delay for about two seconds
time.sleep(1)
