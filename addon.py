# -*- coding: utf-8 -*-
import urllib2
from re import compile as Compile
from xbmc import log
from xbmcgui import Dialog
from xbmcswift2 import Plugin

BASE=['http://www.seirsanduk.com/','http://www.seirsanduk.online']

header='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'

plugin=Plugin()

opener=urllib2.build_opener(urllib2.HTTPHandler,urllib2.HTTPRedirectHandler())
urllib2.install_opener(opener)

@plugin.route('/')
def index():
    log('path: [/]')
    items=[]
    for B in BASE:
        try:
            source=openUrl(B)
        except:
            source=None
        match=Compile('<a href="(.+?)"><img src="(.+?)".*>(.+?)<\/a').findall(source)
        if not match:
            continue
        break
    items=[{'label':name,'thumbnail':B+thumbnail,'path':plugin.url_for('index_source',url='http:'+url,name=name,icon=B+thumbnail)} for url,thumbnail,name in match]
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
    req=urllib2.Request(url)
    req.add_header('User-Agent',header)
    response=urllib2.urlopen(req)
    source=response.read()
    response.close()
    return source

if __name__ == '__main__':
    plugin.run()