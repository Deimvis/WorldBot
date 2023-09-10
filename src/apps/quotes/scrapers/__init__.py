from typing import List
from src.apps.quotes.utils import Quote

import requests
import re

def scrape_all() -> List[Quote]:
    r = requests.get('https://www.forbes.ru/forbeslife/dosug/262327-na-vse-vremena-100-vdokhnovlyayushchikh-tsitat')
    parsed_ = re.findall(r'<p class="yl27R" style="text-align:left;">.*?</p>', r.text)

    quote_text = []
    authors = []
    for i in range(len(parsed_)):
        string = parsed_[i]
        if (i % 2 == 0):
            text = re.search(r'[а-яА-Я].*?<', string)
            quote_text.append(text[0] if text else None)
        else:
            author = re.search(r'[а-яА-Я].*?<', string)
            authors.append(author[0] if author else None)

    quote_text = list(map(lambda string: string[:len(string) - 1].strip(), quote_text))
    authors = list(map(lambda string: string[:len(string) - 1].strip(), authors))

    quotes = []
    for text, author in zip(quote_text, authors):
        quote = Quote(author=author, text=text)
        quotes.append(quote)

    return quotes