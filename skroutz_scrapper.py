import logging

import regex as re
import requests
from bs4 import BeautifulSoup

price_rgx = re.compile(r"((\d{1,3})\.)?(\d{0,3}),(\d{2}) €")
valid_cat = {'46', '55', '49', '56', '28', '32', '31', '30', }
search_url = "https://www.skroutz.gr/search?keyphrase="


class Product:
    """"""

    def __init__(self, name: str, price: float, url: str):
        self.name = name
        self.price = price
        self.url = url


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


def get_product_page(url: str, max_num_of_res: int = 5) -> (list, str):
    """
    Finds product prices from  product url, search query, or search result
    :param url: the actual url (product, search, or search result)
    :param max_num_of_res: =5max number of results (when available)
    :return: list of lists with price and link, error message
    """
    try:
        page = requests.get(url)
    except:
        return [], "Error on getting URL"

    # rel="canonical"
    try:
        actualURL = BeautifulSoup(page.text, 'html.parser').find(
            attrs={"rel": "canonical"}, href=True)['href']
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

    # Create a BeautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')
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
                Product(
                    title if max_num_of_res == 1 else o['title'],
                    price_to_float(o.getText()),
                    "https://www.skroutz.gr" + o['href'] if max_num_of_res > 1 else actualURL
                )
            )
        return ret_val, title
    except:
        return [], "Unkown error"


if __name__ == "__main__":
    tests = [
        'https://www.skroutz.gr/s/11912425/Corsair-Dominator-Platinum-16GB-DDR4-4000MHz-CMD16GX4M2E4000C19.html',
        'https://www.skroutz.gr/s/15281915/Intel-Core-i9-7900X-Tray.html',
        '42.17',
        'https://www.skroutz.gr/s/3405130/Intel-Core-i7-4770-Box.html',
        'https://www.skroutz.gr/c/56/mnhmes-pc-ram/f/499830_583121/DDR4-16GB.html?o=ddr4',
        'https://www.skroutz.gr/search?keyphrase=2060',
        'https://www.skroutz.gr/search?keyphrase=τοστίερα',
    ]

    for t in tests:
        res, msg = get_product_page(t)
        if res:
            for r in res:
                print(r.price, msg)
        else:
            print(msg)

        print('\n')
