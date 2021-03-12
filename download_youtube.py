# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 20:34:28 2021

@author: ghosty
"""
import youtube_dl 
import os
import requests
#from bs4 import BeautifulSoup
#import re


#========================= find playlist ======================================
def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

def find_all_videos(playlist_url):
    response = requests.get(playlist_url)
    playlist = list(find_all(response.text, 'watch?'))
    count =len(playlist)
    print(count)
    videos=[]
    for i in range(count):
        offset = playlist[i]
        video = 'https://www.youtube.com/watch?v='+response.text[offset+8:offset+19]
        videos.append(video)
        print("[%02d]" % (i+1),video)
    return videos

def read_playlist_file(filename):
    with open(filename) as f:
        videos=f.read().splitlines()
    for i in range(len(videos)):
        print(videos[i])
    return videos   
        
#========================= download youtube ===================================
def download_video(download_url, destFileFolder):
    #ref: https://github.com/Dstri26/YoPlaDo-Youtube-Playlist-Downloader/
    #進入下載目錄
    if not os.path.isdir(destFileFolder):
        os.mkdir(destFileFolder)
    os.chdir(destFileFolder) 

    #開始下載
    try:        
        #設定下載選項
        ydl_opts = {
            #'format': 'bestvideo[ext=mp4]+bestaudio[ext=aac]/best[ext=mp4]/best', #1080p or other best
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', #1080p or other best
            #'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]',
            #'outtmpl': '[] %(title)s.mp4'
            'outtmpl': '%(title)s.mp4'
            }        
        #下載
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:            
            #ydl.cache.remove()
            ydl.download([download_url])
    except:
        print("Exception occured. Either the video has no quality as set by you, or it is not available. Skipping video")     

def download_playlist(playlist, destFileFolder):     
    for i in range(len(playlist)):
        download_video(playlist[i], destFileFolder)
        
def download_queue(playlist_queue):
    for i in range(len(playlist_queue)):
        destFileFolder=playlist_queue[i][0]
        playlist_url = playlist_queue[i][1]
        playlist = find_all_videos(playlist_url)
        #playlist = read_playlist_file("E:\\playlist.txt")
        download_playlist(playlist, destFileFolder)  
    
#========================= rename files =======================================
def rename(destFileFolder):   
    for count, filename in enumerate(os.listdir(destFileFolder)):         
        src = destFileFolder + '\\' + filename
        dst = destFileFolder + '\\' "[%02d]" % (count+1) + filename.replace("[]","").replace("繁中完整版 ","").replace("｜胡歌 ｜林依晨｜劉詩詩｜袁弘","")
        #dst = destFileFolder +  '\\' + filename.replace("【酷的放剧场】","")
        dst = destFileFolder + '\\' + "[%02d]" % (count+1) + filename
        #dst = destFileFolder + '\\' + filename[:6]+".mp4"
        print(src,'--->',dst)
        os.rename(src, dst) 
#=================================== main() ===================================
if __name__ == '__main__': 
    playlist_queue=[
        ['G:\\吕不韦传奇', "https://www.youtube.com/playlist?list=PLb8LXNQ3GVIEcYbpkBvHRTGkGXnCs1y4l"],
        ['G:\\七劍下天山', "https://www.youtube.com/playlist?list=PLb8LXNQ3GVIED2K6iNPAREKNtneaUCGdc"],
        ['G:\\糊涂县令郑板桥', "https://www.youtube.com/playlist?list=PLSIJismKOisGZclPziO56RdJAaK0UIMgK"],
        ['G:\\天师钟馗', "https://www.youtube.com/playlist?list=PLSIJismKOisGwADtH8x59_ZJDLBE3HS63"],
        ['H:\\流星蝴蝶剑', "https://www.youtube.com/playlist?list=PLSIJismKOisGiS6PkRAHJa0rZ_YL06en8"],
        ['H:\\天涯明月刀', "https://www.youtube.com/playlist?list=PLSIJismKOisEBVlfiBTMpKD4GdD03ZPui"],
    ]
    #download_video("https://www.youtube.com/watch?v=Nzi3UNVRlNs", "E:\\書劍恩仇錄"'") #single file
    #playlist=find_all_videos("https://www.youtube.com/playlist?list=PLayweIoGTMC74ltVU53kDrtl_NCx4NN0)
    playlist=read_playlist_file("E:\\playlist.txt")
    download_playlist(playlist, "E:\\Movie") #playlist
    #download_queue(playlist_queue)
    #rename("G:\\新碧血劍")