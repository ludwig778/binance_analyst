from os import environ

API = "https://api.binance.com"

CACHE_DIR = "cache_dir"

API_KEY = environ.get("API_KEY")
SECRET_KEY = environ.get("SECRET_KEY")

assert API_KEY, "API_KEY must be set"
assert SECRET_KEY, "SECRET_KEY must be set"
