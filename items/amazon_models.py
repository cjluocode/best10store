import time
import requests
from .user_agent import user_agent_list
import random
from lxml import html
import toolz
from .helper_function import *
from .threads_helper import MultiThreadsClass


# Create Amazon item model

class Item(object):
    def __init__(self):
        self._MultiThreadsClass = MultiThreadsClass()
        self.title = ''
        self.link  = ""
        self.rating = 5.0
        self.rating_count = 10
        self.hotscore = 90
        self.image    = ""
        self.price    = 1
        self.item_list = []

    def loop_amazon_pages_and_scrape_results(self, data):
        url = data.get("page_url")
        q_word = data.get("q_word")

        # avoid search without param and just 2 letters
        if q_word is None:
            return
        if len(q_word) == 2:
            return

        print("looping " + str(url) + " page now")
        try:
            # Get the response
            response = self.load_page(url=url, is_proxy=True)

            if int(response.status_code) == 200:
                try:
                    parser = html.fromstring(response.content)
                    all_item_container = parser.xpath(XPATH_ITEM_CONTAINER)

                    for item in all_item_container:

                        # Get item's title,link,image_url,rating_count,rating
                        item_title = parse_title(item)

                        item_link = parse_link(item)

                        item_image_url = parse_image(item)
                        item_rating_counts = parse_rating_count(item)
                        item_rating = parse_rating(item)


                        # Create new item then append to item_list
                        new_item = Item()
                        new_item.title = item_title
                        new_item.link = item_link
                        new_item.image = item_image_url

                        if item_rating_counts:
                            new_item.rating_count = item_rating_counts
                        if item_rating:
                            new_item.rating = item_rating
                            new_item.hotscore = get_hotscore(item_rating)

                        # no need save items without title
                        if item_title is not None:
                            self.item_list.append(new_item)

                except Exception as e:
                    print(e)

        except Exception as e:
            print(e)


    def get_items(self,q_word=None):
        #set start time
        start_time = time.time()

        self.item_list = []
        pages = []
        for page in range(1, 4):
            page_url = set_url(q_word, page)
            obj = {
                "page_url": page_url,
                "q_word":q_word
            }
            pages.append(obj)

        #self.loop_amazon_pages_and_scrape_results(pages[3])
        self._MultiThreadsClass.run_multi(self.loop_amazon_pages_and_scrape_results, pages, len(pages))
        sorted_item_list = self.sort_item_list(self.item_list)

        print("--- %s seconds ---" % (time.time() - start_time))
        print("---- TOTAL RECORDS: {}".format(len((self.item_list))))
        return sorted_item_list




    def sort_item_list(self, item_list):

        # Remove duplicated item
        unique_item_list = toolz.unique(item_list, key=lambda x: x.title)

        # Sort item by rating_count
        rating_count_sort = sorted(unique_item_list, key=lambda x: x.rating_count, reverse=True)

        # Sort top 10 rating_count by rating
        rating_sort = sorted(rating_count_sort[:10], key=lambda x: x.rating, reverse=True)

        return rating_sort

        # TODO: load page into bs4


    def load_page(self, url, is_proxy=False, max_try_num=20):
        # Set header
        headers = {
            'User-Agent': random.choice(user_agent_list),
        }
        print("[+++][PROXY] Now url is : {}".format(url))
        soup = ""
        try_num = 1
        while try_num <= max_try_num:
            print("[?] Proxy try {}".format(try_num))
            try:
                if is_proxy:
                    proxies = {
                        'https': self.getProxy(),
                        'http': self.getProxy(),
                    }
                    response = requests.get(url=url, headers=headers, proxies=proxies, timeout=5)
                else:
                    response = requests.get(url=url, headers=headers, timeout=5)
                try:
                    if response.status_code == 200:
                        print("[+++] Proxy success")
                        soup = response
                        break
                    elif response.status_code == 404:
                        soup = response
                        try_num += 1
                        continue
                    elif response.status_code == 400:
                        print("[-] Response code is {}".format(response.status_code))
                        soup = response
                        break
                    else:
                        print("[-] Response code is {}".format(response.status_code))
                except Exception as E:
                    try_num += 1
                    soup = response
                    continue

            except Exception as E:
                try_num += 1

        return soup

        # TODO: get proxy from list

    def getProxy(self):
        # Put here your proxies like <ip:port>
        proxies = [
            'http://best10store:$Best10store$@us-wa.proxymesh.com:31280',
        ]

        if len(proxies) == 1:
            number = 0
        else:
            number = random.randrange(0, len(proxies) - 1, 1)
        proxy = proxies[number]

        print("::Now proxy is : {}".format(proxy))
        return proxy