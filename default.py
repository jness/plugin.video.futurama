import urllib,urllib2,re,xbmcplugin,xbmcgui

def getURL(url):
	useragent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
	req = urllib2.Request(url)
	req.add_header('User-Agent', useragent)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link
	
def getRTMP(uri):
	link = getURL('http://www.comedycentral.com/global/feeds/entertainment/media/mediaGenEntertainment.jhtml?uri=%s' % uri)
	streams = re.compile('(rtmpe://.*.mp4)').findall(link)
	return streams[-1]

def INDEX(url):
	link = getURL(url)
	match=re.compile("<a href=\"(http://www.comedycentral.com/full-episodes/futurama/(\S*))\">\n[\s]*<img width='\d*' height='\d*' src='(\S*)'").findall(link)
	
	for url,name,thumbnail in sorted(match):
		addDownLink(name, url, 2, thumbnail)


def VIDEOLINKS(url,name):
	link = getURL(url)
	uri = re.search('<param name="movie" value="http://media.mtvnservices.com/(.*)"', link).group(1)
	rtmp = getURL('http://shadow.comedycentral.com/feeds/video_player/mrss/?uri=%s' % uri)
	rtmp_uri = re.compile('<guid isPermaLink="false">(.*)</guid>').findall(rtmp)
	
	playlist = xbmc.PlayList(1)
	playlist.clear()
	
	stacked_url = 'stack://'
	for uri in rtmp_uri:
		stream = getRTMP(uri)
		stream = stream.replace('rtmpe', 'rtmp')
		stacked_url += stream.replace(',',',,')+' , '
	stacked_url = stacked_url[:-3]
	
	item = xbmcgui.ListItem(name)
	playlist.add(stacked_url, item)
	
	xbmc.Player().play(playlist)
	xbmc.executebuiltin('XBMC.ActivateWindow(fullscreenvideo)')
	

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


def addDownLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
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
	url = 'http://www.comedycentral.com/full-episodes/futurama'
	print ""+url
	INDEX(url)

elif mode==2:
	print ""+url
	VIDEOLINKS(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
