from newsapi import NewsApiClient

api = None

def init_api(api_key):
    global api
    api = NewsApiClient(api_key=api_key)

def get_top_news(category="general"):
    global current_category
    try:
        return api.get_top_headlines(category=category, language="en")
    except:
        return None

def search_news(query):
    try:
        return api.get_everything(q=query, language="en")
    except:
        return None