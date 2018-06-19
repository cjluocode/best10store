import time
import requests
from bs4 import BeautifulSoup
from .algorithms import *
from .user_agent import user_agent_list
import random
from .proxy_scraper import get_proxies
from .xpath import *
from lxml import html
import toolz
# Create Amazon item model



class Item(object):
    def __init__(self):
        self.title = ''
        self.link  = ""
        self.rating = 5.0
        self.rating_count = 10
        self.hotscore = 90
        self.image    = ""
        self.price    = 1


    def get_items(self,q_word=None):

        item_list = []
        start_time = time.time()


        for page in range(1,3):#change to 1 page due to timeout issue
            print("looping " + str(page) + " page now")

            #Set header
            user_agent = random.choice(user_agent_list)
            headers = {
                'User-Agent': user_agent,
            }

            # Set url
            pre_url = 'https://www.amazon.com/s?url=search-alias%3Daps'
            keyword_url = '&field-keywords=%s' % q_word
            url = pre_url + keyword_url + '&page={0}'.format(page)

            r = self.load_page(url=url, headers = headers, is_proxy= True)


            print("requesting getting url")
            # print("status_code: " + str(r.status_code))

            if r:

                if int(r.status_code) == 200:
                    try:
                        parser = html.fromstring(r.content)
                        all_item_container = parser.xpath(XPATH_ITEM_CONTAINER)

                        for item in all_item_container:


                            # Get the title
                            raw_title = item.xpath(XPATH_TITLE)
                            if len(raw_title) > 0:
                                title = raw_title[0]


                            # Get the title
                            raw_title = item.xpath(XPATH_TITLE)
                            if len(raw_title) > 0:
                                title = raw_title[0]
                                print(title)


                            # Get the Link
                            raw_link = item.xpath(XPATH_LINK)
                            if len(raw_link) > 0:
                                link = raw_link[0]

                            # Get image
                            raw_image = item.xpath(XPATH_IMAGE)
                            if len(raw_image) >= 1:
                                image = raw_image[-1]

                            # Get rating counts
                            raw_rating_counts = item.xpath(XPATH_RATING_COUNT)
                            if len(raw_rating_counts) >= 1:
                                raw_rating_counts = raw_rating_counts[-1].text
                                rating_counts = int(raw_rating_counts.replace(',', ''))

                            # Get the ratings
                            raw_rating = item.xpath(XPATH_RATING)
                            if len(raw_rating) >= 1:
                                rating = float(raw_rating[-1].split("out")[0])

                            # Create new item then append to
                            new_item = Item()
                            new_item.title = title
                            new_item.link = link
                            new_item.image = image
                            new_item.rating_count = rating_counts
                            new_item.rating = rating

                            item_list.append(new_item)

                    except Exception as e:
                        print(e)

            print("--- %s seconds ---" % (time.time() - start_time))

        sorted_item_list = self.sort_item_list(item_list)

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

    def load_page(self, url, headers, is_proxy=False, max_try_num=20):
        print("[+++][PROXY] Now url is : {}".format(url))
        soup = ""
        try_num = 1
        while try_num <= max_try_num:
            print("[?] Proxy try {}".format(try_num))
            try:
                if is_proxy:
                    proxies = {
                        'https': self.getProxy(),
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
        # 108.59.14.208:13040
        proxies = [
            "108.59.14.208:13040",
            "108.59.14.203:13040"
        ]

        if len(proxies) == 1:
            number = 0
        else:
            number = random.randrange(0, len(proxies) - 1, 1)
        proxy = proxies[number]

        print("::Now proxy is : {}".format(proxy))
        return proxy