import requests
import re

# 获取当前 requirements.txt 中的 yt-dlp 版本


def get_current_ytdlp_version():
    with open('requirements.txt', 'r') as file:
        for line in file:
            if line.startswith('yt-dlp'):
                current_version = re.search(r'==(.+)', line).group(1)
                return current_version.strip()


def get_latest_ytdlp_version():
    # 获取最新的 yt-dlp 版本
    url = 'https://pypi.org/pypi/yt-dlp/json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        latest_version = data['info']['version']
        return latest_version
    return None

# 更新 requirements.txt 文件中的 yt-dlp 版本


def update_requirements_file(new_version):
    with open('requirements.txt', 'r') as file:
        lines = file.readlines()
    with open('requirements.txt', 'w') as file:
        for line in lines:
            if line.startswith('yt-dlp'):
                file.write(f'yt-dlp=={new_version}\n')
            else:
                file.write(line)

# 主逻辑


def main():
    current_version = get_current_ytdlp_version()
    latest_version = get_latest_ytdlp_version()

    if current_version and latest_version and current_version != latest_version:
        update_requirements_file(latest_version)
        print(
            f'Updated yt-dlp from {current_version} to {latest_version} in requirements.txt')

        # 使用 Git 提交更改
        commit_message = f'Update yt-dlp to version {latest_version}'
        commit_command = f'git commit -am "{commit_message}"'
        push_command = 'git push origin main'

        import subprocess
        subprocess.run(commit_command, shell=True)
        subprocess.run(push_command, shell=True)
    else:
        print('No update needed or failed to fetch version info.')


if __name__ == '__main__':
    main()
