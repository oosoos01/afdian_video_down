# 爱发电视频下载
**前排提醒：本工具仅能下载正在发电的节目，只能下载MP4格式的视频**
### 获取 album_id  
节目的url应为：`https://afdian.net/album/ALBUM_ID`, 注意是节目的url, 不是创作者的。 
### 获取 auth_token  
获取cookie中的 `auth_token`
填到代码里面
### 下载全部
```shell
python main.py --id ALBUM_ID --all
```
### 下载最新n期
```shell
# 列出最新n期
python main.py --id ALBUM_ID --latest n --list
# 下载
python main.py --id ALBUM_ID --latest n
```
