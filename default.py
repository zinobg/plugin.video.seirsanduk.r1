# -*- coding: utf-8 -*-
import urllib2,urllib
from re import compile as Compile
import xbmcplugin
from xbmcgui import ListItem as ListItem

BASE_TK='http://televizora.tk/'
BASE_US='http://seirsanduk.us/'

header_string='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'

def openUrl(url):
    req=urllib2.Request(url)
    req.add_header('User-Agent',header_string)
    response=urllib2.urlopen(req)
    source=response.read()
    response.close()
    return source

def LIST_CHANNELS():
    try:
        BASE=BASE_TK
        xbmc.log("Trying: "+BASE)
        source=openUrl(BASE)
    except:
        BASE=BASE_US
        xbmc.log("Trying: "+BASE)
        source=openUrl(BASE)
    if source:
        match=Compile('<a href="(.+?)"><img src="(.+?)".*>(.+?)<\/a').findall(source)
        for url_chann,thumbnail,name_f in match:
            thumbnail=BASE+thumbnail
            addDir(name_f,url_chann,1,thumbnail)

def PLAY_URL(url,name,thumbnail):
    channel_source=openUrl(url)
    url_01=Compile('file:"(.+?)"').findall(channel_source)
    prog_01=Compile('<div class="title">(.+?)<\/div>').findall(channel_source)
    name_r=name+" | "+prog_01[0]
    for url in url_01:
        addLink(name_r,url,thumbnail)
		
def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                 param[splitparams[0]]=splitparams[1]
    return param

def addLink(name,url,iconimage):
    ok=True
    liz=ListItem(name,iconImage="DefaultVideo.png",thumbnailImage=iconimage)
    liz.setInfo(type="Video",infoLabels={"Title":name})
    liz.setProperty('IsPlayable','true')
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok

def addDir(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumbnail="+urllib.quote_plus(iconimage)
    ok=True
    liz=ListItem(name,iconImage="DefaultFolder.png",thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={ "Title": name })
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

params=get_params()
url=None
name=None
mode=None
thumbnail=None

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass
try:
    thumbnail=urllib.unquote_plus(params["thumbnail"])
except:
    pass

xbmc.log("Mode: "+str(mode))
xbmc.log("URL: "+str(url))
xbmc.log("Name: "+str(name))
xbmc.log("Icon: "+str(thumbnail))

if mode==None or url==None or len(url)<1:
    LIST_CHANNELS()

elif mode==1:
    PLAY_URL(url,name,thumbnail)

xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)