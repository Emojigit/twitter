# -*- coding: utf-8 -*-

__author__ = "Emoji"
__version__ = "1.0.0"
__url__ = "https://github.com/Emojigit/join_repeater"
__description__ = "Join repeat"
__dname__ = "join_repeater"

from telethon import events
import tweepy.asynchronous as tw
import config, re
from tweepy.errors import *
try:
    tw_api_key = config.tw_api_key
except AttributeError:
    raise RuntimeError("Missing `tw_api_bearer` in settings.py!")
TWClient = tw.AsyncClient(bearer_token=tw_api_bearer,return_type=dict)
tweetid_regex = re.compile(r"(http(s?)://twitter.com/([a-zA-Z0-9_-]+)/status/([0-9]+))(\?[a-zA-Z0-9%&=]+)?") # .match
tweetid_reply = "[Tweet Data]({url})\n__Tweeted by__: [{by}](https://twitter.com/{by})\n__Tweeted at__: {time}\n{text}"
user_regex = re.compile(r"http(s?)://twitter.com/([a-zA-Z0-9_-]+)/? ") # UNAME @ GP2
user_reply = "[{uname}](https://twitter.com/{uname}): {description}"
def setup(bot,storage):
    @bot.on(events.NewMessage())
    async def tw_trymatch(event):
        text = event.text
        for x in tweetid_regex.findall(text):
            #await event.respond(str(x))
            id = int(x[3])
            tweet = await TWClient.get_tweet(id=id,tweet_fields=["created_at","author_id"])
            await event.respond(str(tweet))
            text = tweet["data"]["text"]
            await event.reply(tweetid_reply.format(time=tweet["data"]["created_at"],by=x[2],text=text,url=x[0]),link_preview=False)
        for x in user_regex.findall(text + " "):
            uname = x[1]
            user = await TWClient.get_user(username=uname,user_fields=["description"])
            #await event.respond(str(user))
            description = user["data"]["description"]
            if description == "":
                description = "__No description__"
            await event.reply(user_reply.format(uname=uname,description=description),link_preview=False)


