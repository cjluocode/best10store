import time
import requests
from bs4 import BeautifulSoup
from .algorithms import *
from .user_agent import user_agent_list
import random
from .proxy_scraper import get_proxies
from itertools import cycle
from django.core.mail import send_mail
from time import sleep
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


    # Primary Search
    def get_items(self,q_word=None):
        get_proxies()

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
                                 # timeout=29
                                 )


                print("got it url")
                print("status_code: " + str(r.status_code))
                if int(r.status_code) == 200:

                    soup = BeautifulSoup(r.content, "html.parser")
                    try:
                        ul = soup.find('div', {'id': "resultsCol"})
                        all_li = ul.find_all('li', class_='s-result-item')


                        for li in all_li:
                            all_a = li.find_all('a')
                            rating_div = li.find('div', class_='a-column a-span5 a-span-last')
                            if not rating_div:
                                rating_div = li.find('div', class_='a-row a-spacing-top-mini a-spacing-none')

                            try:
                                price = li.find_all('span', class_='sx-price-whole')[0].text
                                rating_count = int(rating_div.find_all('a')[1].text)
                                rating = float(rating_div.find('i').text.split(" ")[0])
                                title = all_a[1].text.strip()
                                link = all_a[1]['href'] + "&tag=best10stoream-20"
                                img = all_a[0].find('img')['src']

                                if title and 'https' in link and not "Learn more about Sponsored Products." in title and len(
                                        title) > 5:
                                    new_item = Item()
                                    new_item.title = title
                                    new_item.link = link
                                    new_item.rating = rating
                                    new_item.rating_count = rating_count
                                    new_item.hotscore = int(calculate_customer_satisfaction_score(rating,rating_count))
                                    new_item.image = img
                                    new_item.price = price
                                    item_list.append(new_item)

                            except:
                                pass
                    except:
                        print("Didn't get the page url")

                    print("parsing finished")
                    print("--- %s seconds ---" % (time.time() - start_time))
                else:
                    send_mail(
                        'Parsing failed',
                        'Here is the status code:' + r.status_code,
                        'cj160901@gmail.com',
                        ['cj160901@gmail.com'],
                    )
                    print("Primary Parsing filed")
            except:
                pass
        # sort item list by rating_count
        rating_count_sort = sorted(item_list, key=lambda x: x.rating_count, reverse=True)

        # sort top 10 rating_count_sort by rating
        rating_sort       = sorted(rating_count_sort[:10], key=lambda x: x.rating, reverse=True)

        return rating_sort
