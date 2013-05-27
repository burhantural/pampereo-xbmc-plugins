# -*- coding: utf-8 -*-

# Imports
import os, sys, time
import xbmc, xbmcgui, xbmcplugin, xbmcaddon

__settings__ = xbmcaddon.Addon(id='plugin.video.democracynow')
__icon__ = __settings__.getAddonInfo('icon')
__fanart__ = __settings__.getAddonInfo('fanart')
__language__ = __settings__.getLocalizedString

# Fanart
xbmcplugin.setPluginFanart(int(sys.argv[1]), __fanart__)

# Main
def Main():

  listitem_video22 = xbmcgui.ListItem('Series ', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://frfsh12.appspot.com/?url=series', listitem_video22, True)

  listitem_video23 = xbmcgui.ListItem('Movies ', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://boxeesporthunterlnk.appspot.com/', listitem_video23, True)

  listitem_video24 = xbmcgui.ListItem('Masrahiat ', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://frfsh12.appspot.com?url=2', listitem_video24, True)

  listitem_video25 = xbmcgui.ListItem('Farfesh tv  ', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://frfsh12.appspot.com?url=4', listitem_video25, True)

  listitem_video26 = xbmcgui.ListItem('Mawaheb ', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://frfsh12.appspot.com?url=7', listitem_video26, True)


  listitem_video27 = xbmcgui.ListItem('Video Clips ', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://frfsh12.appspot.com?url=0', listitem_video27, True)

  listitem_video28 = xbmcgui.ListItem('Funny Clips ', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://frfsh12.appspot.com?url=3', listitem_video28, True)

  listitem_video29 = xbmcgui.ListItem('Kids ', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://frfsh12.appspot.com?url=kids', listitem_video29, True)

  xbmcplugin.setContent(int(sys.argv[1]), 'episodes')

  # End of list...
  xbmcplugin.endOfDirectory(int(sys.argv[1]), True)

Main()
