# music-tool-kit 音乐工具箱

## 安装

```bash
pip install -U music-tool-kit
```

> Tips:

1. python 版本: 3.11.0 及以上
2. 需安装 ffmpeg

## 使用

- 音乐下载

```bash
mk  网址 [输出] [封面url]
```

> 输出格式为 歌曲名-歌手(专辑名) 输出歌曲格式为 mp3 可选, 封面 url 也可选

- 音乐搜索

```bash
mk -s 关键字
```

> 支持 youtube bilibili soundcloud ,输出优先级 youtube > bilibili > soundcloud

- 音乐剪辑

```bash
mk -c 输入的文件 开始时间 结束时间
```

> 时间格式为: 00:00:00
