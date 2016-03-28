from flask import Flask,jsonify,render_template,request
import sys
import json
from elasticsearch import Elasticsearch
#from flask_esclient import ESClient
import os
import requests

app = Flask(__name__)
application = app
app.config['ELASTICSEARCH_URL'] = 'http://52.38.81.155:9200/'
#esclient = ESClient(app)
#esc = Elasticsearch(['http://52.38.81.155:9200/'])
esc = Elasticsearch()

# r = requests.get("http://localhost:9200/tweet/_search/?size=5000")


@app.route('/')
def approot():
	return render_template('twitterMap.html')

@app.route('/tweets', methods=['GET', 'POST'])
def hello_world():
	res=[];
	# keyword=keyword.encode('utf-8')
	keyword=request.form['keyword']
	print "keyword",keyword
	response = esc.search(index="twitters", body={"from" : 0, "size" : 1000, "query": {"match": {"content": keyword}}})
	print len(response["hits"]["hits"])
	for hit in response["hits"]["hits"]:
		lati=hit["_source"]["latitude"]
		longi=hit["_source"]["longitude"]
		#print hit

		pos={}
  		pos["latitude"]=lati
  		pos["longitude"]=longi
  		#pos_json=json.dumps(pos)
  		res.append(pos)
	# index=0
	# while (index<length):
	# 	data3=data2[index]
	# 	data5=data3["_source"]
	# 	#print data5
	# 	res.append(data5)
	# 	#print data5
	# 	index=index+1
	#list0=[{'latitude':40.1234,'longitude':-74.981}]
	#print res
	print res
	return jsonify({'data':res})
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')