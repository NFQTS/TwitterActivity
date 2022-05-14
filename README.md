# TwitterActivity
Tracks mentions and retweets of NFT projects and founder accounts.

Things to note:
1.) You will need your own Twitter developer account to get access to their API. Applying for "Elevated access" is recommended.
2.) You will need to enter your Twitter developer "bearer token" in metaduelsv6.9.py
3.) I have inserted some delays just to prevent the API from getting spammed so you don't hit the rate limit, but I didn't put a lot of thought into it.
4.) Currently, data just prints to the console in the form of a dataframe, sorted by most active users.
5.) Data for User activity and the tweets that have been checked are saved to .pkl files. You'll have to figure out how to save the data to another format if you need.
6.) I was getting a random error that I believe was just caused by my unstable internet connection so I did my best to add some exception handling, but since I wasn't able to identify the root cause with 100% certainty... you'll have to just hope for the best lol. It appears to work fine on my end.

P.S. I'm fairly new to all of this so I apologize if this code is wonky or needs to be refactored. I did my best, I hope it helps!
