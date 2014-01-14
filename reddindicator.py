#!/usr/bin/python

import pynotify
import praw
import sys
import time
import os

# Reddit stuff

username = ''
password = ''
dir = os.path.dirname(os.path.realpath(__file__));

r = praw.Reddit('/u/'+username+' linux desktop notification system by /u/balrogath, v 0.8')
r.login(username, password)

# notifications we've already been notified about
already_done = []

# forever!
while True:
	try:
		print 'Retrieving messages'
		# lovely orangereds! filthy periwinkle...
		unread = r.get_unread()
		for message in unread:
			if message.id not in already_done:
				# we don't want to repeat notifications, now do we?
				already_done.append(message.id)
				print 'Displaying unread...'
				# truncate subject and body
				subj = message.subject[:30] + (message.subject[30:] and '...')
				body = message.body[:140] + (message.body[140:] and '...')
				# friendly
				auth = message.author.name

				# get da notification ready
				pynotify.init('reddit_indicator')

				# but what type of notification?
				if message.was_comment:	
					n = pynotify.Notification('Comment reply from %s'%(auth),
						'%s'%(body),
						dir+'/orangered.png')
				else:
					n = pynotify.Notification('Message from %s: %s'%(auth,subj),
						'%s'%(body),
						dir+'/orangered.png')

				# show the world! or whatever
				n.show()
		# yes, sleep.....				
		time.sleep(60)

	except Exception as e:
		# Ohnoes!
		print 'Error!'
		e = str(e)

		# show the error
		pynotify.init('reddit_indicator')
		n = pynotify.Notification("Error occured!",
			'%s'%(e),
			dir+'/redditerror.png')
		n.show()

		# log the error
		with open("redditerror.txt", "a") as errlog:
			errlog.write("\n\n"+e)

		# sleep a little bit longer than usual
		time.sleep(120)
