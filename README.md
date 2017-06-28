# backgroundbot
A simple python bot that sets top posts from Reddit as background using PRAW.

# Setup
Set background to /path/to/backgroundbot/backgroundbot/pics. 

Create new script on reddit (https://www.reddit.com/prefs/apps). 

In config.py, set username and password, client_id, and client_secret to the relevant values

# Usage
$ python backgroundbot.py 

# Settings (config.py)
sub: subreddit name to search.

save_images: 'True' to save images to savedpics, 'False' not to.

sleeptime: Time between checking for new backgrounds (in seconds).

postlimit: Number of posts checked each time
