import requests
from .models import Quote
url = 'http://quotes.stormconsultancy.co.uk/random.json'
def get_random_quotes():
    response = requests.get(url).json()
    random_quote  = Quote(response.get("author"), response.get("quote"), response.get("permalink"))
    return random_quote