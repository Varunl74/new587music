import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Get this value from my.telegram.org/apps
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")

# Get your token from @BotFather on Telegram.
BOT_TOKEN = getenv("BOT_TOKEN")

# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = getenv("MONGO_DB_URI", None)

# Vars For API End Pont.
YTPROXY_URL = getenv("YTPROXY_URL", 'https://console.cloud.google.com/apis/credentials?authuser=3&project=myyoutubeapp-474314') ## xBit Music Endpoint.
YT_API_KEY = getenv("YT_API_KEY" , None ) ## Your API key like: xbit_10000000xx0233 Get from  https://t.me/SID_ELITE

## Other vaes
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 300))

# Chat id of a group for logging bot's activities
LOGGER_ID = int(getenv("LOGGER_ID"))

# Get this value from @FallenxBot on Telegram by /id
OWNER_ID = int(getenv("OWNER_ID"))

## Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/strad-dev131/music.git",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)  # Fill this variable if your upstream repository is private

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/musicbot_updates")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/musicbotssupport")

# Set this to True if you want the assistant to automatically leave chats after an interval
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))
ASSISTANT_LEAVE_TIME = int(getenv("ASSISTANT_LEAVE_TIME",  1000000000))


# Get this credentials from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "1c21247d714244ddbb09925dac565aed")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "709e1a2969664491b58200860623ef19")


# Maximum limit for fetching playlist's track from youtube, spotify, apple links.
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))


# Telegram audio and video file size limit (in bytes)
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 2048576004444))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 20737418244444))
# Checkout https://www.gbmb.org/mb-to-bytes for converting mb to bytes

PRIVATE_BOT_MODE_MEM = int(getenv("PRIVATE_BOT_MODE_MEM", 1))


CACHE_DURATION = int(getenv("CACHE_DURATION" , "86400"))  #60*60*24
CACHE_SLEEP = int(getenv("CACHE_SLEEP" , "3600"))   #60*60


# Get your pyrogram v2 session from @StringFatherBot on Telegram
STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)


BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}
file_cache: dict[str, float] = {}

START_IMG_URL = ["https://graph.org/file/cd4bc5dc275a425cf081a-4750effd0b3d307acc.jpg",
                 "https://graph.org/file/cf4c9c7e8f236cd6dad50-da9582cde551e2f9dc.jpg",
                 "https://graph.org/file/b310965aba32028e93378-c368d58f86b6c51448.jpg"]
    
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://graph.org/file/977aaecea0f7b3665d275-4181a2706f888aefcd.jpg"
)
PLAYLIST_IMG_URL = "https://graph.org/file/cf4c9c7e8f236cd6dad50-da9582cde551e2f9dc.jpg"
STATS_IMG_URL = "https://graph.org/file/dd9501a2e5f3ad59b051b-6787cccc214f00b5a2.jpg"
TELEGRAM_AUDIO_URL = "https://graph.org/file/b310965aba32028e93378-c368d58f86b6c51448.jpg"
TELEGRAM_VIDEO_URL = "https://graph.org/file/cf4c9c7e8f236cd6dad50-da9582cde551e2f9dc.jpg"
STREAM_IMG_URL = "https://graph.org/file/8e2d8a70d4ea1ce1feda3-87d5d4aa7348fe7cdc.jpg"
SOUNCLOUD_IMG_URL = "https://graph.org/file/8e2d8a70d4ea1ce1feda3-87d5d4aa7348fe7cdc.jpg"
YOUTUBE_IMG_URL = "https://graph.org/file/cf4c9c7e8f236cd6dad50-da9582cde551e2f9dc.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://graph.org/file/8e2d8a70d4ea1ce1feda3-87d5d4aa7348fe7cdc.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://graph.org/file/8e2d8a70d4ea1ce1feda3-87d5d4aa7348fe7cdc.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://graph.org/file/8e2d8a70d4ea1ce1feda3-87d5d4aa7348fe7cdc.jpg"



def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:360"))


if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )
