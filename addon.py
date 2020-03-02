# -*- coding: utf-8 -*-
from urllib2 import Request,urlopen
from re import compile as Compile
from xbmc import log
from xbmcgui import Dialog
from xbmcswift2 import Plugin

BASE='http://www.seirsanduk.com/'

plugin=Plugin()

@plugin.route('/')
def index():
    log('path: [/]')
    items=[]
    source=openUrl(BASE)
    match=Compile('<a href="(.+?)"><img src="(.+?)".*>(.+?)<\/a').findall(source)
    for url,thumbnail,name in match:
        thumbnail=BASE+thumbnail
        url='http:'+url
        item={'label':name,'thumbnail':thumbnail,'path':plugin.url_for('index_source',url=url,name=name,icon=thumbnail)}
        items.append(item)
    return plugin.finish(items)
 
@plugin.route('/stream/<url>/<name>/<icon>/')
def index_source(url,name,icon):
    log('path: [/stream/'+url+'/'+name+'/'+icon+']')
    source=openUrl(url)
    match=Compile('file:"(.+?)"').findall(source)
    item={'label':name,'path':match[0]}
    plugin.play_video(item)
    Dialog().notification(name,'',icon,8000,sound=False)
    return plugin.finish(None,succeeded=False)
    
def openUrl(url):
    req=Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0')
    response=urlopen(req)
    source=response.read()
    response.close()
    return source

if __name__ == '__main__':
    plugin.run()