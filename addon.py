# -*- coding: utf-8 -*-
from urllib2 import Request,urlopen
from re import compile as Compile
from xbmc import log
from xbmcswift2 import Plugin

BASE='http://www.seirsanduk.com/'
header_string='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'

plugin=Plugin()

@plugin.route('/')
def index():
    log('path: [/]')
    items=[]
    source=openUrl(BASE)
    match=Compile('<a href="(.+?)"><img src="(.+?)".*>(.+?)<\/a').findall(source)
    for url_chann,thumbnail,name_f in match:
        thumbnail=BASE+thumbnail
        url_chann='http:'+url_chann
        item={'label':name_f,'thumbnail':thumbnail,'path':plugin.url_for('index_source',url=url_chann,name=name_f,icon=thumbnail)}
        items.append(item)
    return items     
 
@plugin.route('/stream/<url>/<name>/<icon>/')
def index_source(url,name,icon):
    log('path: [/stream/]')
    items=[]
    source=openUrl(url)
    match=Compile('file:"(.+?)"').findall(source)
    for url in match:
        item={'label':'Play: '+name,'thumbnail':icon,'path':url,'is_playable':True}
        items.append(item)
    return plugin.finish(items)
    
def openUrl(url):
    req=Request(url)
    req.add_header('User-Agent',header_string)
    response=urlopen(req)
    source=response.read()
    response.close()
    return source

if __name__ == '__main__':
    plugin.run()