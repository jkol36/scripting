import tweepy
import time
import random
import sys


from twitter import Twitter, OAuth, TwitterHTTPError

# put your tokens, keys, secrets, and twitter handle in the following variables
#OAUTH_TOKEN = "258627515-yzBIDgWcRfw5elo5pN3WeQfKixq3LeLmwb7EApWy"#258627515-JifmjFB4a2VEvhcRmSMHvfDAp09VUvRpNlutCu7j
#OAUTH_SECRET = "I9POsNNsNepcAM6QQuAHpR6r9QBshviUBdxwXi7idPAYE"#DXTgUKRtfXqoePpIi9jwmiDg6EKqsUukByA7Yo6aso0Ow
#CONSUMER_KEY = "TsqbFXrDvQIRVouzqYZQ"#gJT8wlzS5BalkHca9JHkxUNyg
#CONSUMER_SECRET = "UFTXEedfELNM2OxvA2VzinGvPIWQ7owiutdVN66g"#tgX1cPvcXvn18YCUFxXFzZ1fxPn2SVaIzbBaBsgHTQjQrnEyEm
#TWITTER_HANDLE = "Jkol36"


OAUTH_TOKEN = "2422847353-l3qOkBVh9L5DA677VI4BWxjx9Z6dTDnr5plwbhz"
OAUTH_SECRET = "wve3puQk0NITKKBQhGyr8FzlOUQ8jLO8i4kCCgEyLZBxP"
CONSUMER_KEY = "KUS33tu1rs6mp0Fz780NJAQ6C"
CONSUMER_SECRET = "KY8tyYuvtZBuCWRAY4Swv63SZ35FlbwgL2XsalrDyiv6eNRhOR"
TWITTER_HANDLE = "Jkol36"
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_SECRET)
api = tweepy.API(auth)


t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
            CONSUMER_KEY, CONSUMER_SECRET))


def search_tweets(q, count=1000, result_type="recent"):
    """
        Returns a list of tweets matching a certain phrase (hashtag, word, etc.)
    """

    return t.search.tweets(q=q, result_type=result_type, count=count)


def api_dic():
    return dir(api)

def me_dic():
    return dir(api.me())
def dir_search_result(api_query):
    results = api_query
    return dir(results[0])
def fav_follow(keywords, count = 120, result_type="recent"):
    """
        Favorites tweets that match a certain phrase (hashtag, word, etc.)
    """
    
    result = search_tweets(keywords, count, result_type)
    time.sleep(02)
    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    num_followed, num_favorited = 0, 0
    tweets_favorited = []
    for tweet in result['statuses']:
        try:
            # don't favorite your own tweets
            if tweet['user']['screen_name'] == TWITTER_HANDLE:
                continue
            if tweet['id'] not in tweets_favorited:

                result = t.favorites.create(_id=tweet['id'])
                tweets_favorited.append(tweet['id'])
                num_favorited += 1

            if tweet['user']['screen_name'] != TWITTER_HANDLE and tweet['user']['id'] not in following:
                t.friendships.create(user_id=tweet['user']['id'], follow=True)
                following.update(set([tweet['user']['id']]))
                num_followed += 1

                print "favorited: %s" % (result['text']).encode('utf-8')

                print "followed " + tweet['user']['screen_name']




        # when you have already favorited a tweet this error is thrown
        except TwitterHTTPError as e:
            print "error: ", e
        
        time.sleep(02)
    print "You followed %d people" % num_followed
    print "You favorited %d statuses" % num_favorited
def auto_fav(q, count = 1000, result_type="recent"):
    """
        Favorites tweets that match a certain phrase (hashtag, word, etc.)
    """

    result = search_tweets(q, count, result_type)

    for tweet in result['statuses']:
        try:
            # don't favorite your own tweets
            if tweet['user']['screen_name'] == TWITTER_HANDLE:
                continue


            elif tweet['user']['lang'] == "en" and tweet['favorited'] == False:
                result = t.favorites.create(_id=tweet['id'])
                print "favorited: %s" % (result['text']).encode('utf-8')

        # when you have already favorited a tweet this error is thrown
        except TwitterHTTPError as e:
            print "error: ", e






def auto_follow(keywords, count = 5000):
    """
        Follows anyone who tweets about a specific phrase (hashtag, word, etc.)
    """

    result = search_tweets(keywords, count) 
    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    print "Now following people based on keyword {}".format(keywords)

    for tweet in result['statuses']:
        try:
            if tweet['user']['screen_name'] != TWITTER_HANDLE and tweet['user']['id'] not in following and tweet['user']['lang'] == 'en':
                t.friendships.create(user_id=tweet['user']['id'], follow=True)
                following.update(set([tweet['user']['id']]))

                print "followed " + tweet['user']['screen_name']

        except TwitterHTTPError as e:
            print "error: ", e

            # quit on error unless it's because someone blocked me
            if "blocked" not in str(e).lower():
                quit()


def auto_follow_followers():
    """
        Follows back everyone who's followed you
    """

    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    followers = set(t.followers.ids(screen_name=TWITTER_HANDLE)["ids"])

    not_following_back = followers - following

    for user_id in not_following_back:
        try:
            t.friendships.create(user_id=user_id, follow=True)
        except Exception as e:
            print e


def auto_unfollow_nonfollowers():
    api = tweepy.API(auth)

    """
        Unfollows everyone who hasn't followed you back
    """

    following = set(api.friends_ids())
    followers = set(api.followers_ids())

    # put user IDs here that you want to keep following even if they don't
    # follow you back
    
    not_following_back = following - followers

    for userid in not_following_back:
        api.destroy_friendship(user_id=userid)
        print "unfollowed{}".format(userid)
def auto_unfollow_allfollowers():
    api = tweepy.API(auth)
    """
    Unfollows all your followers
    """

    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])

    for userid in following:
        t.friendships.destroy(user_id=userid)



class TwitterUser():
    def __init_(self):
        followers_count = 0
        default_profile = None
        location = None
        Twitter_id = None
        screen_name = None
        followed = 0

def follow_influencers_followers(influencer):
    followed = 0
    for profile in tweepy.Cursor(api.followers, screen_name =influencer).items():
        try:
            user = TwitterUser()
            user.followers_count = profile.followers_count
            fake_account = profile.default_profile
            user.id = profile.id
            user.screen_name = profile.screen_name
            user.location = profile.location
            user.lang = profile.lang
            



            if user.followers_count > 100 and fake_account == False and user.lang == 'en':
                api.create_friendship(user.id, follow = False)
                followed += 1
                print "successfully followed %s" % (user.screen_name)
            else:
                continue
        except Exception, e:
            print e
    print 'done'




def dm_new_followers():
    api = tweepy.API(auth)
    message = "Hey, do you have any weddings coming up any time soon?"

    followers = api.followers_ids()
    sent_profiles = []
    f = open('layers_sent.pk', 'rb')
    exclude = f.readlines()
    for follower in followers:
        if follower not in exclude:
            try:
                api.send_direct_message(user_id = follower, text = message)
                sent_profiles.appened(follower)
                print "Sending %s" % follower
            except Exception, e:
                if "Rate Limit Exceeded" in str(e):
                    break
                else:
                    pass
    with open('sent_profiles.pk', 'wb') as outfile:
        pickle.dump(sent_profiles, outfile)
    f.close()
    


#auto_follow('ui')

def check_ratio():
    api = tweepy.API(auth)
    follower_count = api.me().followers_count
    friend_count = api.me().friends_count
    difference = follower_count - friend_count
    if difference >= 150:
        return {'action':'unfollow'}

    else: 
        return {'action':'follow_fav'}

def get_dms_from_file():
  with open('tross_dms.pk', 'rb') as infile:
    infile.read()

def main():
    checker = check_ratio()
    follow = False
    favorite = False
    unfollow = False
    send_direct_message = False
    sent_dms_count = 0
    hashtags = ['#startups', '#DIY', '#weddingideas', "#etsyweddings", "#weddinggifts", '#groomsmen', '#groomsmengift', '#bridalparty', '#bridalgifts']
    if checker['action'] == "unfollow":
        auto_unfollow_nonfollowers()
        main()

    elif checker['action'] == "follow_fav":
        follow = True
        favorite = True
        send_direct_message = True

    if follow == True:
      for i in hashtags:
          try:
              auto_follow(i, 100)
              time.sleep(20)
          except Exception, e:
              print e
              if "Rate limit exceeded" in str(e):
                  follow = False
              else:
                  pass

    if favorite == True:
        for i in hashtags:
            try:
                auto_fav(i, 300)
                time.sleep(20)
            except Exception, e:
                print e
                if "Rate limit exceeded" in str(e):
                    favorite = False
                    print favorite
                else:
                    pass
    if send_direct_message == True:
      dm_new_followers()

    time.sleep(86400)
    main()


    
main()
