import praw
import config
import time as time
import os
import requests
from PIL import Image

img_bool =  {'y':True,'n':False}
r_img_bool = {True:'y',False:'n'}
 #Clear the Terminal
os.system('clear')
print 'Welcome to MrMcCrary\'s Desktop Finder v%s \nCurrently looking in r/%s \nDefaults can be changed in config.py \nPress Control+C to cancel'%(config.ver,config.sub)
s = raw_input('Press \'S\' to choose settings (or press enter to use defaults) ')
print ''
if s.lower() == 's':
    # Set settings, if enter is pressed, use defaults in config.py
    sub = raw_input('Subreddit? (%s) '%(config.sub))
    # Use requests to see if the input is an invalid subreddit, or if it is down
    p = requests.get('https://www.reddit.com/r/%s'%(sub))
    if  p.status_code == 404:
        print 'Invalid input, using default subreddit'
        sub = config.sub
    elif sub == '':
        sub = config.sub
    
    postlimit = raw_input('Post limit? (%s) '%(config.postlimit))
    if not postlimit.isdigit():
        if postlimit != '':
            print 'Invalid input, using default post limit'
        postlimit = config.postlimit
    
    sleeptime = raw_input('Sleep time? (%s) '%(config.sleeptime))
    if not sleeptime.isdigit():
        if sleeptime != '':
            print 'Invalid input, using default sleep time'
        sleeptime = config.sleeptime

    save_images = raw_input('Save Images? y/n (%s) '%(r_img_bool[config.save_images]).lower())
    if save_images == 'y' or save_images == 'n':
        save_images = img_bool[save_images]
    else:
        if save_images != '':
            print 'Invalid input, using default settings for saving images'
        sleeptime = config.sleeptime

elif s == '':
    print 'Using defaults for settings'
    sub = config.sub
    postlimit = config.postlimit
    sleeptime = config.sleeptime
    save_images = config.save_images
    min_width = config.min_width
    min_height = config.min_height

def bot_login ():

    print '\nLogging in... \n '
    #Create a new Reddit instance
    r = praw.Reddit(username = config.username,
            password = config.password,
            client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent = "mrmccrary background bot v1.0")
    return r

def run_bot(r):
    #Open the record of images already used as f
    with open ('images_used.txt','a') as f:
        f.read
    print "Obtaining Top Picture in r/%s"%(sub)
    # Initialize if a new background has been found as false
    found = False
    # Loop through the hottest posts on r/earthporn
    for submission in r.subreddit(sub).hot(limit=postlimit):
        # Check if the URL is a direct link and the picture has been used yet
        if 'i.' in submission.url and submission.url not in images_used:
           
            print "New Desktop Found! \n"
            print  'Title:      ' + submission.title
            print  'Url:        ' + submission.url + '\n'

            print 'Downloading...'
            # Append the new URL to the list of used pictures
            images_used.append(submission.url)
            # If the picture is unused, download it
            ts = int(time.time())
            os.system("curl -s %s > pics/pic.jpg" %(submission.url))
            # Find the resolution of the picture
            '''with Image.open('pics/pic.jpg') as img:
                width, height = img.size
            if width < min_width or height < min_height and use_dims == 'y':
                found = True
                break
            elif width * height < min_width * min_height:
                found = True
                break
            if save_images == True:'''
            os.system("rsync -av -q pics/pic.jpg savedpics/%s.jpg" % (ts))
                 # Write the URL to the file of used pictures
            with open ('images_used.txt','a') as f:
                    f.write(submission.url + '\n' + '> saved as: ' + str(ts) + '.jpg in savedpics' '\n')
            #else:
            with open ('images_used.txt','a') as f:
                f.write(submission.url + '\n')
            print 'Done, New Desktop Set!'
            # Reset the dock to apply changes
            os.system("killall Dock")
            # Set that a new background has been found
            found = True
            break
        
    if found == False:
        print 'No New Desktops Found :('
    
    print 'Now Sleeping for %s seconds \n'%(sleeptime)
    # Try Again in an hour 
    time.sleep(config.sleeptime)

def get_used_images():
    with open ('images_used.txt','r') as f:
        # If there is no file, set images used to be blank
        if not os.path.isfile('images_used.txt'):
            images_used = []
        # Otherwise, set it equal to images_used.txt
        else:
            images_used = f.read()
            images_used = images_used.split('\n')
            images_used = filter(None, images_used)
        return images_used

r = bot_login()

# Initialize images_used
images_used = get_used_images()

while True:
    run_bot(r)