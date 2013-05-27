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

  listitem_video22 = xbmcgui.ListItem('MBC Masr ', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://boxeesporthunter.appspot.com/?url=279', listitem_video22, True)


  listitem_video = xbmcgui.ListItem('MBC 1 ', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://boxeesporthunter.appspot.com/?url=1', listitem_video, True)

  listitem_video2 = xbmcgui.ListItem('MBC 4', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://boxeesporthunter.appspot.com/?url=4', listitem_video2, True)

  listitem_video3 = xbmcgui.ListItem('MBC 3', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://boxeesporthunter.appspot.com/?url=3', listitem_video3, True)

  listitem_video4 = xbmcgui.ListItem('MBC Drama', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://boxeesporthunter.appspot.com/?url=2', listitem_video4, True)

  listitem_video5 = xbmcgui.ListItem('MBC Action', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://boxeesporthunter.appspot.com/?url=5', listitem_video5, True)

  listitem_video6 = xbmcgui.ListItem('MBC 2', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://boxeesporthunter.appspot.com/?url=271', listitem_video6, True)

  listitem_video7 = xbmcgui.ListItem('Al Hayat 1', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://boxeesporthunter.appspot.com/?url=272', listitem_video7, True)


  listitem_video8 = xbmcgui.ListItem('AlQahira wa Alnas', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://boxeesporthunter.appspot.com/?url=277', listitem_video8, True)


  listitem_video9 = xbmcgui.ListItem('Alsharqia', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://boxeesporthunter.appspot.com/?url=273', listitem_video9, True)


  listitem_video10 = xbmcgui.ListItem('Al Hayat 2', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://boxeesporthunter.appspot.com/?url=278', listitem_video10, True)


  listitem_video11 = xbmcgui.ListItem('DW', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://boxeesporthunter.appspot.com/?url=276', listitem_video11, True)


  listitem_video12 = xbmcgui.ListItem('Alarabya', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://boxeesporthunter.appspot.com/?url=6', listitem_video12, True)


  listitem_video13 = xbmcgui.ListItem('Al Somaria', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://boxeesporthunter.appspot.com/?url=274', listitem_video13, True)


  listitem_video14 = xbmcgui.ListItem('Al Rashid', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://boxeesporthunter.appspot.com/?url=275', listitem_video14, True)


  listitem_video9 = xbmcgui.ListItem('Arabic Movies - farfesh.com', thumbnailImage=__icon__)
  xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'rss://boxeesporthunterlnk.appspot.com/', listitem_video9, True)
 



  xbmcplugin.setContent(int(sys.argv[1]), 'episodes')

  # End of list...
  xbmcplugin.endOfDirectory(int(sys.argv[1]), True)

Main()
