from .xpath import *

def parse_title(item):

    raw_title = item.xpath(XPATH_TITLE_1)
    if not raw_title:
        raw_title = item.xpath(XPATH_TITLE_2)


    if len(raw_title) > 0 :
        title = raw_title[0]
        return title
    else:
        return None


def parse_link(item):

    raw_link = item.xpath(XPATH_LINK)

    if len(raw_link) > 0:
        link = raw_link[0]
        if not link.startswith('http'):
            link = 'https://www.amazon.com' + link

        return link
    else:
        return None

def parse_image(item):

    raw_image = item.xpath(XPATH_IMAGE)
    if len(raw_image) >= 1:
        image = raw_image[-1]
        return image

    else:
        return None

def parse_rating_count(item):

    raw_rating_counts = item.xpath(XPATH_RATING_COUNT_1)

    if not raw_rating_counts:
        raw_rating_counts = item.xpath(XPATH_RATING_COUNT_2)
        if not raw_rating_counts:
            raw_rating_counts = item.xpath(XPATH_RATING_COUNT_3)

    if len(raw_rating_counts) >= 1:
        raw_rating_counts = raw_rating_counts[-1].text
        try:
            rating_counts = int(raw_rating_counts.replace(',', ''))
        except:
            rating_counts = 1


        return rating_counts

def parse_rating(item):

    raw_rating = item.xpath(XPATH_RATING)


    try:

        if "Prime" in raw_rating and len(raw_rating) >1:

            removed_prime_rating = [x for x in raw_rating if x != 'Prime']

            rating = float(removed_prime_rating[0].split("out")[0])

            return rating

        elif len(raw_rating) == 1:

            rating = float(raw_rating[0].split("out")[0])

            return rating

    except Exception as e:
        print(e)
        return 0




def set_url(q_word, page):
    # url=search-alias%3Dstripbooks&field-keywords=startup&rh=n%3A283155%2Ck%3Astartup
    pre_url = 'https://www.amazon.com/s?url=search-alias%3Daps'
    keyword_url = '&field-keywords=%s' % q_word
    amazon_url = pre_url + keyword_url + '&page={0}'.format(page)
    return amazon_url


def get_hotscore(rating):

    hotscore = rating * 20

    return int(hotscore)