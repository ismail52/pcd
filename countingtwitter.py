import tweepy
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import json

consumer_key = 'wrS98crsW28gM6MziFWivSzjP'
consumer_secret = 'GF9c3D3x6poOCSkD3wjV7mpT9lkO5kAmG2xShFIjQhxhU7Zzsm'
access_token = '848637592568557568-rm0H1bDIqnIx2TJuqQsYUzHQoTPkWqR'
access_token_secret = '8yvhFE6oOy08C2l8eYFVwOMbapbs1rZNAffgIAejeBjy4'

def counting_appearance(tweets, keyword):
	appear=0
	for i in tweets:
		if keyword in i.get('text').encode('utf-8'):
			appear+=1

	print "		 this word appeared  " + str(appear) + "  times in tweets"

def counting_favorite(tweets,keyword):
	fc=0
	for i in tweets:
		if keyword in i.get('text').encode('utf-8'):
			fc+=i.get('favorite_count')
	print "\t number of likes\t" + str(fc)

def counting_retweets_date(tweets,keyword):
	cr=0
	for i in tweets:
		if keyword in i.get('text').encode('utf-8'):
			cr+=i.get('retweet_count')
	print "\t number of retweets\t" + str(cr)

def text_and_date(tweets,keyword):
	for i in tweets:
		if keyword in i.get('text').encode('utf-8'):
			print unicode("tweet's text:\t "+i.get('text')).encode('utf-8')
			print " creation date: %s" % str(i.get('created_at')) 

"""x=twitter.statuses.user_timeline(screen_name="realdonaldtrump",count=10)
for i in x:
	print i.get('text').encode('utf-8')
	print i.get('favorite_count')
	print i.get('retweet_count')
	print i.get('created_at')
"""
def main():
	oauth = OAuth(access_token, access_token_secret, consumer_key, consumer_secret)
	twitter = Twitter(auth=oauth)
	list_companies = ["tf1","france24","cnn" ]
	keyword = raw_input('write the keyword\t')
	for company in list_companies:
		tweets=twitter.statuses.user_timeline(screen_name=company,count=90)

		print 'Rates for the ' + company + ' company by twitter'

		try:
			ap = counting_appearance(tweets, keyword)
			if ap!=0:
					try:
						counting_favorite(tweets,keyword)
						counting_retweets_date(tweets,keyword)
						text_and_date(tweets,keyword)
					except Exception, e:
						print 'exception 1', e
		except Exception, e:
				print 'exception2', e

if __name__ == '__main__':
	main()