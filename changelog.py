import sys
from actions_toolkit import core
CATEGORIES = [
    {
            "title": "## 🚀 Features",
            "labels": [
                "feat"
            ]
        },
        {
            "title": "## 🐛 Fixes",
            "labels": [
                "fix"
            ]
        },
        {
            "title": "## 📝 Documentation",
            "labels": [
                "docs"
            ]
        },
        {
            "title": "## 🎨 Style",
            "labels": [
                "style"
            ]
        },
        {
            "title": "## 🧰 Refactor",
            "labels": [
                "refactor"
            ]
        },
        {
            "title": "## 🚨 Perf",
            "labels": [
                "perf"
            ]
        },
        {
            "title": "## 🧪 Tests",
            "labels": [
                "test"
            ]
        },
        {
            "title": "## 📦 Build",
            "labels": [
                "build"
            ]
        },
        {
            "title": "## 📦 CI",
            "labels": [
                "ci"
            ]
        },
        {
            "title": "## 📦 Chore",
            "labels": [
                "chore"
            ]
        }
]
# 获取第一个参数
if len(sys.argv) > 1:
    changelog = sys.argv[1]
else:
    raise Exception('changelog path is required')

# 读取changelog
with open(changelog, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    # 去除第一行
    if len(lines)<2:
        raise Exception('changelog is empty')
    lines = lines[1:]
    # 写入文件
    # with open(changelog, 'w', encoding='utf-8') as f:
    #     for line in lines:
    #         f.write(line)
            # 设置输出
    # lines转字符串
    core.set_output('changelog', '\n'.join(lines))
            
    
    #   #📦 Uncategorized 
    #    - commit message
    