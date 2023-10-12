# !/usr/bin/env python3
import os
import sys
import requests
from  bs4 import BeautifulSoup
from mk.mp3_util import MP3,ID3
from mutagen import File
from yt_dlp import  YoutubeDL
from fake_useragent import UserAgent
import  soundcloud

# 提取yt_dlp信息
def  extract_info(url):
    ydl = YoutubeDL(params={
                'quiet': True,
                'no_color': True,
                'extract_flat': True
            })
    info = ydl.extract_info(url, download=False)
    return info

def download(url:str,title:str=None,cover_url:str=None):
    """下载mp3格式的音乐
    Args:
        url (str): 歌曲网址
        name (str): 歌曲[-歌手]
        cover_url (str, optional): 封面url. Defaults to None.
    """ 
    # 多平台强制删除temp文件夹
    try:
        # 判断文件夹是否存在
        if os.path.exists('temp'):
            if sys.platform == 'win32':
                # 判断文件夹是否存在
                os.system('rmdir /s/q temp')
            else:
                os.system('rm -rf temp')
    except:
        pass
    album = None
    if title != None:
        # 判断是否有专辑
        if title.find('(') != -1 and title.endswith(')') and len(title.split('(')[1].split(')')[0])!=0:
            # 去除专辑格式
            album = title.split('(')[1].split(')')[0]
            title = title.rsplit('(',1)[0]
        outtmpl = f'{title}.%(ext)s'
    else:
        outtmpl = '%(title)s.%(ext)s'
        
    ydl_opts = {
        'quiet': True,
        'no_color': True,
        'format': 'bestaudio/best',
        'outtmpl': outtmpl,
        'paths': {
            'home': 'temp'
        },
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': 0
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = extract_info(url)
        ydl.download([url])
        
    # 解决不规则标题引起的控制台乱码问题
    
    # 获取temp文件夹mp3文件
    mp3s = os.listdir('temp')
    # 获取mp3文件路径
    mp3_path = os.path.join('temp',mp3s[0])
    mp3 = MP3(mp3_path)
    if  title != None:
        if title.find('-') != -1:
            if album!=None:
                mp3.add_album(album)
                song = title.rsplit('-',1)[0].rsplit('(',1)[0]
            else:
                song = title.rsplit('-',1)[0]
                mp3.add_album(title)
            artist = title.split('-')[1]
            # 前后去空串
            mp3.add_title(song.replace('?','').replace('#',''))
            mp3.add_artist(artist)
        else:
            if album!=None:
                mp3.add_album(album)
            else:
                if 'uploader' in info:
                    mp3.add_album(f'{title}-{info["uploader"]}')
                else:
                    mp3.add_album(title+'-Unknown Artist')
            mp3.add_title(title.replace('?','').replace('#',''))
            if 'uploader' in info:
                mp3.add_artist(info['uploader'])
            else:
                mp3.add_artist('Unknown Artist')
        if cover_url != None:
                mp3.add_cover(cover_url)
        else:
            if  'thumbnail' in info:
                thumbnail = info['thumbnail']
                mp3.add_cover(thumbnail)
        mp3.save()
    else:
        title = info['title']
        mp3.add_title(title)
        if 'uploader' in info:
            mp3.add_artist(info['uploader'])
            mp3.add_album(title+'-'+info['uploader'])
        else:
            mp3.add_album(title+'-Unknown Artist')
            mp3.add_artist('Unknown Artist')
        if  cover_url != None:
            mp3.add_cover(cover_url)
        else:
            if  'thumbnail' in info:
                thumbnail = info['thumbnail']    
                mp3.add_cover(thumbnail)
        mp3.save()
    
    print('下载完成!')
    # 多平台将temp文件夹下的文件移动到当前目录
    if sys.platform == 'win32':
        os.system(f'move temp\\*.* .')
    else:
        os.system(f'mv temp/* .')
    
    # 多平台删除temp文件夹
    if sys.platform == 'win32':
        os.system('rmdir /s/q temp')
    else:
        os.system('rm -rf temp')
    
    
def clip(path:str,start:str,end:str):
    """剪辑音乐

    Args:
        path (str): 歌曲文件路径
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
        mp3.add_bytes_cover(img_data)
        mp3.save()
    print('剪辑完成!')
    
# 从youtube搜索歌曲
def search_youtube(name:str):
    """搜索歌曲

    Args:
        name (str): 歌曲名称
    """ 
    res = []
    # 从油管获取结果
    ydl_opts = {
        'quiet': True,
        'no_color': True,
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'paths': {
            'home': 'temp'
        },
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': 0
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        # 搜索3条结果
        info = ydl.extract_info(f'ytsearch3:{name}', download=False)
        for i in range(3):
            title = info['entries'][i]['title']
            url = info['entries'][i]['webpage_url']
            res.append({
                'title': title,
                'url': url
            })
    return res

# 从bilibili搜索歌曲
def search_bilibili(name:str):
    """搜索歌曲

    Args:
        name (str): 歌曲名称
    """ 
    res = []
    ua = UserAgent()
    # 从bilibili获取搜索结果
    url = f'https://search.bilibili.com/all?keyword={name}&page=1'
    headers = {
        'User-Agent':ua.chrome,
        'Referer':'https://www.bilibili.com/'
    }
    
    response = requests.get(url,headers=headers)
    html = response.text
    soup = BeautifulSoup(html,'lxml')
    # 获取搜索结果
    items = soup.find_all('div',class_='video-list row')[0].contents
    for item in items[:4]:
        if item == '[' or item == ']':
            continue
        title = item.contents[0].contents[1].contents[1].contents[2].contents[0].text
        url = item.contents[0].contents[1].contents[0].attrs['href']
        res.append({
            'title': title,
            'url': f'https:{url}'
        })
    return res

# 搜索soundcloud歌曲
def search_soundcloud(name:str):
    """搜索歌曲

    Args:
        name (str): 歌曲名称
    """ 
    res = []
    client = soundcloud.Client(client_id  = 'Qiipt0EkEtDliaaQ2zktLdLcA2cYr8YL')
    tracks = client.get('/tracks',q=name,limit=4)
    for track in tracks:
        res.append({
            'title': track.title,
            'url': track.permalink_url
        })
    return res


# 搜索歌曲
def search(name:str):
    """搜索歌曲

    Args:
        name (str): 歌曲名称
    """ 
    res = []
    # 从油管获取结果
    res.extend(search_youtube(name))
    # 从bilibili获取结果
    res.extend(search_bilibili(name))
    # 从soundcloud获取结果  由于近期soundcloud关闭了api接口,所以暂时不支持
    # res.extend(search_soundcloud(name))
    return res

def main(args=None):
    if args == None:
        args = sys.argv[1:]
    # 校验args
    if len(args) == 0:
        print('configuration:\n\n'
            '---------------------------------------------\n'+
            '下载: mk url [title] [cover_url]\n'+
            '搜索: mk -s name\n'
            '剪辑: mk -c path start end\n'
            '---------------------------------------------\n' 
            )
        return
    flag = args[0]
    if flag == '-c':
        path = args[1]
        start = args[2]
        end = args[3]
        clip(path,start,end)
    elif flag == '-s':
        name = args[1]
        res = search(name)
        for i in range(len(res)):
            print(f'{i+1}. {res[i]["title"]}')
            print(f'    {res[i]["url"]}')
        num = int(input('请输入序号:'))
        if num>len(res) or num<=0:
            print('序号不合法!')
            return
        # 输入标题
        title = input('请输入标题:')
        if title == '':
            title = None
        print('正在下载...')
        download(res[num-1]['url'],res[num-1]['title'],title)
        print('下载完成!')
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
    
    # https://soundcloud.com/jeff-kaale/my-heart'
    # download('https://www.bilibili.com/video/BV1yR4y1L7KN/?spm_id_from=333.1007.top_right_bar_window_default_collection.content.click')
    # clip('青花瓷-周杰伦.mp3','00:00:00','00:00:30')
    pass
    
    