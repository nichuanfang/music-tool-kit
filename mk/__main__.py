# !/usr/bin/env python3
import asyncio
import csv
import os
import sys

from bilibili_api import search as bilibili_search
from mutagen.mp4 import MP4
from rich import print
from rich.console import Console
from yt_dlp import YoutubeDL

# 支持的模型列表
# SUPPORT_MODELS = [
# 	'UVR_MDXNET_Main',
# 	'UVR-MDX-NET-Inst_Main',
# 	'UVR-MDX-NET-Inst_3',
# 	'UVR-MDX-NET-Inst_HQ_3',
# 	'UVR_MDXNET_KARA_2',
# 	'Kim_Inst'
# ]

console = Console()


# 提取yt_dlp信息
def extract_info(url):
	console.log(f"开始解析{url}...")
	ydl = YoutubeDL(params={
		'quiet': True,
		'no_color': True,
		'extract_flat': True
	})
	info = ydl.extract_info(url, download=False)
	if info == None:
		console.log(f"{url}解析失败 请检查网址是否正确!")
		return None
	console.log(f"{url}解析成功!")
	return info


def download(url: str, title: str = None):
	"""下载aac格式的音乐
    Args:
        url (str): 歌曲网址
        title (str): 标题
    """
	info = extract_info(url)
	if info == None:
		return
	try:
		url = info['url']
	except:
		try:
			url = info['webpage_url']
		except:
			print('获取下载地址失败!')
			return
	try:
		download_title = info['title']
	except:
		print('获取标题失败!')
		return
	with console.status(f"[bold green]正在下载{download_title}...\n") as status:
		if title != None:
			outtmpl = title.strip().replace('/', '').replace('\\', '').replace('⧸', ' ').replace('⧹', ' ').replace(
				'|', ' ').replace('?', ' ').replace('*', ' ')
		else:
			outtmpl = download_title
		
		ydl_opts = {
			'quiet': True,
			'no_color': True,
			'format': 'bestaudio/best',
			'outtmpl': outtmpl,
			'nocheckcertificate': True,
			'writethumbnail': True,
			'postprocessors': [
				{
					'key': 'FFmpegExtractAudio',
					'preferredcodec': 'aac',
					'preferredquality': 0
				},
				{
					'key': 'FFmpegMetadata',
					'add_metadata': True,
				},
				{
					'key': 'EmbedThumbnail',
					'already_have_thumbnail': False
				}
			]
		}
		with YoutubeDL(ydl_opts) as ydl:
			ydl.download([url])
		
		# 更改专辑名称为上级目录名称
		# 获取上级目录名称
		album = os.path.basename(os.getcwd())
		
		audio = MP4(f'{outtmpl}.m4a')
		audio['\xa9alb'] = album  # 专辑
		audio.save()
		
		# 解决不规则标题引起的控制台乱码问题
		console.log(f"下载完成!")
		return info


def batch_download(csv_path: str):
	"""批量下载

    Args:
        csv_path (str): _description_
    """
	with open(csv_path, 'r', encoding='utf-8') as f:
		reader = csv.reader(f)
		# 去除第一行
		skiped = True
		# writer.writerow(['url', 'title', 'start_time', 'end_time'])
		for row in reader:
			if skiped:
				skiped = False
				continue
			try:
				url = row[0]
			except:
				continue
			try:
				title = row[1] if row[1].strip() != '' else None
			except:
				title = None
			try:
				start_time = row[2] if row[2].strip() != '' else None
			except:
				start_time = None
			try:
				end_time = row[3] if row[3].strip() != '' else None
			except:
				end_time = None
			# 下载
			if url.__contains__('youtube.com') and url.find('list=') != -1 and url.find('v=') != -1:
				url = url.split('&')[0]
			info = download(url, title)
			# 剪辑
			if title != None:
				title = title.strip().replace('/', '').replace('\\', '').replace('⧸', ' ').replace('⧹', ' ').replace(
					'|', ' ').replace('?', ' ').replace('*', ' ')
			else:
				title = info['title']
			if start_time != None and end_time != None:
				clip(f'{title}.m4a', start_time, end_time)


# if instrumental == 'true' or instrumental == 'True':
# 	# 提取伴奏
# 	extract_accompaniment(f'{title}.m4a')


def clip(path: str, start: str, end: str):
	"""剪辑音乐

    Args:
        path (str): 歌曲文件路径
        start (str): 开始时间(格式 00:00:00)
        end (str): 结束时间(格式 00:00:00)
    """
	with console.status("[bold green]正在剪辑...\n") as status:
		try:
			command = f'ffmpeg -i "{path}" -ss {start} -to {end} -c copy -map_metadata 0 -map 0  -y output.m4a'
		except:
			print('请先安装ffmpeg!')
			return
		# 执行命令
		os.system(command)
		# 删除原文件
		os.remove(path)
		# 重命名
		os.rename('output.m4a', path)
		console.log(f"剪辑完成!")


# 获取两个字符串相似度
# def get_similarity(s1: str, s2: str):
# 	"""获取两个字符串相似度
#
#     Args:
#         s1 (str): 字符串1
#         s2 (str): 字符串2
#
#     Returns:
#         float: 相似度
#     """
# 	return difflib.SequenceMatcher(lambda x: x in ["【", "】", "(", ")", "-", "_", ".", "[", "]", "|"], s1.lower(),
# 	                               s2.lower()).ratio()


# 从youtube搜索歌曲
async def search_youtube(name: str):
	"""搜索歌曲

    Args:
        name (str): 歌曲名称
    """
	res = []
	# 从油管获取结果
	ydl_opts = {
		'quiet': True,
		'no_color': True,
		'no_warnings': True,
		'ignoreerrors': True,
	}
	with YoutubeDL(ydl_opts) as ydl:
		# 搜索10条结果
		info = ydl.extract_info(f'ytsearch10:{name}', download=False)
		for i in range(10):
			try:
				if info['entries'][i] != None:
					title = info['entries'][i]['title']
					url = info['entries'][i]['webpage_url']
					res.append({
						'title': title,
						'url': url
					})
			except:
				break
	# 根据相似度get_similarity重新排序res
	# for i in range(len(res)):
	#     res[i]['similarity'] = get_similarity(name,res[i]['title'])
	
	# res.sort(key=lambda x:x['similarity'],reverse=True)
	# # 最多只取5条数据
	# if len(res)>5:
	#     res = res[:5]
	
	return res


async def search_bilibili(name: str):
	search = await bilibili_search.search_by_type(name, search_type=bilibili_search.SearchObjectType.VIDEO, page=1)
	result = search['result']
	res = []
	for i in range(len(result)):
		if i == 10:
			break
		# 去除<em class="keyword"></em>正则匹配格式
		title = result[i]['title'].replace('<em class="keyword">', '').replace('</em>', '').replace('&#39;', '\'')
		res.append({
			'title': title,
			'url': result[i]['arcurl']
		})
	# 根据相似度get_similarity重新排序res
	# for i in range(len(res)):
	#     res[i]['similarity'] = get_similarity(name,res[i]['title'])
	
	# res.sort(key=lambda x:x['similarity'],reverse=True)
	
	# # 最多只取5条数据
	# if len(res)>5:
	#     res = res[:5]
	return res


# 搜索歌曲
async def search(name: str):
	"""搜索歌曲

    Args:
        name (str): 歌曲名称
    """
	with console.status("[bold green]搜索中...") as status:
		name = name.replace('⧸', '/').replace('⧹', '/').replace('⧺', '+').replace('⧻', '+').replace('⧼', '<').replace(
			'⧽', '>').replace('⧾', '>').replace('⧿', '>')
		tasks = [
			asyncio.create_task(search_youtube(name)),
			asyncio.create_task(search_bilibili(name))]
		# 如果出现异常 返回正常的结果 打印异常信息
		results = await asyncio.gather(*tasks, return_exceptions=True)
		if isinstance(results[0], Exception):
			return results[1]
		elif isinstance(results[1], Exception):
			return results[0]
		elif isinstance(results[0], Exception) and isinstance(results[1], Exception):
			return []
		else:
			return results[0] + results[1]


# 提取伴奏
# def extract_accompaniment(audiopath: str, model_name: str = None):
# 	if not audiopath.endswith('.m4a'):
# 		print('仅支持aac文件!')
# 		return
# 	with console.status("[bold green]提取伴奏中...") as status:
# 		try:
# 			if model_name == None:
# 				command = f'audio-separator --model_name="UVR_MDXNET_Main" --denoise=True --output_format=M4A --single_stem=instrumental "{audiopath}"'
# 			elif model_name in SUPPORT_MODELS:
# 				command = f'audio-separator --model_name={model_name} --denoise=True --output_format=M4A --single_stem=instrumental "{audiopath}"'
# 			else:
# 				print('不支持的模型!')
# 				return
# 		except:
# 			print('请先安装audio-separator!')
# 			return
# 		# 执行命令
# 		os.system(command)
# 		sync_meta()
# 		console.log(f"提取完成!")


# 同步伴奏元信息
# def sync_meta():
# 	# 遍历当前目录
# 	for file in os.listdir('.'):
# 		# 判断是否是mp3文件
# 		if file.endswith('.mp3') and file.__contains__('_(Instrumental)_'):
# 			try:
# 				# 如果标题存在 说明标签已同步 无需处理
# 				MP3(file).songFile['TIT2'].text[0]
# 			except:
# 				# 获取原文件名 使用UVR软件处理过的音频伴奏命名格式为  `标题_(Instrumental)_UVR模型``
# 				try:
# 					raw_name = file.split('_')[0]
# 					if raw_name == None or raw_name == '':
# 						continue
# 					# 判断文件raw_name.mp3是否存在
# 					if os.path.exists(f'{raw_name}.mp3'):
# 						source_mp3 = MP3(f'{raw_name}.mp3')
# 						# 获取source_mp3的比特率
# 						raw_bitrate = mutagen_mp3(f'{raw_name}.mp3').info.bitrate
# 						# 使用ffmpeg同步目标文件的比特率
# 						try:
# 							os.system(
# 								f'ffmpeg  -y -i "{file}" -acodec libmp3lame -ab  {int(raw_bitrate / 1000)}k -ar 48000  "{raw_name}_output.mp3"')
# 						except:
# 							print('请先安装ffmpeg!')
# 							return
# 						dest_mp3 = MP3(f'{raw_name}_output.mp3')
# 						# 将source_mp3的元信息同步到dest_mp3
# 						dest_mp3.add_title(source_mp3.songFile['TIT2'].text[0] + '(instrumental)')
# 						dest_mp3.add_artist(source_mp3.songFile['TPE1'].text[0])
# 						dest_mp3.add_album(source_mp3.songFile['TALB'].text[0])
# 						dest_mp3.add_bytes_cover(source_mp3.songFile['APIC:Cover'].data)
# 						dest_mp3.save()
# 						# output文件重命名
# 						os.rename(f'{raw_name}_output.mp3', f'{raw_name}(instrumental).mp3')
# 						# 删除目标文件
# 						os.remove(file)
#
# 				except Exception as e:
# 					print(e)
# 					continue


def main(args=None):
	if args == None:
		args = sys.argv[1:]
	# 校验args
	if len(args) == 0:
		# '提取伴奏: mk -e audio_path \[model_name]\n'
		print('configuration:\n\n'
		      '---------------------------------------------\n' +
		      '下载: mk url \[title] \n' +
		      '生成批量模板: mk -t\n'
		      '批量下载: mk csv_path\n'
		      '搜索: mk -s name\n'
		      '剪辑: mk -c audio_path start end\n'
		      '---------------------------------------------\n'
		      )
		return
	flag = args[0]
	if flag == '-c':
		path = args[1]
		start = args[2]
		end = args[3]
		clip(path, start, end)
	elif flag == '-s':
		name = args[1]
		loop = asyncio.get_event_loop()
		res: list = loop.run_until_complete(search(name))
		if len(res) == 0:
			print('未搜索到结果!')
			return
		# 打印搜索结果
		for i in range(len(res)):
			print(f'{i + 1}. {res[i]["title"]}')
			print(f'    {res[i]["url"]}')
		print('')
		exit_status = False
		while True:
			num_str = input('请输入序号:')
			if num_str == None or num_str == '':
				exit_status = True
				break
			try:
				num = int(num_str)
			except:
				print('序号必须为数字!')
				continue
			if num > len(res) or num <= 0:
				print('序号不合法!')
				continue
			break
		if exit_status:
			return
		title = input('请输入标题:')
		if title == '':
			title = None
		download(res[num - 1]['url'], title)
	# elif flag == '-e':
	# 	try:
	# 		path = args[1]
	# 	except:
	# 		print('请输入mp3文件路径!')
	# 		return
	# 	try:
	# 		model_name = args[2]
	# 	except:
	# 		model_name = None
	# 	extract_accompaniment(path, model_name)
	elif flag == '-t':
		# 生成批量模板
		with open('template.csv', 'w', encoding='utf-8', newline='') as f:
			writer = csv.writer(f)
			# 写入表头
			
			# 下载地址 标题  开始时间 结束时间 是否生成伴奏(true or false)
			writer.writerow(['url', 'title', 'start_time', 'end_time'])
		print('生成成功!')
	else:
		# 判断flag是否是网址
		if flag.startswith(('http://', 'https://')):
			url = flag
			# 如果url后面跟着|,  且本身就是一个播放列表 则批量下载 根据|后面的列表序号来筛选 (只对youtube音源有效) 序号之间用,分隔
			if url.__contains__('youtube.com') and url.find('|') != -1 and url.find('list=') != -1:
				raw_url = url.split('|')[0]
				info = extract_info(raw_url)
				try:
					list_url = info['url'] if info['url'] != None else info['webpage_url']
				except:
					try:
						list_url = info['webpage_url']
					except:
						print('获取列表地址失败!')
						return
				
				if raw_url.__contains__('v='):
					info = extract_info(list_url)
				# 获取entries
				entries = info['entries']
				if len(entries) == 0:
					print('列表为空!')
					return
				indexs = url.split('|')[1].split(',')
				if len(indexs) == 1 and indexs[0] == '':
					# 下载全部
					for entry in entries:
						try:
							url = entry['url']
						except:
							try:
								url = entry['webpage_url']
							except:
								print('获取下载地址失败!')
								continue
						download(url)
						return
				for index in indexs:
					try:
						index = int(index.strip())
						if index > len(entries) or index <= 0:
							print('序号不合法!')
							continue
						entry = entries[index - 1]
						# 下载
						try:
							url = entry['url']
						except:
							try:
								url = entry['webpage_url']
							except:
								print('获取下载地址失败!')
								continue
						download(url)
					except Exception as e:
						continue
			else:
				# 不下载列表 去掉列表后缀
				if url.__contains__('youtube.com') and url.find('list=') != -1 and url.find('v=') != -1:
					url = url.split('&')[0]
				if len(args) == 1:
					download(url, None)
				elif len(args) == 2:
					title = args[1]
					download(url, title)
				else:
					print('非法参数!')
		elif flag.endswith('.csv'):
			# 批量下载
			# 判断csv文件是否存在
			if not os.path.exists(flag):
				print('csv文件不存在!')
				return
			batch_download(flag)
		else:
			print('请输入合法的网址!')
			return


if __name__ == '__main__':
	# add_cover('out.mp3','https://yt3.googleusercontent.com/ytc/APkrFKYi81RwDYPJx9n1cZzI3jT3nQv1PmB0QPlNk2Ruhw=s900-c-k-c0x00ffffff-no-rj')
	# add_title('out.mp3','test_title')
	# add_artist('out.mp3','test_artist')
	
	# mp3 = MP3('out.mp3')
	# mp3.add_cover('https://yt3.googleusercontent.com/ytc/APkrFKYi81RwDYPJx9n1cZzI3jT3nQv1PmB0QPlNk2Ruhw=s900-c-k-c0x00ffffff-no-rj')
	# mp3.add_title('test_title')
	# mp3.add_artist('test_artist')
	# mp3.add_album('test_album')
	# mp3.save()
	
	
	# info = extract_info('https://www.youtube.com/playlist?list=PLXqdiA7ZTh9WEXkz9Oimedlm3JRiDJ_hO')
	# # 获取缩略图url
	# thumbnail = info['thumbnail']
	# # 获取标题
	# title = info['title']
	
	# https://soundcloud.com/jeff-kaale/my-heart'
	# download('https://youtu.be/2FswQIz19XE?si=G41BIw8Wp3Hv3fiB')
	# 测试伴奏提取
	# extract_accompaniment('Damien Jurado - Ohio (Filous Remix).m4a')
	
	# clip('Damien Jurado - Ohio (Filous Remix).m4a','00:00:00','00:00:30')
	# loop = asyncio.get_event_loop()
	# a=  loop.run_until_complete(search_youtube("卡农"))
	# 转换为秒
	# 调用异步函数search_bilibili_
	# res = asyncio.run(search_bilibili("a lover's Concerto"))
	# 获取执行的结果
	# sync_meta()
	# download('https://www.youtube.com/watch?v=YudHcBIxlYw&list=RDYudHcBIxlYw&start_radio=1')
	# clip('グーラ領⧸森林.mp3','00:00:00','00:00:30')
	# batch_download('test.csv')
	# info = extract_info('https://www.youtube.com/playlist?list=PL68LFSU9iLnC3YSNDqfy3x-1uF8czx33c')
	# print(info)
	pass
