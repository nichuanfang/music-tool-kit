# -*- coding: utf-8 -*-
# !/usr/bin/env python3
import requests
import os
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB,ID3NoHeaderError
from PIL import Image

# webp转jpg
def  webp2jpg(webp_path,jpg_path):
    im = Image.open(webp_path).convert('RGB')
    im.save(jpg_path, 'jpeg')
    # 删除webp文件
    os.remove(webp_path)
    # 返回jpg文件字节码
    with open(jpg_path,'rb') as f:
        return f.read()

class MP3:
    
    def __init__(self,mp3path:str) -> None:
        """mp3对象

        Args:
            mp3path (str): mp3文件路径
        """        
        try:
            self.mp3path = mp3path.replace('?','')
            self.songFile = ID3(mp3path)
        except ID3NoHeaderError:
            self.songFile = ID3()
            # 获取mp3文件名
            self.songFile.filename = mp3path.replace('\\','/').rsplit('/',1)[1]
        except Exception as e:
            print(e)
            return
    
    # 给mp3文件添加封面
    def add_cover(self,cover_url):
        mp3_name = self.mp3path.replace('\\','/').split('.')[0].rsplit('/',1)[1]
        cover_extension = cover_url.split('.')[-1]
        
        response = requests.get(cover_url)
        if response.status_code != 200:
            print('封面url不合法!')
            return
        image_data = response.content
        if cover_extension == 'webp':
            with open(f'{mp3_name}.{cover_extension}','wb') as f:
                f.write(response.content)
            image_data = webp2jpg(f'{mp3_name}.{cover_extension}',f'{mp3_name}.jpg')
            os.remove(f'{mp3_name}.jpg')
        
        # 插入封面
        self.songFile['APIC'] = APIC(  
            encoding=0,
            mime='image/jpg',
            type=3,
            desc=u'Cover',
            data=image_data
        )
        print(f'封面{cover_url}添加完成')
        
    # 给mp3文件添加封面
    def add_bytes_cover(self,image_data:bytes):
        # 插入封面
        self.songFile['APIC'] = APIC(  
            encoding=0,
            mime='image/jpg',
            type=3,
            desc=u'Cover',
            data=image_data
        )

    # 给mp3文件添加歌名
    def add_title(self,title):
        # 插入歌名
        self.songFile['TIT2'] = TIT2(  
            encoding=3,
            text=title
        )
        print(f'歌名{title}添加完成')
        
    # 给mp3文件添加歌手
    def add_artist(self,artist):
        # 插入歌手
        self.songFile['TPE1'] = TPE1(  
            encoding=3,
            text=artist
        )
        print(f'歌手{artist}添加完成')
        
    # 给mp3文件添加专辑
    def add_album(self,album):
        print(f'开始添加专辑{album}')
        # 插入专辑
        self.songFile['TALB'] = TALB(  
            encoding=3,
            text=album
        )
        print(f'专辑{album}添加完成')
    
    def save(self):
        # 保存
        self.songFile.save(self.mp3path.replace('\\','/'))
        print('保存完成')
        