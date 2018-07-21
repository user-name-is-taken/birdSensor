#!/usr/bin/env python2.7
# tweetpic.py take a photo with the Pi camera and tweet it
# by Alex Eames http://raspi.tv/?p=5918
import tweepy
from datetime import datetime
import os
import time
import keys


#OAuth process, using the keys and tokens
auth=tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Creation of the actual interface, using authentication
api=tweepy.API(auth)
def tweeting_loop():
        b_p_d= "/home/pi/birds/bird_pics" #bird_pic_directory
        cmd="ls "+b_p_d
        fp=os.popen(cmd)
        lis=fp.read().split()
        fp.close
        for pic in lis:
                tweet(pic)
                
                
def follow_back():
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()

def tweet(photo_name,errors=0):
    """Send the tweet with photo"""
    try:
        i=datetime.now()  #take time and date for filename
        now=i.strftime('%Y%m%d-%H%M%S')
        photo_path="/home/pi/birds/bird_pics"+photo_name
        status='Photo auto-tweet from Pi:'+ i.strftime('%Y/%m/%d %H:%M:%S')
        api.update_with_media(photo_path,status=status)#pass photo_path
        os.remove(photo_path)
        print "tweet successful"
    except tweepy.error.TweepError:
        print "tweet error"
        """if errors<=3:
            time.sleep(3)
            return tweet(photo_name,errors+1)"""
    except OSError:
        print "OSError "+photo_path+" this was tweeded, and not deleted"
