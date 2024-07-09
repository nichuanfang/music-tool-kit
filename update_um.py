import os
import tarfile

import requests

# 音乐解锁软件的版本号 更新地址: https://git.unlock-music.dev/um/-/packages/generic/cli-build 可以先通过访问这个地址 获取响应的Location  从而获取版本号
um_version = '92'

def download_and_extract_um():
	url = f'https://git.unlock-music.dev/api/packages/um/generic/cli-build/{um_version}/um-windows-amd64.tar.gz'
	dest_dir = os.path.join(os.path.dirname(__file__), 'mk', 'bin')
	os.makedirs(dest_dir, exist_ok=True)
	tar_path = os.path.join(dest_dir, 'um-windows-amd64.tar.gz')
	
	# Download the file with User-Agent header
	print(f'Downloading {url}...')
	headers = {'User-Agent': 'Mozilla/5.0'}
	response = requests.get(url, headers=headers)
	if response.status_code == 200:
		with open(tar_path, 'wb') as out_file:
			out_file.write(response.content)
	else:
		raise Exception(f"Failed to download file: {response.status_code} {response.reason}")
	
	# Extract the tar.gz file
	print(f'Extracting {tar_path}...')
	with tarfile.open(tar_path, 'r:gz') as tar:
		tar.extractall(path=dest_dir)
	
	# Clean up
	os.remove(tar_path)
	print('Download and extraction complete.')

if __name__ == '__main__':
	download_and_extract_um()
