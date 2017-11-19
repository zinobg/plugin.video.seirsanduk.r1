import urllib2
import urllib
import re
import xbmcplugin
import xbmcgui
import xbmcaddon
import os

from sqlite3 import dbapi2 as sqlite
try:
	DB = os.path.join(xbmc.translatePath("special://userdata/Database"), 'Textures13.db')
	db = sqlite.connect(DB)
	db.execute('Delete FROM texture WHERE url LIKE "%seirsanduk%"')
	db.commit()
	db.close()
except:
	pass

BASE = "http://www.seirsanduk.com/"

def CATEGORIES():
	req = urllib2.Request(BASE)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	source=response.read()
	response.close()
	match=re.compile('<li><a href="(.+?)"><img src="(.+?)".*>(.+?)</a></li>').findall(source)
	for url,thumbnail,name in match:
		url = BASE + url
		thumbnail = BASE + thumbnail
		req=urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response=urllib2.urlopen(req)
		source=response.read()
		response.close()
		match=re.compile('file:"(.+?)"').findall(source)
		for url in match:
			addLink(name,url,thumbnail)	
		
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

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
