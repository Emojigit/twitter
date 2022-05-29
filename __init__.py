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
    tw_api_bearer = config.tw_api_bearer
except AttributeError:
    raise RuntimeError("Missing `tw_api_bearer` in config.py!")
TWClient = tw.AsyncClient(bearer_token=tw_api_bearer,return_type=dict)
tweetid_regex = re.compile(r"(http(s?)://twitter.com/([a-zA-Z0-9_-]+)/status/([0-9]+))(\?[a-zA-Z0-9%&=]+)?") # .match
tweetid_reply = "[Tweet Data]({url})\n__Tweeted by__: [{dname}](https://twitter.com/{by})\n__Tweeted at__: {time}\n{text}"
user_regex = re.compile(r"http(s?)://twitter.com/([a-zA-Z0-9_-]+)/?(\?[a-zA-Z0-9%&=]+)? ") # UNAME @ GP2
user_reply = "[{dname}](https://twitter.com/{uname}){verified}\n__Location__: {location}\n__URL__: {url}\n__Description__: {description}"
nf = "404 Not Found"
def rmduplicate(l):
    return list(dict.fromkeys(l))
def setup(bot,storage):
    @bot.on(events.NewMessage())
    async def tw_trymatch(event):
        text = event.text
        for x in rmduplicate(tweetid_regex.findall(text)):
            #await event.respond(str(x))
            id = int(x[3])
            tweet = await TWClient.get_tweet(id=id,expansions=["author_id"],tweet_fields=["created_at","author_id"],user_fields=["name"])
            #await event.respond(str(tweet))
            text = tweet["data"]["text"]
            await event.reply(tweetid_reply.format(time=tweet["data"]["created_at"],by=x[2],text=text,url=x[0],dname=tweet["includes"]["users"][0]["name"]),link_preview=False)
        for x in rmduplicate(user_regex.findall(text + " ")):
            uname = x[1]
            user = (await TWClient.get_user(username=uname,user_fields=["description","location","verified","url"]))["data"]
            #await event.respond(str(user))
            description = user["description"]
            if description == "":
                description = nf
            dname = user["name"]
            await event.reply(user_reply.format(dname=dname,uname=uname,description=description,location=user["location"] if "location" in user else nf,verified=" ✅" if user["verified"] else "",url=user["url"] if user["url"] != "" else nf),link_preview=False)


