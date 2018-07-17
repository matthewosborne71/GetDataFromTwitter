###############################################################################
## GetDataFromTwitter.py                                                     ##
###############################################################################

from GetAPICred import get_twitter_client
import json
import unicodedata
import re
import pandas as pd
from tweepy import Cursor
import time
import math
import urllib2
import datetime

# load in my API
client1,client2,client3 = get_twitter_client()
clients = [client1,client2,client3]

def IsRT(tweet):
    if ":" not in tweet:
        return False
    elif "RT @" not in tweet.split(":")[0]:
        return False
    else:
        return True

def ExtractRTInfo(tweet):
    RTUser = tweet.split(":")[0]
    RTUser = RTUser.split("@")[1]

    RT_text = tweet.split(":")[1]

    return RTUser,RT_text

# Grab a user's profile info
def GrabProfile(screen_name):
    try:
        profile = clients[0].get_user(screen_name = screen_name)
    except Exception:
        profile = "GrabProfile Didn't Work"

    return profile

def internet_on():
    try:
        urllib2.urlopen("https://www.google.com/")
        return True
    except urllib2.URLError, e:
        print "No Internet"
        return False

def GrabAllProfiles(path,csv,file,Type):
    import re
    from time import sleep

    print "Creating document to hold data"
    f = open(path + file, "w+")
    f.write("screen_name,id_str,created_at,protected,statuses_count," +
            "verified,followers_count,friends_count,description,location\n")
    f.close()

    g = open(path + "Errors.txt","w+")
    g.write("Name,Error\n")
    g.close

    print "Loading in Names"
    a = pd.read_csv(path + csv)

    f = open(path + file,"a")
    g = open(path + "Errors.txt","a")

    for chunk in paginate(list(a['id']),100):


        print "Checking Internet Connection"
        while internet_on() == False:
            print "waiting for connection to return"
            time.sleep(60)

        users = clients[0].lookup_users(chunk)
        for user in users:
            description = user.description
            description = unicodedata.normalize('NFKD',description).encode('ascii','ignore')
            description = str.replace(description, '\n', ' ')
            description = str.replace(description, '\r', ' ')
            description = str.replace(description, ',', '')
            description = str.replace(description,"'",'')
            description = str.replace(description,'"','')

            location = user.location
            location = unicodedata.normalize('NFKD',location).encode('ascii','ignore')
            location = str.replace(location, '\n', ' ')
            location = str.replace(location, '\r', ' ')
            location = str.replace(location, ',', '')
            location = str.replace(location,"'",'')
            location = str.replace(location,'"','')

            screen_name = user.screen_name
            id_str = user.id_str
            created_at = str(user.created_at)
            protected = str(user.protected)
            statuses_count  = str(user.statuses_count)
            verified = str(user.verified)
            followers_count = str(user.followers_count)
            friends_count = str(user.friends_count)

            #"screen_name,id_str,created_at,protected,statuses_count," +
                    #"verified,followers_count,friends_count,description,location\n"

            f.write(screen_name + "," + id_str + "," + created_at + "," + protected
                    + "," + statuses_count + "," + verified + "," + followers_count
                    + "," + friends_count + "," + description + "," + location
                    + "\n")

    f.close()

# This will grab all the tweets from a list of users, you need a code that
# gives you a path to store the data, and a folder name as inputself.
# Source must be either 'screen_name' or 'id'
def GrabTweets(path,Source,folder,Type):
    # get the api

    Errors = open(path + folder + "Errors.text", "a+")
    Errors.write("Log of errors for run at " + str(datetime.datetime.now()) + ".\n")

    # read in the screen_names, note currently for nba players
    df = pd.read_csv(path + Source)
    Users = df[Type]

    i = 0
    # for each user in the list of screen_names
    for name in Users:

        print "Checking Internet Connection"
        while internet_on() == False:
            print "waiting for connection to return"
            time.sleep(60)

        try:
            if i%3 == 0:
                client = clients[0]
            elif i%3 == 1:
                client = clients[1]
            elif i%3 == 2:
                client = clients[2]

            if Type == 'id':
                Timeline = Cursor(client.user_timeline, user_id = name,tweet_mode='extended',count = 200).pages(16)
            elif Type == 'screen_name':
                Timeline = Cursor(client.user_timeline, screen_name = name,tweet_mode='extended',count = 200).pages(16)
            else:
                print "Didn't enter correct type. Try again"
                break

            # t will hold all of the tweets
            t = open(path + folder + str(name) + ".csv", "w+")
            t.write("author,TweetID,created_at,retweet,retweet_count,favorite_count,text\n")

            # h will hold all the individual hashtags used
            h = open(path + folder + str(name) + "Hashtags.csv", "w+")
            h.write("author,tweetID,hashtag\n")

            # m will hold all the individual mentions used
            m = open(path + folder + str(name) + "Mentions.csv","w+")
            m.write("author,tweetID,mentionName\n")

            r = open(path + folder + str(name) + "Retweets.csv","w+")
            r.write("author,tweetID,RTUser,RTtext\n")

            print "Getting the tweets from " + str(name)
            i = 0
            for page in Timeline:
                for status in page:
                    if i%1000 == 0:
                        print i

                    if 'retweeted_status' in dir(status):
                        retweet = "True"
                        RTUser = status.retweeted_status.user.screen_name
                        tweet = status.retweeted_status.full_text

                    else:
                        retweet = "False"
                        tweet = status.full_text

                    tweet = unicodedata.normalize('NFKD', tweet).encode('ascii','ignore')
                    tweet = str.replace(tweet, '\n', ' ')
                    tweet = str.replace(tweet, '\r', ' ')
                    tweet = str.replace(tweet, ',', '')
                    tweet = str.replace(tweet, '"','')
                    tweet = str.replace(tweet,"'",'')
                    #s = s.encode('ascii',errors='ignore') decode('utf-8').encode('ascii', errors='ignore')

                    if retweet == "True":
                        RTtext = tweet
                        tweet = "RT @" + RTUser + ": " + RTtext

                    t.write(status.user.id_str + "," + str(status.id) + ","  + str(status.created_at) +
                    "," + retweet + "," + str(status.retweet_count) + "," +
                    str(status.favorite_count) + "," + tweet + "\n")
                    for hashtag in status.entities['hashtags']:
                        word = unicodedata.normalize('NFKD', hashtag['text']).encode('ascii','ignore')
                        h.write(status.user.id_str + "," + str(status.id) + "," + word + "\n")
                    for mention in status.entities['user_mentions']:
                        m.write(status.user.id_str + "," + str(status.id) + "," + mention['screen_name'] + "\n")
                    if retweet == "True":
                        r.write(status.user.id_str + "," + str(status.id) + "," +
                                RTUser + "," + RTtext + "\n")
                    i=i+1

            t.close()
            h.close()
            m.close()
            r.close()
        except:
            Errors.write(str(name) + " had and error.\n")
            print "There was an error for " + str(name)

        i = i + 1




def GetListMembers(owner,slug,FileName):
    members = []

    print "Grabbing those names!"
    for member in Cursor(clients[0].list_members, owner, slug).items():
        members.extend([member.screen_name])

    print "These names are great!"
    print "Let me write them down!"
    f = open(FileName+"_screen_names.csv","w+")
    f.write("screen_name \n")
    for name in members:
        f.write(name + "\n")

    f.close()

def Stick():
    NBATeams = pd.read_csv("NBATeams.csv")
    Teams = pd.DataFrame(NBATeams['screen_name'],columns=['screen_name'])

    NBALocalCommentators = pd.read_csv("NBALocalCommentators.csv")
    LocalCommentators = pd.DataFrame(NBALocalCommentators['screen_name'],columns=['screen_name'])

    NBAExecs = pd.read_csv("NBAExecs.csv")
    Execs = pd.DataFrame(NBAExecs['screen_name'],columns=['screen_name'])

    NBA_TNT = pd.read_csv("NBA_TNT_screen_names.csv")

    NBABeatWriters = pd.read_csv("NBABeatWriters_screen_names.csv")

    NBA_ESPN = pd.read_csv("NBA_ESPN_screen_names.csv")

    NBA_NonPlayers = pd.concat([Teams,LocalCommentators,Execs,NBA_TNT,NBABeatWriters,NBA_ESPN],ignore_index=True)
    NBA_NonPlayers = NBA_NonPlayers.drop_duplicates()

    NBA_NonPlayers.to_csv("NBA_NonPlayers_screen_names.csv",index=False)

def paginate(items,n):
    for i in range(0,len(items),n):
        yield items[i:i+n]

def GrabFollowers(screen_name):
    f = open(screen_name + "Users.csv","w+")
    f.write("screen_name,id,protected,verified,followers_count,friends_count,statuses_count,description\n")

    print "Getting " + screen_name + "'s profile."
    profile = GrabProfile(screen_name)
    Max = profile.followers_count
    max_pages = math.ceil(Max/5000)

    print "Grabbing Followers"

    i = 1
    Pages = Cursor(clients[0].followers_ids,screen_name=screen_name).pages(max_pages)
    for followers in Pages:
        for chunk in paginate(followers,100):

            i = i + 1

            print "Checking Internet Connection"
            while internet_on() == False:
                print "waiting for connection to return"
                time.sleep(60)

            users = clients[0].lookup_users(user_ids = chunk)
            for user in users:
                description = user.description
                description = unicodedata.normalize('NFKD',description).encode('ascii','ignore')
                description = str.replace(description, '\n', ' ')
                description = str.replace(description, '\r', ' ')
                description = str.replace(description, ',', '')


                f.write(user.screen_name + "," + user.id_str + "," +
                        str(user.protected) + "," + str(user.verified) + "," +
                        str(user.followers_count) + "," + str(user.friends_count)
                        + "," + str(user.statuses_count) + "," + description + "\n")
        if len(followers) == 5000:
            print "More results available, sleeping to avoid rate limit."
            time.sleep(60)

    f.close()

def TheGameSampling(seed1=440,seed2=614):
    import DataPaths as DP

    path = DP.GetPaths()

    OSU = pd.read_csv(path + "TheGame/OhioStateUsers.csv")
    OSU = OSU[OSU['protected'] == False]
    OSUscreen_names = OSU['screen_name'].sample(n=3000,random_state=seed1)
    del OSU

    Mich = pd.read_csv(path + "TheGame/UMichUsers.csv")
    Mich = Mich[Mich['protected'] == False]
    Michscreen_names = Mich['screen_name'].sample(n=3000,random_state=seed2)

    screen_names = pd.concat([OSUscreen_names,Michscreen_names])
    screen_names = screen_names.drop_duplicates()
    screen_names.rename('screen_name')
    screen_names.to_csv(path + "TheGame/" + "TheGameScreenNames.csv",index=False)

# This function will take in a query and pull the unique user_names of the
# people that have sent a tweet containing that query.
def FindTweeters(query,path,FileName,since_id=None):

    # Create or open the file that we will be writing the names to
    try:
        f = open(path+FileName,'r')
        f.close()
        f = open(path+FileName,"a")
    except:
        f = open(path+FileName,"w+")
        f.write("id,foundTweet\n")

    i = 0
    print "Grabbing People that have tweeted " + query
    for page in Cursor(clients[0].search, q=query,count=100,result_type="recent",
                        include_entities=True).pages(15):
        for status in page:
            if 'retweeted_status' in dir(status):
                retweet = "True"
                RTUser = status.retweeted_status.user.screen_name
                tweet = status.retweeted_status.full_text

            else:
                retweet = "False"
                tweet = status.full_text

            tweet = unicodedata.normalize('NFKD', tweet).encode('ascii','ignore')
            tweet = str.replace(tweet, '\n', ' ')
            tweet = str.replace(tweet, '\r', ' ')
            tweet = str.replace(tweet, ',', '')
            tweet = str.replace(tweet, '"','')
            tweet = str.replace(tweet,"'",'')
            #s = s.encode('ascii',errors='ignore') decode('utf-8').encode('ascii', errors='ignore')

            if retweet == "True":
                RTtext = tweet
                tweet = "RT @" + RTUser + ": " + RTtext


            f.write(status.user.id_str + "," + tweet + "\n")


    f.close()
