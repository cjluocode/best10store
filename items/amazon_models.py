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


        for page in range(1,2):#change to 1 page due to timeout issue
            print("looping " + str(page) + " page now")

            #Set header
            user_agent = random.choice(user_agent_list)
            headers = {
                'User-Agent': user_agent,
            }

            #Set url
            pre_url = 'https://www.amazon.com/s?url=search-alias%3Daps'
            keyword_url = '&field-keywords=%s' % q_word
            url = pre_url + keyword_url + '&page={0}'.format(page)


            proxy_host = "proxy.crawlera.com"
            proxy_port = "8010"
            proxy_auth = "5b115385a7f3490bbbb35fa44d8b9bf9:"
            proxies = {"https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
                       "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}


            try:
                print("requesting getting url")
                r = requests.get(url,
                                 headers=headers,
                                 proxies=proxies,
                                 verify=False,
                                 timeout=29
                                 )


                print("status_code: " + str(r.status_code))

                if int(r.status_code) == 200:
                    try:
                        parser = html.fromstring(r.content)
                        all_item_container = parser.xpath(XPATH_ITEM_CONTAINER)

                        for item in all_item_container:

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

            except:
                pass

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
