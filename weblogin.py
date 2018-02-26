# -*- coding: utf-8 -*-
import os,re,urllib,urllib2
import xbmc, xbmcgui
import cookielib

def check_login(source_login,username):
    logged_in_string='nav_vodlist'
    if re.search(logged_in_string,source_login,re.IGNORECASE):
        return True
    else:
        return False

def doLogin(cookiepath,username,password,url_to_open):
    #check if user has supplied only a folder path, or a full path
    if not os.path.isfile(cookiepath):
        #if the user supplied only a folder path, append on to the end of the path a filename.
        cookiepath=os.path.join(cookiepath,os.path.join(xbmc.translatePath('special://temp'),'cookies_seirsanduk.lwp'))
    #delete any old version of the cookie file
    try:
        os.remove(cookiepath)
    except:
        pass

    if username and password:
        login_url=url_to_open
        header_string='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
        login_data=urllib.urlencode({'user_name':username,'user_password':password,'user_rememberme':1,'login':'В+Х+О+Д'})
        req=urllib2.Request(login_url, login_data)
        req.add_header('User-Agent',header_string)
        cj=cookielib.LWPCookieJar()
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        response=opener.open(req)
        source_login=response.read()
        response.close()
        login=check_login(source_login,username)
        if login==True:
            cj.save(cookiepath)
            return source_login
        else:
            xbmcgui.Dialog().notification('[ Login ERROR ]','Wrong username or password!',xbmcgui.NOTIFICATION_ERROR,8000,sound=True)
            raise SystemExit
