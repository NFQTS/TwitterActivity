import requests
import pickle
import time
import pandas as pd

# Api Authentication stuff
bearer_token = "ENTER BEARER TOKEN HERE FROM TWITTER DEVELOPER ACCOUNT"
headers = {"Authorization": "Bearer {}".format(bearer_token)}



user_tweet_lists = {} # dictionary used to easily save lists into a pickle file

# these lists are to track which tweet ids have met specific criteria and is a temporary way to allow one tweet to add points for multiple criteria
# these will have to be replaced if more efficient ways of calling the API
metaduels_mention_list = []
metaduels_rt_list = []
hashtag_use_list = []
theo_founder_mention_list = []
theo_founder_rt_list = []
zac_founder_mention_list = []
zac_founder_rt_list = []
project_data = {}


# when script starts, loads lists of tweet ids from a pickle file so we don't count tweets multiple times
try:
    a_file = open("project_data.pkl", "rb")
    project_data = pickle.load(a_file)
    a_file.close()
    b_file = open("tweet_lists.pkl", "rb")
    user_tweet_lists = pickle.load(b_file)
    b_file.close()

    metaduels_mention_list = user_tweet_lists['Metaduels Mentions']
    metaduels_rt_list = user_tweet_lists['Metaduels RTs']
    hashtag_use_list = user_tweet_lists['Hashtag List']
    zac_founder_mention_list = user_tweet_lists['Zac Founder Mentions']
    zac_founder_rt_list = user_tweet_lists['Zac Founder RTs']
except:
    print("Couldn't find any save data, starting monitoring...")


def create_user(twitter_id):
    """Creates a User profile and stores it in the project data dictionary"""
    time.sleep(10) # delay to not spam API requests
    twitter_handle = check_user_name(twitter_id) #finds the users twitter handle based on their id
    project_data[twitter_id] = {'Twitter Handle': twitter_handle, 'Metaduels Mentions': 0, 'Metaduels RTs': 0,
                             'Hashtag Uses': 0, 'Theo Founder Mentions': 0, 'Theo Founder RTs': 0, 'Zac Founder Mentions': 0, 'Zac Founder RTs': 0}
    print(f"{twitter_handle}'s profile has been created!")


def check_user_name(twitter_ids):
    """Checks the User's Twitter handle based on their Twitter ID and returns that Twitter handle so we can store it"""
    url = f"https://api.twitter.com/2/users/{twitter_ids}"
    response = requests.request("GET", url, headers=headers)
    username_json = response.json()
    if 'errors' not in username_json: #code will break if the user is suspended from twitter, so this just uses their twitter id instead of a twitter handle
        username = username_json['data']['username']
    else:
        username = twitter_ids
    time.sleep(10)
    return username


def check_project_mentions():
    """Checks the Twitter API to find @metaduels mentions from the last 7 days, and also retweets that contain @metaduels.
    A point is rewarded for each mention and the Tweet ID is added to a list of tweets that have already been checked
    so we don't check tweets multiple times."""
    # NOTE: We should change the endpoint to only search for tweets that happen after a specific Tweet ID and add the ability
    # to manage that.
    print("Checking Metaduels Mentions")
    url = f"https://api.twitter.com/2/tweets/search/recent?query=%40metaduels%20-is%3Aretweet&max_results=10&tweet.fields=id,text,author_id"
    response = requests.request("GET", url, headers=headers)
    res_json = response.json()
    # Cycle through tweets and add tweet IDs to exclusion list
    if res_json['meta']['result_count'] >= 1: #this prevents the code from breaking if there are no results
        for tweet in res_json['data']:
            #print(tweet)
            if tweet['id'] not in metaduels_mention_list: # makes sure we don't count tweets more than once
                metaduels_mention_list.append(tweet['id'])
                user_id = tweet['author_id']
                if user_id not in project_data: #checks if User is in the system
                    try:
                        create_user(user_id)
                        project_data[user_id]['Metaduels Mentions'] += 1
                    except:
                        print("Problem found during project mention check...")
                elif user_id in project_data:
                    project_data[user_id]['Metaduels Mentions'] += 1
    print("Saving Data...")
    save_data()
    time.sleep(10)
    print("Project Mentions Checked!")
    print("Checking Metaduels RTs")
    url = f"https://api.twitter.com/2/tweets/search/recent?query=%40metaduels%20is%3Aretweet&max_results=10&tweet.fields=id,text,author_id"
    response = requests.request("GET", url, headers=headers)
    res_json = response.json()
    # Cycle through tweets and add tweet IDs to exclusion list
    if res_json['meta']['result_count'] >= 1:
        for tweet in res_json['data']:
            if tweet['id'] not in metaduels_rt_list:
                metaduels_rt_list.append(tweet['id'])
                user_id = tweet['author_id']
                if user_id not in project_data:
                    try:
                        create_user(user_id)
                        project_data[user_id]['Metaduels RTs'] += 1
                    except:
                        print("Problem found during project RT check...")
                elif user_id in project_data:
                    project_data[user_id]['Metaduels RTs'] += 1
    time.sleep(10)
    print("Project RTs Checked!")


def check_theo_founder_mentions():
    """Checks the Twitter API to find @theowebzone mentions from the last 7 days, and also retweets that contain @theowebzone.
    A point is rewarded for each mention and the Tweet ID is added to a list of tweets that have already been checked
    so we don't check tweets multiple times."""
    print("Checking Theo Founder Mentions")
    url = f"https://api.twitter.com/2/tweets/search/recent?query=%40theowebzone%20-is%3Aretweet&max_results=10&tweet.fields=id,text,author_id"
    response = requests.request("GET", url, headers=headers)
    res_json = response.json()
    # Cycle through tweets and add tweet IDs to exclusion list
    if res_json['meta']['result_count'] >= 1:
        for tweet in res_json['data']:
            if tweet['id'] not in theo_founder_mention_list:
                theo_founder_mention_list.append(tweet['id'])
                user_id = tweet['author_id']
                if user_id not in project_data:
                    try:
                        create_user(user_id)
                        project_data[user_id]['Theo Founder Mentions'] += 1
                    except:
                        print("Problem found during theo mention check...")
                elif user_id in project_data:
                    project_data[user_id]['Theo Founder Mentions'] += 1
                print("Theo Mention Found!")
    save_data()
    time.sleep(10)
    print("Theo Founder Mentions Checked!")
    print("Checking Theo Founder RTs")
    url = f"https://api.twitter.com/2/tweets/search/recent?query=%40theowebzone%20is%3Aretweet&max_results=10&tweet.fields=id,text,author_id"
    response = requests.request("GET", url, headers=headers)
    res_json = response.json()
    # Cycle through tweets and add tweet IDs to exclusion list
    if res_json['meta']['result_count'] >= 1:
        for tweet in res_json['data']:
            if tweet['id'] not in theo_founder_rt_list:
                theo_founder_rt_list.append(tweet['id'])
                user_id = tweet['author_id']
                if user_id not in project_data:
                    try:
                        create_user(user_id)
                        project_data[user_id]['Theo Founder RTs'] += 1
                    except:
                        print("Problem found during theo rt check...")
                elif user_id in project_data:
                    project_data[user_id]['Theo Founder RTs'] += 1
    save_data()
    time.sleep(10)
    print("Theo Founder RTs Checked!")


def check_zac_founder_mentions():
    """Checks the Twitter API to find @zac_denham mentions from the last 7 days, and also retweets that contain @zac_denham.
    A point is rewarded for each mention and the Tweet ID is added to a list of tweets that have already been checked
    so we don't check tweets multiple times."""
    print("Checking Zac Mentions")
    url = "https://api.twitter.com/2/tweets/search/recent?query=%40zac_denham%20-is%3Aretweet&max_results=100&tweet.fields=id,text,author_id"
    response = requests.request("GET", url, headers=headers)
    res_json = response.json()
    # Cycle through tweets and add tweet IDs to exclusion list
    if res_json['meta']['result_count'] >= 1:
        for tweet in res_json['data']:
            if tweet['id'] not in zac_founder_mention_list:
                zac_founder_mention_list.append(tweet['id'])
                user_id = tweet['author_id']
                if user_id not in project_data:
                    try:
                        create_user(user_id)
                        project_data[user_id]['Zac Founder Mentions'] += 1
                    except:
                        print("Problem found during zac mention check...")
                elif user_id in project_data:
                    project_data[user_id]['Zac Founder Mentions'] += 1
    save_data()
    time.sleep(10)
    print("Zac Founder Mentions Checked!")
    print("Checking Zac Founder RTs")
    url = f"https://api.twitter.com/2/tweets/search/recent?query=%40zac_denham%20is%3Aretweet&max_results=10&tweet.fields=id,text,author_id"
    response = requests.request("GET", url, headers=headers)
    res_json = response.json()
    # Cycle through tweets and add tweet IDs to exclusion list
    if res_json['meta']['result_count'] >= 1:
        for tweet in res_json['data']:
            if tweet['id'] not in zac_founder_rt_list:
                zac_founder_rt_list.append(tweet['id'])
                user_id = tweet['author_id']
                if user_id not in project_data:
                    try:
                        create_user(user_id)
                        project_data[user_id]['Zac Founder RTs'] += 1
                    except:
                        print("Problem found during zac rt check...")
                elif user_id in project_data:
                    project_data[user_id]['Zac Founder RTs'] += 1
    save_data()
    time.sleep(10)
    print("Zac Founder RTs Checked!")


def create_leaderboard():
    """Creates a dataframe that includes twitter ids, twitter handles, and activity scores"""
    # lists that help with creating the dataframe
    user_list = []
    handle_list = []
    activity_list = []
    for user in project_data:
        user_list.append(user)
        handle_list.append(project_data[user]['Twitter Handle'])
        activity_score = 0
        for metric in project_data[user]:
            if metric != 'Twitter Handle':
                activity_score += project_data[user][metric]
        activity_list.append(activity_score)

    print("Need to create a leaderboard")
    print("need to rank projects")
    df_data = {
        'User ID': user_list,
        'Twitter Handle': handle_list,
        'Activity': activity_list
    }
    rankings_df = pd.DataFrame(data=df_data).set_index(['User ID']).sort_values(by=['Activity'], ascending=False)
    print(rankings_df)


def save_data():
    """Saves data to pickle files"""
    a_file = open("project_data.pkl", "wb") # stores user data
    pickle.dump(project_data, a_file)
    a_file.close()
    b_file = open("tweet_lists.pkl", "wb") # stores the ids of old tweets that have already been checked
    pickle.dump(user_tweet_lists, b_file)
    b_file.close()

while True:
    try:
        check_project_mentions()
        check_theo_founder_mentions()
        check_zac_founder_mentions()
        create_leaderboard()
        print(f"Project user data: {project_data}")
    except:
        print("Random error... retrying soon.")
        time.sleep(30)
    time.sleep(60)