import re,os
import urllib2,urllib
import xbmcplugin,xbmcgui,xbmcaddon
import weblogin

username=xbmcaddon.Addon().getSetting('username')
password=xbmcaddon.Addon().getSetting('password')

BASE='http://www.seirsanduk.com/login/'

def LIST_CHANNELS():
    source=weblogin.doLogin('',username,password,BASE)
    match=re.compile('<li><a href="(.+?)"><img src="(.+?)".*>(.+?)<\/a><\/li>').findall(source)
    for url,thumbnail,name in match:
        thumbnail=BASE+thumbnail
        addDir(name,url,1,thumbnail)

def INDEX_CHANNELS(name,url):
    url = BASE + url
    xbmc.log(url+username+password)
    source=weblogin.doLogin('',username,password,url)
    match=re.compile('file:"(.+?)"').findall(source)
    name='PLAY: '+name
    for url in match:
        addLink(name,url,'')	
		
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
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('IsPlayable','true')
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok

def addDir(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png",thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={ "Title": name })
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

params=get_params()
url=None
name=None
mode=None

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

xbmc.log("Mode: "+str(mode))
xbmc.log("URL: "+str(url))
xbmc.log("Name: "+str(name))

if mode==None or url==None or len(url)<1:
        LIST_CHANNELS()

elif mode==1:
    INDEX_CHANNELS(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))