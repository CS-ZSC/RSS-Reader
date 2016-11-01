import os
import requests
from xml.etree import ElementTree as ET
from flask import Flask
from flask import render_template
import HTMLParser

html = HTMLParser.HTMLParser()
r = requests.get('http://spectrum.ieee.org/rss/computing/fulltext')

#tree = ET.parse('fulltext')
#root = tree.getroot()
root = ET.fromstring(r.text.encode('utf-8'))
channel = root.find('channel')

feed0 = []	# initialize an empty list
feed1 = []  # initialize an empty list
feed2 = []  # initialize an empty list

n = 0

for item in channel.findall('item'):
  if n == 18: break

  title = item.find('title').text
  link = item.find('link').text
  description = item.find('description').text
  thumbnail = item.find('{http://search.yahoo.com/mrss/}thumbnail').attrib['url']
  
  feed_item = {} # initalize an empty dictionary
  feed_item['title'] = title
  feed_item['link']  = link
  feed_item['desc']  = html.unescape(description)
  feed_item['thumb'] = thumbnail
  
  if   n % 3 == 0: feed0 += [feed_item]
  elif n % 3 == 1: feed1 += [feed_item]
  else:            feed2 += [feed_item]
  n += 1

app = Flask(__name__)
@app.route('/')
def rssread():
  return render_template('index.html', feed0=feed0, feed1=feed1, feed2=feed2)

if __name__ == '__main__':
  app.run(port=os.environ['PORT'])