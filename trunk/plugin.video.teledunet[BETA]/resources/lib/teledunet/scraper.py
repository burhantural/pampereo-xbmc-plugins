import cookielib
import re
import urllib2
import os.path
import xbmc, xbmcaddon, xbmcgui
import gc
from math import ceil
from urllib2 import (urlopen, Request)
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup

# Import Plugin Settings
#__settings__ = xbmcaddon.Addon("plugin.video.teledunet")
__settings__ = xbmcaddon.Addon("plugin.video.teledunet[BETA]")

TELEDUNET_URL = 'http://www.teledunet.com/'
TELEDUNET_TIMEPLAYER_URL = 'http://www.teledunet.com/tv/?file=rtmp://www.teledunet.com:1935/teledunet/%s'
HTML_FALLBACK = 'htmlfallback.html'

# TESTMDOE PARAMS
TESTMODE_ERR_URL = 'IaMtEsTmOdE'

# For GOOGLE Cache Mode
GOOGLE_CACHE_URL = 'http://google.com/search?q=cache:%s'
#user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1'
headers={'User-Agent':user_agent,}

#icons paths und other Paramaters 
ICON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'img')
OK_ICON = os.path.join(ICON_PATH,'ok.png')
ERR_ICON = os.path.join(ICON_PATH,'error.png')
WARNING_ICON = os.path.join(ICON_PATH,'warning.png')
DISP_NAME = "TELEDUNET.COM"
DISP_TIME = int(ceil(float(__settings__.getSetting("NOTIFICATION_TIME")))) # value in ms


cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))



def _url(path=''):
	"""Returns a full url for the given path"""
	return urljoin(BASE_URL, path)

def get(url):
	"""Performs a GET request for the given url and returns the response"""
	try:	
		conn = urlopen(url)
		resp = conn.read()
		conn.close()
		return resp
	except IOError:
		pass
	return ""
	

def _html(url):
	"""Downloads the resource at the given url and parses via BeautifulSoup"""
	return BeautifulSoup(get(url), convertEntities=BeautifulSoup.HTML_ENTITIES)

def _get_channel_time_player(channel_name):
	url = TELEDUNET_TIMEPLAYER_URL % channel_name
	req = Request(url)
	req.add_header('Referer', TELEDUNET_URL)	# Simulate request is coming from website
	html = get(req)

	m = re.search('time_player=(.*);', html, re.M | re.I)
	time_player_str = eval(m.group(1))

	m = re.search('curent_media=\'(.*)\';', html, re.M | re.I)
	rtmp_url = m.group(1)

	return rtmp_url, repr(time_player_str).rstrip('0').rstrip('.')

def get_rtmp_params(channel_name):

    '''
	Recent hack in Teledunet service returns channel link as follows:
	rtmp://ks3313747.kimsufi.com:1935/teledunet/abu_dhabi_drama
	'''
    #m = re.search('(.*:.*).*\/(.*)', channel_name, re.M|re.I)
    #rtmp_url = m.group(1)
    #channel_name = m.group(2)

    rtmp_url,time_player_id = _get_channel_time_player(channel_name)

    return {
    'rtmp_url': rtmp_url,
    'playpath': channel_name,
    'app': 'teledunet',
    'swf_url': ('http://www.teledunet.com/tv/player.swf?'
                'bufferlength=5&'
                'repeat=single&'
                'autostart=true&'
                'id0=%(time_player)s&'
                'streamer=%(rtmp_url)s&'
                'file=%(channel_name)s&'
                'provider=rtmp'
               ) % {
				'time_player': time_player_id, 
				'channel_name': channel_name, 
				'rtmp_url': rtmp_url
				},
    'video_page_url': 'http://www.teledunet.com/tv/?channel=%s&no_pub' % channel_name,
    'live': '1'
    }
    
def update_htmlfallback():
	if (__settings__.getSetting("DISABLE_ONLINE_MODE") == "false"):
		html = _html(TELEDUNET_URL)
		if html.find(True) is not None : # if the website is online , we get a non-empty soup
			path = os.path.join(os.path.dirname(__file__),HTML_FALLBACK)
			file = open(path,'w')
			for div in html.findAll("div", { "class":"div_channel" }):
				print >> file ,div
			if (DISP_TIME) > 0 :
				xbmc.executebuiltin('Notification(%s,"Update HTMLFALLBACK file succsess",%d,%s)'%(DISP_NAME,DISP_TIME,OK_ICON))
			file.close()
		else :
			if (DISP_TIME) > 0 :
				xbmc.executebuiltin('Notification(%s,"Update HTMLFALLBACK file failed",%d,%s)'%(DISP_NAME,DISP_TIME,ERR_ICON))
	else :
		xbmc.executebuiltin('Notification(%s,"Online Mode disabled",%d,%s)'%(DISP_NAME,DISP_TIME,ERR_ICON))
	
def get_channels():
	#try online Mode
	html = _html(TELEDUNET_URL)
	items = _parse_html_online_mode(html)
	
	if not items:
		if (DISP_TIME) > 0 and (__settings__.getSetting("NOTIFICATION_WEBSITE_STATUS") == "true"):
			xbmc.executebuiltin('Notification(%s,Website is [COLOR red]offline[/COLOR],%d,%s)'%(DISP_NAME,DISP_TIME,ERR_ICON))
		try :
			items = _parse_html_google_mode(html)
		except IOError :  
			items = _parse_html_fallback_mode(html)
	else :
		if (DISP_TIME > 0) and (__settings__.getSetting("NOTIFICATION_WEBSITE_STATUS") == "true"):
			xbmc.executebuiltin('Notification(%s,Website is [COLOR green]online[/COLOR],%d,%s)'%(DISP_NAME,DISP_TIME,OK_ICON))
	gc.collect()
	return items

def _parse_html_online_mode(html):
	
	if (__settings__.getSetting("DISABLE_ONLINE_MODE") == "true") :
		html = _html(os.path.join(TELEDUNET_URL,TESTMODE_ERR_URL))
		items = []
		return items 
	
	items = _find_channels_in_html(html,True)
				
	return items

def _parse_html_google_mode(html):
	
	cache_url = GOOGLE_CACHE_URL % TELEDUNET_URL					
	if (__settings__.getSetting("DISABLE_GOOGLE_MODE") == "true") :
		#cache_url = os.path.join(cache_url,TESTMODE_ERR_URL)
		raise IOError
	
	request = Request(cache_url,None,headers)
	response =  urlopen(request)			
	data = response.read() 
	response.close()
	if DISP_TIME > 0 :
		xbmc.executebuiltin('Notification(%s,USE GoogleMode,%d,%s)'%(DISP_NAME,DISP_TIME,WARNING_ICON))
	
	html = BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
	items =_find_channels_in_html(html,False)
	return items

def _parse_html_fallback_mode(html):
	path = os.path.join(os.path.dirname(__file__),HTML_FALLBACK)
	if DISP_TIME > 0 :
		xbmc.executebuiltin('Notification(%s,USE FALLBACK,%d,%s)'%(DISP_NAME,DISP_TIME,WARNING_ICON))		
	html = BeautifulSoup(''.join(open(path).readlines()), convertEntities=BeautifulSoup.HTML_ENTITIES)
	items = _find_channels_in_html(html,False)
	return items

def _find_channels_in_html(html,coloration=[True,False]):
	color = '#009900'
	items = []
	'''
	for div in html.findAll("div", { "class":"div_channel" }):
		#print div,
		is_colored = color in div
		onClickEl = div.findAll('a')[0]['onclick']
		m = re.search('.*\'(.*)\'.*', onClickEl, re.M|re.I)
		if m is not None:
			channel_name = m.group(1)
			# Remove the '+' at the End to get RTMP_Params 
			if channel_name.endswith('+'):
				channel_name = channel_name[:-1]
			#print channel_name
			if (color in div['style']) and (coloration == True):
				items.append({
					 'thumbnail': div.findAll('img')[0]['src'],
					 'label': '[COLOR green]%(channelname)s[/COLOR]' % {'channelname': div.find('font').contents[0]},
					 'path': channel_name
				})
			else :
				items.append({
				 'thumbnail': div.findAll('img')[0]['src'],
				 'label': div.find('font').contents[0],
				 'path': channel_name
				})
	'''
	for div in html.findAll("div", {"class": "div_channel"}):
		is_working = color in div['style'],
		label_pattern = '[COLOR green]%s[/COLOR]' if ((is_working) and (coloration==True)) else '%s'
		path = re.sub('^.*\=', '', div.findAll('a')[1]['href'])

		items.append({
            'title': label_pattern % div.find('font').contents[0],
            'thumbnail': div.findAll('img')[0]['src'],
            'path': path
        })
	
	return items