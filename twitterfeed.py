import requests
import telebot
import feedparser
import schedule
import time
import json
bot_token = 'TOKEN'
bot = telebot.TeleBot(bot_token)
def getJSON():
    with open('feeds.json') as json_file:
        feedd = json.load(json_file)
        return feedd
feeds = getJSON()
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hi %s,\nWelcome to Twitter Feed Bot. I can subscribe to Twitter feeds and send you latest tweets in Telegram.\nThanks.'%(message.from_user.first_name))

@bot.message_handler(commands=['add'])
def addFeed(message):
    try:
        twitter = message.text.split(' ')[1]
    except:
        twitter = None
    chat_id = message.chat.id
    try:
        if twitter != None:
            feed_url = f'https://nitter.net/{twitter}/rss'
            feed_url = feed_url.replace('@','')
            addFeeds(feed_url,chat_id)
        else:
            bot.send_message(message.chat.id, 'Please send Twitter account username like: \n/add @PlutoGateNetwork')
    except:
        bot.send_message(message.chat.id, 'Please send Twitter account username like: \n/add @PlutoGateNetwork. Something went wrong. Please report it @PlutoGateGroup')

def parseFeed(url):
    try:
        feed = feedparser.parse(url)
        latest_url = feed.entries[0].link
        latest_title = feed.entries[0].title
        final = [latest_title, latest_url]
        return final
    except:
        final = ['Error', 'Error']

def feedRunner():
    global feeds
    for tweets in feeds:
        try:
            latest_url = parseFeed(tweets['feedurl'])
            if latest_url != tweets['latest_url']:
                newparse = parseFeed(tweets['feedurl'])
                tweets['latest_url'] = newparse[1]
                bot.send_message(tweets['chat_id'], '%s\n%s'%(newparse[0],newparse[1].replace('nitter.net','twitter.com')))
            else:
                pass
        except:
            print("error")
            pass
    saveJSON(feeds)

def addFeeds(feedurl,chat_id):
    global feeds
    global count
    try:
        latest = feedparser.parse(feedurl)
        latest_feed = latest.entries[0].link
        latest_title = latest.entries[0].title
        new_entry = {'feedurl':feedurl,'chat_id':chat_id, 'latest_url':latest_feed}
        feeds.append(new_entry)
        saveJSON(feeds)
        bot.send_message(chat_id, f'Latest Tweet:\n\n{latest_title}\n\n{latest_feed.replace("nitter.net","twitter.com")}')
        bot.send_message(chat_id, 'Twitter Feed subscribed successfully.')
    except:
        bot.send_message(chat_id, 'Something went wrong with your Twitter feed. Please report it @PlutoGateGroup')
def saveJSON(data):
    with open('feeds.json', 'w') as outfile:
        json.dump(data, outfile)
bot.polling()

schedule.every(10).minutes.do(feedRunner)

while True:
    schedule.run_pending()
    time.sleep(1)
