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
mk -c 输入的mp3文件 开始时间 结束时间
```

> 时间格式为: 00:00:00

- 提取伴奏

```bash
mk -e 输入的mp3文件 [模型名称]
```

> 支持的模型:

1. UVR_MDXNET_Main (整体较好 默认)
2. UVR-MDX-NET-Inst_Main (整体较好)
3. UVR-MDX-NET-Inst_3 (整体较好)
4. UVR-MDX-NET-Inst_HQ_3 (整体较好)
5. UVR_MDXNET_KARA_2 (一般,人声剔除不干净,声音忽高忽低)
6. Kim_Inst (一般)
