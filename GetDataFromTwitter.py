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
client = get_twitter_client()

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
        profile = client.get_user(screen_name = screen_name)
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


def GrabMediaProfiles():
    import re
    from time import sleep
    import DataPaths as DP

    path = DP.GetPaths()

    print "Creating document to hold data"
    f = open(path + "Media/" + "MediaProfiles.csv","w+")
    f.write("screen_name,id_str,created_at,protected,statuses_count," +
            "verified,followers_count,friends_count,description,location\n")
    f.close()

    g = open(path + "Media/" + "Errors.txt","w+")
    g.write("Name,Error\n")
    g.close

    print "Loading in Names"
    a = pd.read_csv(path + "Media/" + "MediaOutletsScreenNames.csv")

    f = open(path + "Media/" + "MediaProfiles.csv","a")
    g = open(path + "Media/" + "Errors.txt","a")
    i = 1

    for Person in a['screen_name']:

        print "Attempting to Grab Data for " + Person
        if i%180 == 0:
            sleep(16*60)

        Profile = GrabProfile(Person)
        print "Data Retrieved!"
        print "Let me Write this down!"
        if Profile != "GrabProfile Didn't Work":
            description = Profile.description
            description = unicodedata.normalize('NFKD',description).encode('ascii','ignore')
            description = str.replace(description, '\n', ' ')
            description = str.replace(description, '\r', ' ')
            description = str.replace(description, ',', '')

            if Profile.location == '':
                f.write(str(Profile.screen_name) + "," + str(Profile.id_str)  +
                    "," + str(Profile.created_at)  + "," + str(Profile.protected) + "," +
                    str(Profile.statuses_count)  + "," + str(Profile.verified) + "," +
                    str(Profile.followers_count) + "," + str(Profile.friends_count) + "," +
                    description + "," + "None\n")
            else:
                f.write(str(Profile.screen_name) + "," + str(Profile.id_str)  +
                    "," + str(Profile.created_at)  + "," + str(Profile.protected) + "," +
                    str(Profile.statuses_count)  + "," + str(Profile.verified) + "," +
                    str(Profile.followers_count) + "," + str(Profile.friends_count) + "," +
                    description +
                    "," + re.sub('[,]','',unicodedata.normalize('NFKD',Profile.location).encode('ascii','ignore')) +
                    "\n")
        else:
            g.write(Person + Profile + "\n")

        i=i+1




def GrabCelebProfiles():
    import re
    from time import sleep

    print "Creating document to hold data"
    f = open("CelebProfiles.csv","w+")
    f.write("screen_name,id_str,created_at,protected,statuses_count," +
            "verified,followers_count,friends_count,description,location\n")
    f.close()

    g = open("Errors.txt","w+")
    g.write("Name,Error\n")
    g.close

    print "Loading in Names"
    a = pd.read_csv("CelebsScreen_Names.csv")

    f = open("CelebProfiles.csv","a")
    g = open("Errors.txt","a")
    i = 1

    for Person in a['screen_name']:

        print "Attempting to Grab Data for " + Person
        if i%180 == 0:
            sleep(16*60)

        Profile = GrabProfile(Person)
        print "Data Retrieved!"
        print "Let me Write this down!"
        if Profile != "GrabProfile Didn't Work":
            description = Profile.description
            description = unicodedata.normalize('NFKD',description).encode('ascii','ignore')
            description = str.replace(description, '\n', ' ')
            description = str.replace(description, '\r', ' ')
            description = str.replace(description, ',', '')

            if Profile.location == '':
                f.write(str(Profile.screen_name) + "," + str(Profile.id_str)  +
                    "," + str(Profile.created_at)  + "," + str(Profile.protected) + "," +
                    str(Profile.statuses_count)  + "," + str(Profile.verified) + "," +
                    str(Profile.followers_count) + "," + str(Profile.friends_count) + "," +
                    description + "," + "None\n")
            else:
                f.write(str(Profile.screen_name) + "," + str(Profile.id_str)  +
                    "," + str(Profile.created_at)  + "," + str(Profile.protected) + "," +
                    str(Profile.statuses_count)  + "," + str(Profile.verified) + "," +
                    str(Profile.followers_count) + "," + str(Profile.friends_count) + "," +
                    description +
                    "," + re.sub('[,]','',unicodedata.normalize('NFKD',Profile.location).encode('ascii','ignore')) +
                    "\n")
        else:
            g.write(Person + Profile + "\n")

        i=i+1



def GrabNBAProfiles():
    import re
    from time import sleep

    print "Creating document to hold data"
    f = open("NBANonPlayerProfiles.csv","w+")
    f.write("screen_name,id_str,created_at,protected,statuses_count," +
            "verified,followers_count,friends_count,description,location\n")
    f.close()

    g = open("Errors.txt","w+")
    g.write("Name,Error\n")
    g.close

    print "Loading in Names"
    a = pd.read_csv("NBA_NonPlayers_screen_names.csv")

    f = open("NBANonPlayerProfiles.csv","a")
    g = open("Errors.txt","a")
    i = 1

    for Person in a['screen_name']:

        print "Attempting to Grab Data for " + Person
        if i%180 == 0:
            sleep(16*60)

        Profile = GrabProfile(Person)
        print "Data Retrieved!"
        print "Let me Write this down!"
        if Profile != "GrabProfile Didn't Work":
            description = Profile.description
            description = unicodedata.normalize('NFKD',description).encode('ascii','ignore')
            description = str.replace(description, '\n', ' ')
            description = str.replace(description, '\r', ' ')
            description = str.replace(description, ',', '')

            if Profile.location == '':
                f.write(str(Profile.screen_name) + "," + str(Profile.id_str)  +
                    "," + str(Profile.created_at)  + "," + str(Profile.protected) + "," +
                    str(Profile.statuses_count)  + "," + str(Profile.verified) + "," +
                    str(Profile.followers_count) + "," + str(Profile.friends_count) + "," +
                    description + "," + "None\n")
            else:
                f.write(str(Profile.screen_name) + "," + str(Profile.id_str)  +
                    "," + str(Profile.created_at)  + "," + str(Profile.protected) + "," +
                    str(Profile.statuses_count)  + "," + str(Profile.verified) + "," +
                    str(Profile.followers_count) + "," + str(Profile.friends_count) + "," +
                    description +
                    "," + re.sub('[,]','',unicodedata.normalize('NFKD',Profile.location).encode('ascii','ignore')) +
                    "\n")
        else:
            g.write(Person + Profile + "\n")

        i=i+1

# Grab Profile Data for all congressman, can be changed to grab for any list
# of screen_names
def GrabCongressProfileData():
    import re
    from time import sleep
    # Note, 180 profiles every 15 minutes

    # Create a csv file that will hold the profile info
    print "Creating the document that will hold the profile data"
    f = open("CongressionalTwitterProfiles.csv","w+")
    f.write("screen_name,id_str,created_at,protected,statuses_count," +
            "verified,followers_count,friends_count,description,location\n")
    f.close()

    # Create an error file to hold any user that has a typo in their screen_name
    g = open("Errors.txt","w+")
    g.write("CongressPerson,Error\n")
    g.close

    # Load in the files holding the screen_names of the congressmen
    print "Loading in the 115th Congress"
    a = pd.read_csv("HouseTwitter.csv")
    print a.head()
    b = pd.read_csv("SenateTwitter.csv")
    print b.head()
    c = a.append(b)

    print c.head()

    # open csv so it can be appended to
    f = open("CongressionalTwitterProfiles.csv","a")
    g = open("Errors.txt","a")
    i = 1


    #sleep(15*60) # This is only temporary and should be removed!
    for Person in c['screen_name']:

        print "Attempting to Grab Data for " + Person
        if i%180 == 0:
            sleep(16*60)

        Profile = GrabProfile(Person)
        print "Data Retrieved!"
        print "Let me Write this down!"
        if Profile != "GrabProfile Didn't Work":
            description = Profile.description
            description = unicodedata.normalize('NFKD',description).encode('ascii','ignore')
            description = str.replace(description, '\n', ' ')
            description = str.replace(description, '\r', ' ')
            description = str.replace(description, ',', '')

            if Profile.location == '':
                f.write(str(Profile.screen_name) + "," + str(Profile.id_str)  +
                    "," + str(Profile.created_at)  + "," + str(Profile.protected) + "," +
                    str(Profile.statuses_count)  + "," + str(Profile.verified) + "," +
                    str(Profile.followers_count) + "," + str(Profile.friends_count) + "," +
                    description + "," + "None\n")
            else:
                f.write(str(Profile.screen_name) + "," + str(Profile.id_str)  +
                    "," + str(Profile.created_at)  + "," + str(Profile.protected) + "," +
                    str(Profile.statuses_count)  + "," + str(Profile.verified) + "," +
                    str(Profile.followers_count) + "," + str(Profile.friends_count) + "," +
                    description +
                    "," + re.sub('[,]','',unicodedata.normalize('NFKD',Profile.location).encode('ascii','ignore')) +
                    "\n")
        else:
            g.write(Person + Profile + "\n")

        i=i+1

# This will grab all the tweets from a list of users, you need a code that
# gives you a path to store the data, and a folder name as inputself.
def GrabTweets(ScreenNameSource,folder):
    import DataPaths

    # get the data storage path
    path = DataPaths.GetPaths()

    # get the api
    client = get_twitter_client()

    Errors = open(path + folder + "Errors.text", "a+")
    Errors.write("Log of errors for run at " + str(datetime.datetime.now()) + ".\n")

    # read in the screen_names, note currently for nba players
    df = pd.read_csv(path + ScreenNameSource)
    Users = df['screen_name']

    # for each user in the list of screen_names
    for name in Users:

        print "Checking Internet Connection"
        while internet_on() == False:
            print "waiting for connection to return"
            time.sleep(60)

        try:
            Timeline = Cursor(client.user_timeline, screen_name = name, count = 200).pages(16)
            # t will hold all of the tweets
            t = open(path + folder + name + ".csv", "w+")
            t.write("author,TweetID,created_at,retweet,retweet_count,favorite_count,text\n")

            # h will hold all the individual hashtags used
            h = open(path + folder + name + "Hashtags.csv", "w+")
            h.write("author,tweetID,hashtag\n")

            # m will hold all the individual mentions used
            m = open(path + folder + name + "Mentions.csv","w+")
            m.write("author,tweetID,mentionName\n")

            r = open(path + folder + name + "Retweets.csv","w+")
            r.write("author,tweetID,RTUser,RTtext\n")

            print "Getting the tweets from " + name
            i = 0
            for page in Timeline:
                for status in page:
                    if i%1000 == 0:
                        print i
                    tweet = status.text
                    tweet = unicodedata.normalize('NFKD', tweet).encode('ascii','ignore')
                    tweet = str.replace(tweet, '\n', ' ')
                    tweet = str.replace(tweet, '\r', ' ')
                    tweet = str.replace(tweet, ',', '')
                    #s = s.encode('ascii',errors='ignore') decode('utf-8').encode('ascii', errors='ignore')

                    retweet = str(IsRT(tweet))
                    t.write(status.user.id_str + "," + str(status.id) + ","  + str(status.created_at) +
                    "," + retweet + "," + str(status.retweet_count) + "," +
                    str(status.favorite_count) + "," + tweet + "\n")
                    for hashtag in status.entities['hashtags']:
                        word = unicodedata.normalize('NFKD', hashtag['text']).encode('ascii','ignore')
                        h.write(status.user.id_str + "," + str(status.id) + "," + word + "\n")
                    for mention in status.entities['user_mentions']:
                        m.write(status.user.id_str + "," + str(status.id) + "," + mention['screen_name'] + "\n")
                    if retweet == "True":
                        RTUser,RTtext = ExtractRTInfo(tweet)
                        r.write(status.user.id_str + "," + str(status.id) + "," +
                                RTUser + "," + RTtext + "\n")
                    i=i+1

            t.close()
            h.close()
            m.close()
            r.close()
        except:
            Errors.write(name + " had and error.\n")
            print "There was an error for " + name
            print "I need to rest for a minute."
            time.sleep(60)



def GetListMembers(owner,slug,FileName):
    members = []

    print "Grabbing those names!"
    for member in Cursor(client.list_members, owner, slug).items():
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
    Pages = Cursor(client.followers_ids,screen_name=screen_name).pages(max_pages)
    for followers in Pages:
        for chunk in paginate(followers,100):

            i = i + 1

            print "Checking Internet Connection"
            while internet_on() == False:
                print "waiting for connection to return"
                time.sleep(60)

            users = client.lookup_users(user_ids = chunk)
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
