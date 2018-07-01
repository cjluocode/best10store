import requests
from lxml import html
from .user_agent import user_agent_list
import random

proxies = {'http': 'http://best10store:$Best10store$@us.proxymesh.com:31280',
           'https': 'http://best10store:$Best10store$@us.proxymesh.com:31280'}

headers = {
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8',
    # 'accept-encoding': 'gzip, deflate, br',
    # 'accept-language': 'en-IN,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,hi;q=0.6',
    'User-Agent': random.choice(user_agent_list),
}




class Review(object):

    def __init__(self):

        self.content = ""

    def parse_reviews(self, link):
        review_list = []


        page = requests.get(link,
                            proxies=proxies,
                            headers=headers,
                            timeout=10)
        print(page.status_code)

        page_response = page.text
        parser = html.fromstring(page_response)

        XPATH_REVIEW_SECTION_1 = '//div[contains(@id,"reviews-summary")]'
        XPATH_REVIEW_SECTION_2 = '//div[@data-hook="review"]'

        reviews = parser.xpath(XPATH_REVIEW_SECTION_1)
        if not reviews:
            reviews = parser.xpath(XPATH_REVIEW_SECTION_2)

        for review in reviews:
            XPATH_REVIEW_TEXT_1 = './/div[@data-hook="review-collapsed"]//text()'

            raw_review_text1 = review.xpath(XPATH_REVIEW_TEXT_1)

            reviews = raw_review_text1[0]

            # print(reviews)

            new_review = Review()

            new_review.content = reviews

            review_list.append(new_review.content)

        return review_list


