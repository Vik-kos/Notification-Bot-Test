import requests
from bs4 import BeautifulSoup
import pandas

def strike(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result

def get_titles(deals):
    #print(type(deals))
    titles = deals.find_all("a", href = True)
    titles_text = [title["title"][4:] for title in titles]
    return titles_text
    

def get_prices(deals):
    old_prices = [deals.find("del", class_ = "oldPreis").text]
    new_prices = [deals.find("span", class_ = "newPreis").text]
    prices = deals.find_all("div", class_ = "nowPrice")
    for price in prices:
        old_prices.append(price.find("del").text)
        new_prices.append(price.find("p").text)
    
    return old_prices, new_prices


def get_mmoga_deals():
    s = requests.Session()
    url = "https://www.mmoga.com"
    html_text = s.get(url).text

    soup = BeautifulSoup(html_text, "lxml")
    #print(soup)
    deals = soup.find("div", class_ = "row")
    #print(deals)
    titles = get_titles(deals)
    old_prices, new_prices = get_prices(deals)
    game_deals = {
        'title': titles,
        'new_price': new_prices,
        'old_price': old_prices
    }
    pandas.DataFrame(game_deals).to_csv("game-deals.csv")

    

if __name__ == '__main__':
    get_mmoga_deals()
    
