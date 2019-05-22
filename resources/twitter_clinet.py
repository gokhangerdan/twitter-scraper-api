import requests
from bs4 import BeautifulSoup
import json


def get_worldwide_trends():
    response = requests.get('https://twitter.com/i/trends').json()["module_html"]
    soup = BeautifulSoup(response, "html.parser")
    trend_items = soup.find_all("li", {"class": "trend-item"})
    trends = []
    for x in trend_items:
        trends.append(
            {
                "trend_name": x.attrs["data-trend-name"],
                "href": x.findChild("a", {"class": "pretty-link"}).attrs["href"],
                "tweet_count": x.findChild("div", {"class": "trend-item-stats"}).text
            }
        )
        
    return trends

def get_twitter_account(uname):
    headers = {
        'cookie': 'tfw_exp=0; personalization_id="v1_BLVDnoxa0ov95ERahyCOlg=="; guest_id=v1%3A155091605623166964; external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|8e8t2xd8A2w%3D; _ga=GA1.2.1121849784.1550916063; _gid=GA1.2.385525915.1551172560; dnt=1; ads_prefs="HBISAAA="; kdt=dLCOlcGxxeiWphHevmbwSGuks0qIMm1mvy78Klrn; remember_checked_on=1; twid="u=1090771556731678723"; auth_token=52738cdf88b93bf89cd5fe59c76b69df7b2cbd12; csrf_same_site_set=1; csrf_same_site=1; twtr_pixel_opt_in=Y; mbox=PC#8a8ca04344604685b873244022490955.26_14#1552388758|check#true#1551179218|session#de89c0c8194f44b98449d9386a854804#1551181018; ct0=e8d9846dc62d2a4d4eb2a382fb762afa; lang=en; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCJjodjRpAToHaWQiJTEz%250AYzc4YTY2YmExYjliNDEwYWM4MmJiZjdmMjNiMDJkOgxjc3JmX2lkIiU2MTZl%250AYWU4OTgyNDA2NjVjMTI4NzczODFkZTY0YjIxNQ%253D%253D--18aed5f06a6b6cba03e6004d569c33eedcd9f790',
        'x-push-state-request': 'true',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,tr-TR;q=0.8,tr;q=0.7',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'referer': 'https://twitter.com/{uname}'.format(uname=uname),
        'authority': 'twitter.com',
        'x-requested-with': 'XMLHttpRequest',
        'x-twitter-active-user': 'yes',
        'x-asset-version': '9c3f5b',
    }

    response = requests.get('https://twitter.com/{uname}'.format(uname=uname), headers=headers).json()

    return response['init_data']['profile_user']

def get_search_results(q):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://twitter.com/search?vertical=default&q={q}&src=typd'.format(q=q),
        'X-Requested-With': 'XMLHttpRequest',
        'X-Twitter-Active-User': 'yes',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    }

    params = (
        ('vertical', 'default'),
        ('q', q),
        ('src', 'typd'),
        ('composed_count', '0'),
        ('include_available_features', '1'),
        ('include_entities', '1'),
        ('include_new_items_bar', 'true'),
        ('latent_count', '0'),
        ('min_position', 'thGAVUV0VFVBaAwLutsoHi8B4WgIC26fWF4vAeEhikAhJjwusAAAH0P4BiTdLxqfwAAAAiD3C_941XQAEPcMQGrNdAAA9wwNG9V3AAD3DEDDgX4AAPcH4k7ZTAAA9waIXoF4AAD3BnI__XgAEPcLD0yteAAQ9wxBK0VrAAD3DEDYnWoAAPcMQSKJdwAA9ww3wrV-ABD3DEF66WwAAPcMQGrBeAAg9wVxSF1-AAD3DEFO8WwAEPcLWm9ddwAA9wvNu4VqABD3BZ9BSWsAAPcMQI4lbQAA9wWCw610ABD3DEEodXgAEPcMHZxRawAA9wxAdtF-AAD3DEDgTWwAAPcMGdMZdAAA9wZR8P1pAAD3DEBZLXcAAPcMQGqpfQAA9wvjtLFpABD3DEFGFWoAAPcHWyt1bQAA9wv7syV9AAD3BkF3OW0AEVABUcFQAlAAA='),
    )

    response = requests.get('https://twitter.com/i/search/timeline', headers=headers, params=params).json()["items_html"]

    soup = BeautifulSoup(response, "html.parser")

    tweets = soup.find_all("div", {"class": "tweet"})

    tweet_details = []
    for x in tweets:
        tweet_details.append(
            {
                "account": x.findChild("a", {"class": "account-group"}).attrs["href"],
                "tweet": x.findChild("a", {"class": "tweet-timestamp"}).attrs["href"],
                "timestamp": x.findChild("a", {"class": "tweet-timestamp"}).findChild("span").attrs["data-time"],
                "avatar": x.findChild("img", {"class": "avatar"}).attrs["src"],
                "full_name": x.findChild("strong", {"class": "fullname"}).text,
                "username": x.findChild("span", {"class": "username"}).text,
                "tweet_text": x.findChild("p", {"class": "tweet-text"}).text,
                "reply_count": x.findChild("span", {"class": "ProfileTweet-action--reply"}).findChild("span", {"class": "ProfileTweet-actionCount"}).attrs["data-tweet-stat-count"],
                "retweet_count": x.findChild("span", {"class": "ProfileTweet-action--retweet"}).findChild("span", {"class": "ProfileTweet-actionCount"}).attrs["data-tweet-stat-count"],
                "favorite_count": x.findChild("span", {"class": "ProfileTweet-action--favorite"}).findChild("span", {"class": "ProfileTweet-actionCount"}).attrs["data-tweet-stat-count"],
            }
        )

    return tweet_details