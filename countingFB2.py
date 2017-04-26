import facebook
import json
import requests
import sys
ACCESS_TOKEN='EAACEdEose0cBAFKyhKKW09mEgcOiJIaUtcZAUGaZC9bT6YgQLxMpFhRMHgfMen0C62yaPkBWaZCAGSPEObNetSusU7QWwf7LZAg1NaTkfryvDvrjE8sZCpHqnRgHyUJDKMfhqX39qeZCoa4fIMvBnnhmbFpDSIIs5ZCqgsG8tyPqXiKpmCyJf0vRdlNW4ReXkgZD'
if sys.stdout.encoding != 'cp850':
  sys.stdout = codecs.getwriter('cp850')(sys.stdout, 'strict')
if sys.stderr.encoding != 'cp850':
  sys.stderr = codecs.getwriter('cp850')(sys.stderr, 'strict')

def getid(_, postid):
	return(postid['id'])

	
def render_to_json(graph_url):
	# render graph url call to JSON
	web_response = requests.get(graph_url)
	json_data = web_response.json()
	return json_data


def counting_appearance(company, keyword):
	appear = 0
	i=0
	base_url = 'https://graph.facebook.com/'+str(company)
	fields = 'feed.limit(50){message,story}'
	url = '%s?fields=%s&access_token=%s' % (base_url, fields, ACCESS_TOKEN)
	posts=render_to_json(url)
	for i, user_posts in enumerate(posts['feed']['data']):
		if 'message' in user_posts and keyword in user_posts['message'].encode('utf-8'): 
		    appear += 1
	 	elif 'story' in user_posts and keyword in user_posts['story'].encode('utf-8'): 
		    appear += 1

	print "		" + str(i+1) + '  posts treated'
	print "		 this word appeared  " + str(appear) + "  times in posts"
	return(appear)


def counting_likes(posts, keyword):
	likes=0
	for user_posts in posts['data']:
		if 'message' in user_posts and keyword in user_posts['message'].encode('utf-8'):
			idp=user_posts['id']	
			#print(idp)
			url = 'https://graph.facebook.com/%s/likes?summary=true&access_token=%s' % (str(idp), ACCESS_TOKEN)
			posts2 = render_to_json(url)
			likes += posts2['summary']['total_count']

	 	elif 'story' in user_posts and keyword in user_posts['story'].encode('utf-8'):
			idp=user_posts['id']
			#print(idp)
			url = 'https://graph.facebook.com/%s/likes?summary=true&access_token=%s' % (str(idp), ACCESS_TOKEN)
			posts2 = render_to_json(url)
			likes += posts2['summary']['total_count']

	

	print "\t number of likes\t" + str(likes)



def counting_shares(posts, keyword):
	sh=0
	for user_posts in posts['data']: 
		if 'message' in user_posts and keyword in user_posts['message'].encode('utf-8'):
			idp=user_posts['id']	
			#print(idp)
			url = 'https://graph.facebook.com/%s/?fileds=shares&access_token=%s' % (str(idp), ACCESS_TOKEN)
			posts2 = render_to_json(url)
			if 'shares' in posts2 and 'count' in posts2['shares'] and int(posts2['shares']['count'])!=0:
				sh += posts2['shares']['count']

	 	elif 'story' in user_posts and keyword in user_posts['story'].encode('utf-8'): 
			idp=user_posts['id'] 
			#print(idp)
			url = 'https://graph.facebook.com/%s/?fileds=shares&access_token=%s' % (str(idp), ACCESS_TOKEN)
			posts2=render_to_json(url) 
			if 'shares' in posts2 and 'count' in posts2['shares'] and int(posts2['shares']['count'])!=0:
				sh += posts2['shares']['count']
	print "\t number of shares\t" + str(sh)

def counting_comments(posts, keyword): 
	comments=0
	for user_posts in posts['data']:
		if 'message' in user_posts and keyword in user_posts['message'].encode('utf-8'):
			idp=user_posts['id']	
			#print(idp)
			url = 'https://graph.facebook.com/%s/comments?summary=true&access_token=%s' % (str(idp), ACCESS_TOKEN)
			posts2 = render_to_json(url)
			comments += posts2['summary']['total_count']

	 	elif 'story' in user_posts and keyword in user_posts['story'].encode('utf-8'):
			idp=user_posts['id']
			#print(idp)
			url = 'https://graph.facebook.com/%s/comments?summary=true&access_token=%s' % (str(idp), ACCESS_TOKEN)
			posts2 = render_to_json(url)
			comments += posts2['summary']['total_count']

	

	print "\t number of comments\t" + str(comments)

def link_and_date(company, keyword): 
	base_url = 'https://graph.facebook.com/'+str(company)
	fields = 'feed.limit(50){message,story,link,created_time}'
	url = '%s?fields=%s&access_token=%s' % (base_url, fields, ACCESS_TOKEN)
	i=0
	posts=render_to_json(url)
	for user_posts in posts['feed']['data']:	 	
		if 'message' in user_posts and (keyword in user_posts['message']):
			    
				try:
					idp=user_posts['id']
					print 'creation date:\t%s link:\t%s'%(user_posts['created_time'],user_posts['link'])
					base_url = 'https://graph.facebook.com/'+idp
					url = '%s/comments?limit=1000&access_token=%s' % (base_url, ACCESS_TOKEN)	
					posts2=render_to_json(url)
					for i,c in enumerate(posts2['data']):
							print str(i)+'comment:\t'+c['message'].encode('utf-8')
				except Exception, e:
					print 'exception 1', e
		elif 'story' in user_posts and (keyword in user_posts['story']):
				try:
					idp=user_posts['id']
					print 'creation date:\t%s link:\t%s'%(user_posts['created_time'],user_posts['link'])
					base_url = 'https://graph.facebook.com/'+idp
					url = '%s/comments?limit=1000&access_token=%s' % (base_url, ACCESS_TOKEN)	
					posts2=render_to_json(url)
					for i,c in enumerate(posts2['data']):
							print str(i)+'comment:\t'+c['message'].encode('utf-8')
				except Exception, e:
					print 'exception 1', e
			
def main():
	list_companies = ["mosaiquefm","france24english","cnninternational", "cisco","pepsi" ]
	keyword = raw_input('write the keyword\t')
	graph=facebook.GraphAPI(access_token=ACCESS_TOKEN)
	for company in list_companies:
		print 'Rates for the ' + company + ' company by facebook'
		postid= graph.get_object(id=company, fields='about')
		idcompany = getid(company, postid)

		try:
			posts = graph.get_connections(id=idcompany, connection_name='feed', limit=30,With='location')
			ap = counting_appearance(company, keyword)
			if ap!=0:
					try:
						counting_likes(posts,keyword)
						counting_comments(posts,keyword)
						counting_shares(posts,keyword)
						link_and_date(company, keyword)
					except Exception, e:
						print 'exception 1', e
		except Exception, e:
				print 'exception2', e

if __name__ == '__main__':
	main()
