# !/usr/bin/env python3
import os
import sys
from mk.mp3_util import MP3,ID3
from mutagen import File
from yt_dlp import  YoutubeDL

# 提取yt_dlp信息
def  extract_info(url):
    ydl = YoutubeDL()
    info = ydl.extract_info(url, download=False)
    return info

def download(url:str,title:str=None,cover_url:str=None):
    """下载mp3格式的音乐
    Args:
        url (str): 歌曲网址
        name (str): 歌曲[-歌手]
        cover_url (str, optional): 封面url. Defaults to None.
    """ 
    if title != None:
        outtmpl = f'{title}.%(ext)s'
    else:
        outtmpl = '%(title)s.%(ext)s'
        
    ydl_opts = {
        'quiet': True,
        'no_color': True,
        'format': 'bestaudio/best',
        'outtmpl': outtmpl,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': 0
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        
    if  title != None:
        mp3 = MP3(f'{title}.mp3')
        if title.find('-') != -1:
            song = title.split('-')[0]
            artist = title.split('-')[1]
            mp3.add_title(song)
            mp3.add_artist(artist)
        else:
            mp3.add_title(title)
        if cover_url != None:
                mp3.add_cover(cover_url)
        else:
            info = extract_info(url)
            if  'thumbnail' in info:
                thumbnail = info['thumbnail']
                mp3.add_cover(thumbnail)
        mp3.save()
    else:
        info = extract_info(url)
        title = info['title']
        mp3 = MP3(f'{title}.mp3')
        mp3.add_title(title)
        if  cover_url != None:
            mp3.add_cover(cover_url)
        else:
            if  'thumbnail' in info:
                thumbnail = info['thumbnail']    
                mp3.add_cover(thumbnail)
        mp3.save()
    
    print('下载完成!')
    
def clip(path:str,start:str,end:str):
    """剪辑音乐

    Args:
        path (str): 歌曲文件url
        start (str): 开始时间(格式 00:00:00)
        end (str): 结束时间(格式 00:00:00)
    """ 
    try:
        audio=File(path)
        img_data = audio.tags._DictProxy__dict['APIC:Cover'].data
    except:
        img_data = None
    command = f'ffmpeg -i {path} -ss {start} -t {end} -acodec copy output.mp3'
    # 执行命令
    os.system(command)
    # 删除原文件
    os.remove(path)
    # 重命名
    os.rename('output.mp3',path)
    if  img_data!=None:
        # 添加封面
        mp3 = MP3(path)
        mp3.add_cover(img_data)
        mp3.save()
    print('剪辑完成!')

def main(args=None):
    if args == None:
        args = sys.argv[1:]
    # 校验args
    if len(args) == 0:
        print('configuration:\n\n'
            '---------------------------------------------\n'+
            '下载: mk url [title] [cover_url]\n'+
            '剪辑: mk -c path start end\n'
            '提取伴奏: mk -e path\n'
            '---------------------------------------------\n'
            )
        return
    flag = args[0]
    if flag == '-c':
        path = args[1]
        start = args[2]
        end = args[3]
        clip(path,start,end)
    elif flag == '-e':
        pass
    else:
        # 默认下载
        # 判断flag是否是网址
        if flag.startswith(('http://','https://')):
            url = flag
            if len(args) == 1:
                download(url,None,None)
            elif len(args) == 2:
                title_or_url = args[1]
                if title_or_url.startswith(('http://','https://')):
                    download(url,None,title_or_url)
                else:
                    download(url,title_or_url,None)
            elif (len(args) == 3):
                if args[1].startswith(('http://','https://')):
                    print('歌曲名称不合法!')
                    return
                if not args[2].startswith(('http://','https://')):
                    print('封面url不合法!')
                    return
                download(url,args[1],args[2])
            else:
                print('非法参数!')
        else:
            print('请输入合法的网址!')
            return

if  __name__ == '__main__':
    # add_cover('out.mp3','https://yt3.googleusercontent.com/ytc/APkrFKYi81RwDYPJx9n1cZzI3jT3nQv1PmB0QPlNk2Ruhw=s900-c-k-c0x00ffffff-no-rj')
    # add_title('out.mp3','test_title')
    # add_artist('out.mp3','test_artist')
    
    # mp3 = MP3('out.mp3')
    # mp3.add_cover('https://yt3.googleusercontent.com/ytc/APkrFKYi81RwDYPJx9n1cZzI3jT3nQv1PmB0QPlNk2Ruhw=s900-c-k-c0x00ffffff-no-rj')
    # mp3.add_title('test_title')
    # mp3.add_artist('test_artist')
    # mp3.add_album('test_album')
    # mp3.save()
    
    
    # info = extract_info('https://www.youtube.com/watch?v=zq-lIBwhWLk')
    # # 获取缩略图url
    # thumbnail = info['thumbnail']
    # # 获取标题
    # title = info['title']
    
    
    # download('https://youtu.be/xsk1SLmf9a0?si=zj8z06UGwLAKEMOj','Handbook - See The World','https://i2.cdn.turner.com/cnn/2008/WORLD/asiapcf/09/03/ta.jaychou/art.jaychou.jpg')
    # clip('青花瓷-周杰伦.mp3','00:00:00','00:00:30')
    pass
    
    