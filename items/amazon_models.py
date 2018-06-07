import time
import requests
from bs4 import BeautifulSoup
from .algorithms import *
from .user_agent import user_agent_list
import random
from .proxy_scraper import get_proxies
from itertools import cycle
from django.core.mail import send_mail
# Create Amazon item model

proxies = get_proxies()
proxy_pool = cycle(proxies)






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

        item_list = []
        start_time = time.time()




        for page in range(1, 3):

            #Set header
            user_agent = random.choice(user_agent_list)
            print(user_agent)
            headers = {
                'User-Agent': user_agent,
            }
            #Set proxy
            proxy  = next(proxy_pool)
            print(proxy)

            #Set url
            pre_url = 'https://www.amazon.com/s?url=search-alias%3Daps'
            keyword_url = '&field-keywords=%s' % q_word
            url = pre_url + keyword_url + '&page={0}'.format(page)

            try:
                r = requests.get(url,
                                 headers=headers,
                                 proxies={"http":proxy,"https":proxy},
                                 timeout=5)


                print('getting to items')
                # sleep(5)while True:
                print(r.status_code)


                if int(r.status_code) == 200:
                    print("looks great")

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
                        pass

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




    # Back Search
    def get_square_items(self,q_word=None):

        print("sqaure items ")
        item_list = []

        start_time = time.time()


        for page in range(1, 3):

            # set header
            user_agent = random.choice(user_agent_list)
            print(user_agent)
            headers = {
                'user-agent': user_agent
            }

            #Set proxy
            proxy = next(proxy_pool)
            print(proxy)

            #Set Url
            pre_url = 'https://www.amazon.com/s?url=search-alias%3Daps'
            keyword_url = '&field-keywords=%s' % q_word
            url = pre_url + keyword_url + '&page={0}'.format(page)

            try:
                r = requests.get(url,
                                 headers=headers,
                                 proxies={"http":proxy, "https":proxy},
                                 timeout=5)

                print("Status_code: " + str(r.status_code))

                if int(r.status_code) == 200:
                    print("looks great")

                    soup = BeautifulSoup(r.content, "html.parser")

                    ul = soup.find('div', {'id': "resultsCol"})

                    all_li = ul.find_all('li', class_='s-result-item')
                    title = ''
                    link  = ""
                    image = ""
                    for li in all_li:
                        # Get Title and Link
                        all_tags = li.find_all('a', class_='a-link-normal')
                        all_imgs = li.find_all('img', class_='s-access-image cfMarker')
                        all_prices = li.find_all('span', class_='sx-price-whole')

                        try:
                            for price in all_prices:
                                price = int(price.text)

                            for img in all_imgs:
                                if 'src' in img.attrs:
                                    image = img['src']
                            for a in all_tags:
                                if 'title' in a.attrs and 'href' in a.attrs:
                                    title = a['title']
                                    link = a['href'] + "&tag=best10stoream-20"



                            rating_count = int(li.find('a', class_='a-size-small a-link-normal a-text-normal').text)
                            rating = float(li.find('span', class_='a-icon-alt').text.split(" ")[0])
                            # print(rating)
                            if not link.startswith("https://"):
                                link = 'https://www.amazon.com' + link
                            new_item = Item()
                            new_item.title = title
                            new_item.link  = link
                            new_item.image = image
                            new_item.price = price
                            new_item.rating = rating
                            new_item.rating_count = rating_count
                            new_item.hotscore = int(calculate_customer_satisfaction_score(rating, rating_count))

                            item_list.append(new_item)


                        except:
                            pass
                else:
                    send_mail(
                        'Parsing failed',
                        'Here is the status code:' + r.status_code,
                        'cj160901@gmail.com',
                        ['cj160901@gmail.com'],
                    )
                    print("Backup-Parsing failed")
            except:
                pass

            # sort item list by rating_count
            rating_count_sort = sorted(item_list, key=lambda x: x.rating_count, reverse=True)

            # sort top 10 rating_count_sort by rating
            rating_sort = sorted(rating_count_sort[:10], key=lambda x: x.rating, reverse=True)


            return  rating_sort
