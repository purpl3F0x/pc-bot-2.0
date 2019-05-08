import logging

import regex as re
import requests
from bs4 import BeautifulSoup

price_rgx = re.compile(r"((\d{1,3})\.)?(\d{0,3}),(\d{2}) €")
valid_cat = {'46', '55', '49', '56', '28', '32', '31', '30', }
search_url = "https://www.skroutz.gr/search?keyphrase="


def price_to_float(s: str) -> float:
    """
    Converts a string with format 'n.nnn,nn €' to float
    :param s: the price
    :return: return price in float
    """
    res = re.match(price_rgx, s)
    ret_val = (res.group(2)
               if res.group(2) else "") + res.group(3) + "." + res.group(4)
    return float(ret_val)


def deep_dive(url: str, args: dict = {}) -> str:
    """
    Returns actual url, of search - tries to navigate to tech. category if multiple results
    :param url:  url
    :param args: optional url parameters (must be formatted)
    :return: returns the actual url
    """
    if url.find('skroutz.gr/s/') != -1:  # Reduce numbers of requests
        return url

    url = BeautifulSoup(requests.get(url).text, 'html.parser').find(attrs={"rel": "canonical"}, href=True)['href']

    if url.find('skroutz.gr/c/') != -1:
        return url + ('?' if '?' not in url else '&') + (
            lambda x: '&'.join("%s=%s" % (str(k), str(v)) for (k, v) in x.items()))(args)
    elif url.find('skroutz.gr/s/') != -1:
        return url
    elif url.find('skroutz.gr/search?keyphrase') >= 0:
        cards = BeautifulSoup(requests.get(url).text, 'html.parser').find_all(attrs={'class': "card technology"})
        for c in cards:
            a = c.find('a', href=True)
            f = a['href'].find('/c/')
            if f >= 0 and a['href'][f + 3:f + 5] in valid_cat:
                return 'https://skroutz.gr' + a['href'] + ('?' if '?' not in url else '&') + (
                    lambda x: '&'.join("%s=%s" % (str(k), str(v)) for (k, v) in x.items()))(args)
        return ''
    else:
        return ''


def get_product_page(url: str, max_num_of_res: int = 5, args: dict = {}) -> (list, str):
    """
    Finds product prices from  product url, search query, or search result
    :param url: the actual url (product, search, or search result)
    :param max_num_of_res: =5max number of results (when available)
    :param args: optional url parameters
    :return: list of lists with price and link, error message
    """

    try:
        actualURL = deep_dive(url, args)
        print(actualURL)
        try:
            soup = BeautifulSoup(requests.get(actualURL).text, 'html.parser')
        except:
            return [], "error getting deep-dive "
    except TypeError:
        return [], "Couldn't extract actual URL"
    except:
        return [], "Unkown Error when getting URL"

    logging.info('Getting info about >\t', actualURL)

    a = actualURL.find('skroutz.gr/c/')
    if a >= 0:
        if actualURL[a + 13:a + 15] not in valid_cat:
            return 0, "Not valid results"
    else:
        max_num_of_res = 1

    reslts = soup.find(
        attrs={"id": lambda x: x == "prices" or x == "sku-list"})
    if not reslts:
        return [], "Not found prices div"

    offers = reslts.find_all(
        attrs={"class": ["product-link", "sku-link"]}, href=True)
    if not offers:
        return [], "Not found any listings"

    try:
        title = soup.title.string.replace(" - Skroutz.gr", "")
        ret_val = []
        for o in offers[:min(max_num_of_res, len(offers))]:
            ret_val.append(
                {
                    'name' : title if max_num_of_res == 1 else o['title'],
                    'price': price_to_float(o.getText()),
                    'url'  : "https://www.skroutz.gr" + o['href'] if max_num_of_res > 1 else actualURL,
                    '_'    : soup,
                }
            )
        return ret_val, title
    except:
        return [], "Unkown error"


if __name__ == "__main__":
    tests = [
        '2323'
        'https://www.skroutz.gr/s/11912425/Corsair-Dominator-Platinum-16GB-DDR4-4000MHz-CMD16GX4M2E4000C19.html',
        'https://www.skroutz.gr/s/15281915/Intel-Core-i9-7900X-Tray.html',
        '42.17',
        'https://www.skroutz.gr/s/3405130/Intel-Core-i7-4770-Box.html',
        'https://www.skroutz.gr/c/56/mnhmes-pc-ram/f/499830_583121/DDR4-16GB.html?o=ddr4',
        'https://www.skroutz.gr/search?keyphrase=2060',
        'https://www.skroutz.gr/search?keyphrase=τοστίερα',
        'https://www.skroutz.gr/search?keyphrase=7900X',
    ]

    for t in tests:
        res, msg = get_product_page(t)
        if res:
            for r in res:
                print(r['price'], msg)
                print(res)
        else:
            print(msg)
            exit()

        print('\n')
