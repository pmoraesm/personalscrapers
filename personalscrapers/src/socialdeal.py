import re

import requests
from bs4 import BeautifulSoup
import pandas as pd


def _get_title(element):
    try:
        return element.find("div" , class_="title-container").select_one("h4").text
    except AttributeError:
        return "N/A"

def _get_company(element):
    try:
        return element.find("div", class_="company").select_one("span").text
    except AttributeError:
        return "N/A"

def _get_old_price(element):
    try:
        return (element.find("div", class_=lambda value: value and value.startswith("price-col"))
            .select_one("span[class^=old-price]").text)
    except AttributeError:
        return "N/A"

def _get_price(element):
    try:
        return (element.find("div", class_=lambda value: value and value.startswith("price-col"))
            .select_one("span[class=price]").text)
    except AttributeError:
        return "N/A"

def _get_sold(element):
    try:
        return (int(re.search(r'\d+', element.find("div", class_="sold-text text-color-stats")
            .text.replace('.','')).group()))
    except AttributeError:
        return 0

def _get_link(element):
    try:
        return f'<a href={element.find("a", class_="deal-card")["href"]}>link</a>'
    except TypeError :
        return "N/A"


def scrape_page(url: str) -> list:
    """
    Scrappe page
    """
    page = requests.get(url)
    results = BeautifulSoup(page.content, "html.parser").find(id="lastMinuteDeals")
    elements = results.find_all("div", class_=lambda value: value and value.startswith("mix"))
    return elements


def gen_df(elements: list, df: pd.DataFrame) -> pd.DataFrame():
    """
    Generate DataFrame with results
    """
    for element in elements:
        title = _get_title(element)
        company = _get_company(element)
        old_price = _get_old_price(element)
        price = _get_price(element)
        sold = _get_sold(element)
        link = _get_link(element)

        df.loc[len(df)] = [ title, company, old_price, price, sold, link ]
    return df


def scrape_socialdeal(url: str = 'https://www.socialdeal.nl/ontdek/eindhoven/') -> pd.DataFrame:
    """
    Scrapes socialdeal url, uses /eindhoven if url is not specified, return pandas df with results
    """

    # Scrape page
    elements = scrape_page(url)

    # Instantiante PD DataFrame and configure it
    df = pd.DataFrame(columns=['title', 'company', 'old_price', 'price', 'sold', 'link'])
    df = gen_df(elements, df)

    # Display DataFrame
    df = df.sort_values('sold', ascending=False)
    return df

if __name__ == "__main__":
    scrape_socialdeal()
