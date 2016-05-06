import sys
import urllib
import urllib2
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import CommonFunctions

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

common = CommonFunctions
common.plugin = "TVYO-1.0"
 
xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)
	
def buildMainMenu():
    url = build_url({'mode': 'diziler', 'link': WEB_PAGE_BASE + '/dizi/yerli-diziler'})
    li = xbmcgui.ListItem('Yerli Diziler', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    url = build_url({'mode': 'diziler', 'link': WEB_PAGE_BASE + '/dizi/yabanci-diziler'})
    li = xbmcgui.ListItem(u'Yabanc\u0131 Diziler', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

def buildDizilerMenu():
   result = common.fetchPage({"link": args['link'][0]})
   if result["status"] == 200:
		diziModulDiv = common.parseDOM(result["content"], "div", attrs = { "id": "module_diziler_listeleme_1" })
		diziListesiDiv = common.parseDOM(diziModulDiv, "div", attrs = { "class": "items" })
		diziListesiLi = common.parseDOM(diziListesiDiv, "li")
		
		diziAdlari = common.parseDOM(diziListesiLi, "em")
		diziLinkleri = common.parseDOM(diziListesiLi, "a", attrs = { "class": "play" }, ret = "href")
		diziCoverlari = common.parseDOM(diziListesiLi, "img", ret = "src")
		diziItemIdleri = common.parseDOM(diziListesiLi, "a", attrs = { "class": "add" }, ret = "item-id")
		diziAciklamalari = common.parseDOM(diziListesiLi, "p")
		
		for i in range(0, len(diziLinkleri)):
			url = build_url({'mode': 'dizi', 'link': diziLinkleri[i].replace("/dizi/", ""), 'itemId' : diziItemIdleri[i]})
			
			li = xbmcgui.ListItem(diziAdlari[i], iconImage=diziCoverlari[i], thumbnailImage=diziCoverlari[i])
			li.setArt({'poster': diziCoverlari[i], 'tvshow.poster': diziCoverlari[i], 'season.poster': diziCoverlari[i]})		
			li.setInfo(type="Video", infoLabels={"Label": diziAdlari[i], "Title": diziAdlari[i], "Plot": diziAciklamalari[i]})			
			
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

   xbmcplugin.endOfDirectory(addon_handle)
   
def buildDiziMenu():
    url = build_url({'mode': 'videolar', 'type': '1', 'link': args['link'][0], 'itemId': args['itemId'][0]})
    li = xbmcgui.ListItem(u'B\u00f6l\u00fcmler', iconImage=xbmc.translatePath('special://home/addons/' + ADDON_ID +'/bolumler.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    url = build_url({'mode': 'videolar', 'type': '3', 'link': args['link'][0], 'itemId': args['itemId'][0]})
    li = xbmcgui.ListItem('Fragmanlar', iconImage=xbmc.translatePath('special://home/addons/' + ADDON_ID +'/fragman.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    url = build_url({'mode': 'videolar', 'type': '4', 'link': args['link'][0], 'itemId': args['itemId'][0]})
    li = xbmcgui.ListItem('Klipler', iconImage=xbmc.translatePath('special://home/addons/' + ADDON_ID +'/klip.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)
	
def buildVideolarMenu():
	result = common.fetchPage({"link": WEB_PAGE_BASE + "/dizi/video/" + args['link'][0] + "?type=" + args['type'][0] + "&selectFilter=4&item_id=" + args['itemId'][0]})
	
	if result["status"] == 200:
		videoSection = common.parseDOM(result["content"], "section", attrs = { "id": "videos" })
		itemsDiv = common.parseDOM(videoSection, "div", attrs = { "class": "mask" })
		videoListesiLi = common.parseDOM(itemsDiv, "li")
		
		for i in range(0, len(videoListesiLi)):
			videoBasliklari = common.parseDOM(videoListesiLi[i], "em")
			videoAltBasliklari = common.parseDOM(videoListesiLi[i], "em", ret = "title")
			videoSloganlari = common.parseDOM(videoListesiLi[i], "span", attrs = { "class": "title no-hit" })
			videoResimleri = common.parseDOM(videoListesiLi[i], "img", ret = "data-original")
			videoLinkleri = common.parseDOM(videoListesiLi[i], "a", ret = "href")
			
			baslik = videoBasliklari[0] + " - " + videoSloganlari[0].replace(u"\u0130zle", "")
			
			url = build_url({'mode': 'videoOynat', 'link': WEB_PAGE_BASE + videoLinkleri[0], 'title': baslik.encode('utf-8', 'ignore'), 'thumbnail': videoResimleri[0]})
			li = xbmcgui.ListItem(baslik, iconImage='DefaultVideo.png', thumbnailImage = videoResimleri[0])
			li.setInfo(type='video', infoLabels={ 'label' : baslik, 'title': videoAltBasliklari[0] })
			li.setProperty('IsPlayable', 'true')
			li.setArt({'poster': videoResimleri[0], 'tvshow.poster': videoResimleri[0], 'season.poster': videoResimleri[0]})
			
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
	
	xbmcplugin.endOfDirectory(addon_handle)
	
def videoOynat():
	result = common.fetchPage({"link": args['link'][0]})
	
	if result["status"] == 200:
		playlistUrl = extract(result["content"], 'mobileUrl : \"', '",')
		
		response = urllib2.urlopen(playlistUrl)
		if response and response.getcode() == 200:
			content = response.read()
			playlistUrlRoot = extract(playlistUrl, 'http://', 'playlist.m3u8')
			
			videoUrl = 'http://' + playlistUrlRoot + extract(content, '#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1500000\n', '\n')
			showError(ADDON_ID, 'Video : %s ' % (videoUrl))
			li = xbmcgui.ListItem(args['title'][0], iconImage=args['thumbnail'][0], thumbnailImage=args['thumbnail'][0], path=videoUrl)
			li.setProperty("IsPlayable", "true")
			li.setInfo(type='Video', infoLabels={ "Title": args['title'][0], "Label" : args['title'][0]})
			xbmc.Player().play(item=videoUrl, listitem=li)
		else:
			showError(ADDON_ID, 'Video %s adresinde bulunamadi' % (playlistUrl))
	
def extract(text, startText, endText):
    start = text.find(startText, 0)
    if start != -1:
        start = start + startText.__len__()
        end = text.find(endText, start + 1)
        if end != -1:
            return text[start:end]
    return None
	
def showError(addonId, errorMessage):
    notify(addonId, errorMessage)
    xbmc.log(errorMessage, xbmc.LOGERROR)

def notify(addonId, message, timeShown=5000):
    addon = xbmcaddon.Addon(addonId)
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (addon.getAddonInfo('name'), message, timeShown, addon.getAddonInfo('icon')))
	
WEB_PAGE_BASE = 'https://www.tvyo.com'
ADDON_ID = 'plugin.video.tvyo'

mode = args.get('mode', None)

if mode is None:
	buildMainMenu()

elif mode[0] == 'diziler':
	buildDizilerMenu()
	
elif mode[0] == 'dizi':
	buildDiziMenu()	
	
elif mode[0] == 'videolar':
	buildVideolarMenu()
	
elif mode[0] == 'videoOynat':
	videoOynat()