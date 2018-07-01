import requests
from lxml import html


proxies = {'http': 'http://best10store:$Best10store$@us-wa.proxymesh.com:31280',
           'https': 'http://best10store:$Best10store$@us-wa.proxymesh.com:31280'}


class Review(object):

    def __init__(self):

        self.content = ""

    def parse_reviews(self, link):
        review_list = []

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

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


