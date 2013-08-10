import urllib,urllib2,re,cookielib,sys,os,urlresolver
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from resources.libs import main
from t0mm0.common.net import Net
from t0mm0.common.addon import Addon
net = Net()
from urlresolver import common

#Mash Up - by Mash2k3 2012.


from universal import playbackengine, watchhistory
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.movie25', sys.argv)
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.movie25/art', ''))

    
wh = watchhistory.WatchHistory('plugin.video.movie25')



def Mplaylists(murl):
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        r=re.findall('<poster>(.+?)</poster>',link)
        if r:
                vip=r[0]
        else:
                vip='Unknown'
        f=re.findall('<fanart>(.+?)</fanart>',link)
        if f:
                fan=f[0]
        else:
                fan=art+'/fanart2.jpg'
        match=re.compile('<name>(.+?)</name><link>(.+?)</link><thumbnail>(.+?)</thumbnail><date>(.+?)</date>').findall(link)
        for name,url,thumb,date in match:
            main.addDirc(name+' [COLOR red] Updated '+date+'[/COLOR]',url,236,thumb,'',fan,'','','')
        info=re.findall('<info><message>(.+?)</message><thumbnail>(.+?)</thumbnail></info>',link)
        if info:
            for msg,pic in info:
                main.addLink(msg,'',pic)
        main.GA("MoviePL",vip+"-Directory")


def MList(mname,murl):
        mname  = mname.split('[C')[0]
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        r=re.findall('<poster>(.+?)</poster>',link)
        if r:
                vip=r[0]
        else:
                vip='Unknown'
        f=re.findall('<fanart>(.+?)</fanart>',link)
        if f:
                fan=f[0]
        else:
                fan=art+'/fanart2.jpg'
        info=re.findall('<info><message>(.+?)</message><thumbnail>(.+?)</thumbnail></info>',link)
        if info:
            for msg,pic in info:
                main.addLink(msg,'',pic)
        directory=re.compile('<dir><name>([^<]+)</name.+?link>([^<]+)</link.+?thumbnail>([^<]+)</thumbnail></dir>').findall(link)
        for name,url,thumb in directory:
                main.addDir(name,url,236,thumb)
        match=re.compile('<title>([^<]+)</title.+?link>([^<]+)</link.+?thumbnail>([^<]+)</thumbnail>').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for name,url,thumb in match:
            main.addPlayM(name+' [COLOR blue]'+vip+'[/COLOR]',url,237,thumb,'',fan,'','','')
            loadedLinks = loadedLinks + 1
            percent = (loadedLinks * 100)/totalLinks
            remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
            dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
            if (dialogWait.iscanceled()):
                return False   
        dialogWait.close()
        del dialogWait
        main.GA(vip+"-Directory",vip+"-Playlist")

def MLink(mname,murl,thumb):
        main.GA(mname,"Watched")
        ok=True
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Opening Link,5000)")
        infoLabels =main.GETMETAT(mname,'','','')
        video_type='movie'
        season=''
        episode=''
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
        hosted_media = urlresolver.HostedMediaFile(url=murl)
        try:
            if re.findall('billionuploads',murl):
                try:
                    stream_url =resolve_billionuploads(murl)
                except:
                        if hosted_media:
                                source = hosted_media
                                if source:
                                    xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,5000)")
                                    stream_url = source.resolve()
                                else:
                                    stream_url = False
                                    return
            elif re.findall('180upload',murl):
                    try:
                            stream_url =resolve_180upload(murl)
                    except:
                        if hosted_media:
                                source = hosted_media
                                if source:
                                    xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,5000)")
                                    stream_url = source.resolve()
                                else:
                                    stream_url = False
                                    return
            else:
                    if hosted_media:
                        source = hosted_media
                        if source:
                            xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,5000)")
                            stream_url = source.resolve()
                        else:
                            stream_url = False
                            return
                    else:
                        stream_url = murl
            infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
            # play with bookmark
            player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
            #WatchHistory
            if selfAddon.getSetting("whistory") == "true":
                wh.add_item(mname+' '+'[COLOR green]MoviePlaylist[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
            player.KeepAlive()
            return ok
        except:
            return ok

def resolve_billionuploads(url):

    try:
            #########
            dialog = xbmcgui.DialogProgress()
            dialog.create('Resolving', 'Resolving BillionUploads Link...')       
            dialog.update(0)
        
            print 'BillionUploads - Requesting GET URL: %s' % url
            html = net.http_GET(url).content
               
            #Check page for any error msgs
            if re.search('This server is in maintenance mode', html):
                print '***** BillionUploads - Site reported maintenance mode'
                raise Exception('File is currently unavailable on the host')

            #Set POST data values
            op = 'download2'
            rand = re.search('<input type="hidden" name="rand" value="(.+?)">', html).group(1)
            postid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
            method_free = re.search('<input type="hidden" name="method_free" value="(.*?)">', html).group(1)
            down_direct = re.search('<input type="hidden" name="down_direct" value="(.+?)">', html).group(1)
        
            #Captcha
            captchaimg = re.search('<img src="(http://BillionUploads.com/captchas/.+?)"', html)
        
            dialog.close()
        
            #If Captcha image exists
            if captchaimg:
                #Grab Image and display it
                img = xbmcgui.ControlImage(550,15,240,100,captchaimg.group(1))
                wdlg = xbmcgui.WindowDialog()
                wdlg.addControl(img)
                wdlg.show()
            
                #Small wait to let user see image
                time.sleep(3)
            
                #Prompt keyboard for user input
                kb = xbmc.Keyboard('', 'Type the letters in the image', False)
                kb.doModal()
                capcode = kb.getText()
            
                #Check input
                if (kb.isConfirmed()):
                    userInput = kb.getText()
                    if userInput != '':
                        capcode = kb.getText()
                    elif userInput == '':
                        Notify('big', 'No text entered', 'You must enter text in the image to access video', '')
                        return None
                else:
                    return None
                wdlg.close()
            
                data = {'op': op, 'rand': rand, 'id': postid, 'referer': url, 'method_free': method_free, 'down_direct': down_direct, 'code': capcode}

            else:
                data = {'op': op, 'rand': rand, 'id': postid, 'referer': url, 'method_free': method_free, 'down_direct': down_direct}

            #They need to wait for the link to activate in order to get the proper 2nd page
            dialog.close()
            common.addon.show_countdown(3, 'Please Wait', 'Resolving')
               
            dialog.create('Resolving', 'Resolving BillionUploads Link...') 
            dialog.update(50)
        
            print 'BillionUploads - Requesting POST URL: %s DATA: %s' % (url, data)
            html = net.http_POST(url, data).content
            dialog.update(100)
            link = re.search('&product_download_url=(.+?)"', html).group(1)
            link = link + "|referer=" + url
            return link

    except Exception, e:
        print '**** BillionUploads Error occured: %s' % e
        raise
    finally:
        dialog.close()

def resolve_180upload(url):

    try:
        datapath = addon.get_profile()
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving 180Upload Link...')
        dialog.update(0)
        
        puzzle_img = os.path.join(datapath, "180_puzzle.png")
        
        print 'MashUp 180Upload - Requesting GET URL: %s' % url
        html = net.http_GET(url).content

        dialog.update(50)
                
        data = {}
        r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)

        if r:
            for name, value in r:
                data[name] = value
        else:
            raise Exception('Unable to resolve 180Upload Link')
        
        #Check for SolveMedia Captcha image
        solvemedia = re.search('<iframe src="(http://api.solvemedia.com.+?)"', html)

        if solvemedia:
           dialog.close()
           html = net.http_GET(solvemedia.group(1)).content
           hugekey=re.search('id="adcopy_challenge" value="(.+?)">', html).group(1)
           open(puzzle_img, 'wb').write(net.http_GET("http://api.solvemedia.com%s" % re.search('<img src="(.+?)"', html).group(1)).content)
           img = xbmcgui.ControlImage(450,15,400,130, puzzle_img)
           wdlg = xbmcgui.WindowDialog()
           wdlg.addControl(img)
           wdlg.show()
        
           xbmc.sleep(3000)

           kb = xbmc.Keyboard('', 'Type the letters in the image', False)
           kb.doModal()
           capcode = kb.getText()
   
           if (kb.isConfirmed()):
               userInput = kb.getText()
               if userInput != '':
                   solution = kb.getText()
               elif userInput == '':
                   Notify('big', 'No text entered', 'You must enter text in the image to access video', '')
                   return False
           else:
               return False
               
           wdlg.close()
           dialog.create('Resolving', 'Resolving 180Upload Link...') 
           dialog.update(50)
           if solution:
               data.update({'adcopy_challenge': hugekey,'adcopy_response': solution})

        print '180Upload - Requesting POST URL: %s' % url
        html = net.http_POST(url, data).content
        dialog.update(100)
        
        link = re.search('<a href="(.+?)" onclick="thanks\(\)">Download now!</a>', html)
        if link:
            print '180Upload Link Found: %s' % link.group(1)
            return link.group(1)
        else:
            raise Exception('Unable to resolve 180Upload Link')

    except Exception, e:
        print '**** 180Upload Error occured: %s' % e
        raise
    finally:
        dialog.close()
