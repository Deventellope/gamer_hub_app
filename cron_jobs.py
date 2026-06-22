from mongo_setup import games_collection, news_collection

from datetime import datetime


# format number to date
def format_number_to_date(numbers):
    formatted_date= datetime.fromtimestamp(numbers).strftime("%b %d, %Y")
    return formatted_date


# fetch format news data and the store
def fetch_trending_games():
    ...

# fetch, format news data and the store
def fetch_game_news_data(data):


    timestamp= data.get("timestamp")

    content_to_store= {
    "gid": "5189234812394823948",
    "appid": 1245620,
    "game_name": "Elden Ring",          # you add this from your DB
    "title": "ELDEN RING — Patch 1.12 Now Available",
    "url": "https://store.steampowered.com/news/app/1245620/...",
    "author": "FROM SOFTWARE",
    "content_preview": "Patch 1.12 addresses the following issues...",
    "feed_label": "Product Update",
    "published_at": format_number_to_date(timestamp) if timestamp else "",         # keep raw for sorting
    "published_readable": "Jun 03, 2025",
    "fetched_at": "2025-06-19T10:00:00" # when your cron ran
}

# fetch, format and store upcoming game releases
def fetch_news_data():
    ...



# fetch, format and store upcoming game releases
# top games must exist in orignal database too
def fetch_top_games():
    # data to store 
    # Name
    # platform
    # developer
    # genre
    # rating
    # year
    ...

# fetch, format and store upcoming game releases
def fetch_trend_releases():

    # name 
    # rating
    # genre
    # short description
    ...


def fetch_full_game_data():
    {
  "id": 3498,
  "name_original": "Grand Theft Auto V",

  "description_raw": "...", #cleaned full game description

  "released": "2013-09-17", #release date
  "tba": false,

  "background_image": "...",
  "background_image_additional": "...",

  "website": "https://www.rockstargames.com/gta-v",

  "rating": 4.48,
  "rating_top": 5, #4.48/5

  "metacritic": 97,
  "metacritic_url": "...",

  "playtime": 75, #average playtime hrs

  "added": 100000,

  "platforms": [], #xbox , pc what not

  "stores": [], #where to buy the gaame

  "developers": [], #studio 
  "publishers": [], #distribution company

  "genres": [],
  "tags": [], #keyword descriptions

  "esrb_rating": {}, #game PG

  "series_games": [], #other related games

    }