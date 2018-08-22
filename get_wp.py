import urllib.request as ul
from lxml import etree, cssselect, html
from io import StringIO, BytesIO
import os, shutil
import argparse
import random

#optional argument for collection
parser = argparse.ArgumentParser()
parser.add_argument('-c','--collection', required=False)
parser.add_argument('-d','--destination', required=True)
args = parser.parse_args()

catStr = args.collection
dest = args.destination

if catStr is not None:
    url = 'https://unsplash.com/search/photos/'+catStr

else:
    #get featured category extensions and pick random one
    response = ul.urlopen('https://unsplash.com/collections')
    webContent = response.read()
    html = etree.HTML(webContent)
    result = etree.tostring(html, pretty_print=True, method="html")
    select = cssselect.CSSSelector('a')

    links = [ el.get('href') for el in select(html) ]
    titles = [ el.get('class') for el in select(html) ]

    dic = dict(zip(links, titles))
    links = iter(dic)

    choices = []
    category = None
    for l in dic.keys():
        if dic[l] == 'fM0CB _1CBrG':
            choices.append(l)

    category = random.choice(choices)

    url = 'https://unsplash.com'+category

print(url)

#get all <a> links
response = ul.urlopen(url)
webContent = response.read()
html = etree.HTML(webContent)
result = etree.tostring(html, pretty_print=True, method="html")
select = cssselect.CSSSelector('a')
links = [ el.get('href') for el in select(html) ]
titles = [ el.get('title') for el in select(html) ]
dic = dict(zip(links, titles))
links = iter(dic)

#empty folder
for the_file in os.listdir(dest):
    file_path = os.path.join(dest, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
    except Exception as e:
        print(e)

#get all download links and download photos to folder
i=0
for l in dic.keys():
    if dic[l] == 'Download photo':
        f=open(dest+str(i)+".jpg", 'wb')
        f.write(ul.urlopen(l).read())
        f.close()
        i+=1

