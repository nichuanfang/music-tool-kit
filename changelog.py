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
lines = changelog.split('\n')[1:]
core.set_output('changelog', '\n'.join(lines))
            
    
    #   #📦 Uncategorized 
    #    - commit message
    