# music-tool-kit 音乐工具箱

music-tool-kit，主要使用场景为提取[youtube](https://www.youtube.com)和[bilibili](https://www.bilibili.com)视频中的音频,支持**音频下载**,**元信息自动补全**,**音频截取**,**提取伴奏**,**youtube 列表批量下载**,**自定义批量下载**等.

> **Note**
>
> 本项目仅为个人使用,无任何商业用途,仅支持 mp3 格式的音乐

- [music-tool-kit 音乐工具箱](#music-tool-kit-音乐工具箱)
  - [环境准备](#环境准备)
    - [安装](#安装)
    - [升级](#升级)
    - [卸载](#卸载)
  - [使用](#使用)
    - [音乐下载](#音乐下载)
    - [音乐搜索](#音乐搜索)
    - [音乐剪辑](#音乐剪辑)
    - [提取伴奏](#提取伴奏)
    - [生成批量下载 csv 模板文件](#生成批量下载-csv-模板文件)
    - [批量下载](#批量下载)
  - [License](#license)

## 环境准备

### 安装

```bash
pip install -U music-tool-kit
```

![help](https://raw.githubusercontent.com/nichuanfang/music-tool-kit/main/example/help.png)

> Tips: python 版本: 3.11.0 及以上,需安装 ffmpeg

### 升级

```bash
pip install -U music-tool-kit
```

### 卸载

```bash
pip uninstall music-tool-kit
```

## 使用

### 音乐下载

```bash
mk  "网址" [输出] "[封面url]"

```

普通下载
![download](https://raw.githubusercontent.com/nichuanfang/music-tool-kit/main/example/download.png)

列表下载
![download_list](https://raw.githubusercontent.com/nichuanfang/music-tool-kit/main/example/batch_download.png)

- 输出格式为 **歌曲名-歌手(专辑名)** 输出歌曲格式为 **mp3**

- 列表下载使用方法为 `mk "列表url | 列表序号"` ,**url 需要为 [youtube](https://www.youtube.com) 的列表格式**,如果想下载全部歌曲,直接输入 `mk "列表url |"` 即可!

  ```bash
    mk "https://www.youtube.com/playlist?list=PL8B3F8A7B0A9F4DE8 | 1,2,3,4,5"
  ```

  > **Note**
  >
  > 仅支持下载 youtube 的列表下载,url|后面的列表序号之间需要用逗号分隔

### 音乐搜索

```bash
mk -s "关键字"
```

![search](https://raw.githubusercontent.com/nichuanfang/music-tool-kit/main/example/search.png)
支持 youtube bilibili 输出优先级 youtube > bilibili

### 音乐剪辑

```bash
mk -c "输入的mp3文件" 开始时间 结束时间
```

![clip](https://raw.githubusercontent.com/nichuanfang/music-tool-kit/main/example/clip.png)

> Tips: 时间格式为 `00:00:00`

### 提取伴奏

```bash
mk -e "输入的mp3文件" [模型名称]
```

支持的模型:

- `UVR_MDXNET_Main` (整体较好)
- `UVR-MDX-NET-Inst_Main` (整体较好)
- `UVR-MDX-NET-Inst_3` (整体较好)
- `UVR-MDX-NET-Inst_HQ_3` (整体较好)
- `UVR_MDXNET_KARA_2` (一般,人声剔除不干净,声音忽高忽低)
- `Kim_Inst` (一般)

![extract](https://raw.githubusercontent.com/nichuanfang/music-tool-kit/main/example/inst.png)

> **Note**
>
> 默认模型为`UVR_MDXNET_Main`,具体请结合音乐类型和自己的实际听感自行调整模型;伴奏提取比较吃 cpu 性能,时间比较漫长,请耐心等待,大概需要 5~10 分钟

### 生成批量下载 csv 模板文件

```bash
mk -t
```

生成的模板文件如下:
![csv_template](https://raw.githubusercontent.com/nichuanfang/music-tool-kit/main/example/csv_template.png)
用户自行填写下载信息,保存后使用`mk "csv文件"`即可批量下载

| url  | title | cover_url | start_time | end_time | instrumental |
| ---- | ----- | --------- | ---------- | -------- | ------------ |
| 网址 | 标题  | 封面 url  | 开始时间   | 结束时间 | 是否生成伴奏 |

### 批量下载

```bash
mk "csv文件"
```

![csv_download](https://raw.githubusercontent.com/nichuanfang/music-tool-kit/main/example/csv_download.png)

> Tips: 格式为 `下载 url,标题,封面 url,截取开始时间,截取终止时间,是否生成伴奏(true 或 false)`

## License

This work is released under the MIT license. A copy of the license is provided in the [LICENSE](https://raw.githubusercontent.com/nichuanfang/music-tool-kit/main/LICENSE) file.
