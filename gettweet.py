from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
import json
from HTMLParser import HTMLParser
from elasticsearch import Elasticsearch
import sys

es = Elasticsearch()
#es.create(index="tweets",doc_type="json")

class listener(StreamListener):
    #i=1
    def on_data(self, data):
        try:
            data=json.loads(data)
           #tweet=data.split(',"coordinates":')[1].split(',"place":')[0]
            if data['coordinates']:
                lon, lat = data['coordinates']['coordinates']
                cont = data['user']['description']
                loc={}
                loc['latitude']=lat
                loc['longitude']=lon
                loc['content']=cont
                loc_json=json.dumps(loc)
                print loc_json
                es.index(index='twitters',doc_type='json',body=loc_json)
                return True
        except Exception, e:
            pass

    def on_error(self, status):
        print status


auth = tweepy.OAuthHandler('OBodyM84pC3r6pEnv74U2rPug','eMWLLBpMODKee8hh1znqelVeiCvAegRI76kb5PFjcobI4H8bk3')
auth.set_access_token('704101032201166848-O0oWQzWgFL0ZIwadD9XM6qgpg9IcfWt', 'COEFXtVcIzFOxDDQQ80re78e1jPvluRDb59YGPBhf9P7K')

#print 'start!'
twitterStream = Stream(auth, listener())
#print 'after create streams'
twitterStream.filter(track=["music","weather","company","good","and"])


