import os
from pathlib import Path

LOG_LEVEL = os.getenv("LOG_LEVEL", 'info').upper()

BASE_DIR = Path(__file__).resolve().parent

RUN_HEADLESS = os.getenv("RUN_HEADLESS", "True").lower() == "true"

URLS = os.getenv("URLS", '').split(",")
URLS_FILE = os.getenv("URLS_FILE", 'urls.txt')
if URLS_FILE:
    with open(URLS_FILE) as urlfile:
        URLS = urlfile.read().split("\n")

TOKEN = os.getenv("TOKEN", '')
MY_ID = os.getenv("MY_ID", '')
TIME_TO_CHECK = os.getenv("TIME_TO_CHECK", '09:00')

SERVER_URL = os.getenv("SERVER_URL", "api.telegram.org")
