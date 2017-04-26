import facebook
import json
import requests
import sys
import nltk
import random
from nltk.corpus import movie_reviews
import pickle
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC, LinearSVC, NuSVC 
from sklearn.linear_model import LogisticRegression,SGDClassifier



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

    print "     " + str(i+1) + '  posts treated'
    print "      this word appeared  " + str(appear) + "  times in posts"
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
    return likes


def counting_shares(posts, keyword):
    sh=0
    for user_posts in posts['data']: 
        if 'message' in user_posts and keyword in user_posts['message'].encode('utf-8'):
            idp=user_posts['id']    
            #print(idp)
            url = 'https://graph.facebook.com/%s/?fields=shares&access_token=%s' % (str(idp), ACCESS_TOKEN)
            posts2 = render_to_json(url)
            if 'shares' in posts2 and 'count' in posts2['shares'] and int(posts2['shares']['count'])!=0:
                sh += posts2['shares']['count']

        elif 'story' in user_posts and keyword in user_posts['story'].encode('utf-8'): 
            idp=user_posts['id'] 
            #print(idp)
            url = 'https://graph.facebook.com/%s/?fields=shares&access_token=%s' % (str(idp), ACCESS_TOKEN)
            posts2=render_to_json(url) 
            if 'shares' in posts2 and 'count' in posts2['shares'] and int(posts2['shares']['count'])!=0:
                sh += posts2['shares']['count']
    print "\t number of shares\t" + str(sh)
    return sh

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

def comments_link_and_date(company, keyword):
    ACCESS_TOKEN='EAAF3d97493QBAHq3MYwbZAUs3eK9y6LrzhlqcLkagHwdA8i2SOE1IjOU4tBnD3mnniFNG3sBJKFDqxE3BQhKVn8poPsh52zLICV9RuwmeZCy8mdzW3abq4n89GR8XdMjpHokXVQmDuqouSeP5Ux0SktR40hXMZD'
    more_test = [
    (['love', 'this', 'car'], 'positive'),
    (['love','and', 'like', 'car'], 'positive'),
    (['love','you', 'lot'], 'positive'),
    (['this', 'view', 'amazing'], 'positive'),
    (['feel', 'great', 'this', 'morning'], 'positive'),
    (['excited', 'about', 'the', 'concert'], 'positive'),
    (['best', 'friend'], 'positive'),
    (['not', 'like', 'this', 'car'], 'negative'),
    (['this', 'view', 'horrible'], 'negative'),
    (['feel', 'tired', 'this', 'morning'], 'negative'),
    (['not', 'looking', 'forward', 'the', 'concert'], 'negative'),
    (['enemy'], 'negative'),
    (['not','good','enough'], 'negative'),
    (['dont','like','trump'], 'negative'),
    (['fuck','bad','trump'], 'negative')]

    #get the pickle
    classifier_f = open("naive_bayes5k.pickle", "rb")
    classifier = pickle.load(classifier_f)
    classifier_f.close()


    #get the pickle documants
    classifier_f = open("documents.pickle", "rb")
    documents = pickle.load(classifier_f)
    classifier_f.close()
    #get the pickle 
    classifier_f = open("doc_feat.pickle", "rb")
    word_features = pickle.load(classifier_f)
    classifier_f.close()

    def document_features(document): 
        document_words = set(document) 
        features = {}
        for word in word_features:
            features['contains({})'.format(word)] = (word in document_words)
        return features

    #print((find_features(movie_reviews.words('neg/cv000_29416.txt'))))

    featuresets = [(document_features(rev), category) for (rev, category) in documents]

    random.shuffle(featuresets)

    # positive and negative data example:      
    train_set = featuresets[:10000]+more_test
    test_set =  featuresets[10000:]



    testing_set=test_set
    training_set = nltk.classify.apply_features(document_features, train_set)

    classifier = nltk.NaiveBayesClassifier.train(training_set)
    print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, test_set))*100)
    
    #save classifier pickle
    save_classifier = open("naive_bayes5k.pickle","wb")
    pickle.dump(classifier, save_classifier)
    save_classifier.close()
    
    resultsmessage=[]
    resultsdate=[]
    resultslink = []
    resultscom = []
    base_url = 'https://graph.facebook.com/'+str(company)
    fields = 'feed.limit(50){message,story,link,created_time}'
    url = '%s?fields=%s&access_token=%s' % (base_url, fields, ACCESS_TOKEN)
    i,pos,neg=0,0,0
    posts=render_to_json(url)
    for user_posts in posts['feed']['data']:        
        if 'message' in user_posts and (keyword in user_posts['message']):
                
                try:
                    idp=user_posts['id']

                    resultslink.append(user_posts['link'])
                    resultsmessage.append(user_posts['message'])
                    resultsdate.append(user_posts['created_time'])
                    base_url = 'https://graph.facebook.com/'+idp
                    url = '%s/comments?limit=1000&access_token=%s' % (base_url, ACCESS_TOKEN)   
                    posts2=render_to_json(url)
                    for i,c in enumerate(posts2['data']):
                    
                            resultscom.append(c['message'])
                            sentiment=classifier.classify(document_features(c['message'].split()))
                            if sentiment=='pos' or sentiment=='positive':
                                pos+=1
                            else:
                                neg+=1
                except Exception, e:
                    print 'exception 1', e
        elif 'story' in user_posts and (keyword in user_posts['story']):
                try:
                    idp=user_posts['id']
                    
                    resultslink.append(user_posts['link'])
                    resultsmessage.append(user_posts['message'])
                    resultsdate.append(user_posts['created_time'])
                    base_url = 'https://graph.facebook.com/'+idp
                    url = '%s/comments?limit=1000&access_token=%s' % (base_url, ACCESS_TOKEN)   
                    posts2=render_to_json(url)
                    for i,c in enumerate(posts2['data']):
                           
                            resultscom.append(c['message'])
                            sentiment=classifier.classify(document_features(c['message'].split()))
                            if sentiment=='pos' or sentiment=='positive':
                                pos+=1
                            else:
                                neg+=1 
                except Exception, e:
                    print 'exception 1', e
    #print ('positive comments'+str(pos))
    #print ('negative comments'+str(neg))
    comtype=pos+neg
    # tables: comments , date , message ,link. commentares_type
    return resultscom,resultsdate,resultsmessage,resultslink,pos,neg

