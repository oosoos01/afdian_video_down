import argparse
import os
from random import randint
from time import sleep

import eyed3
import requests

SLEEP_TIME = 30

cookies = {}

#填写auth_token
os.environ["auth_token"] = "填写自己cookie里的auth_token"

headers = {
    'authority': 'afdian.net',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://afdian.net/album/c6ae1166a9f511eab22c52540025c377',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
}


def download_page(data, list: bool, n: int=-1):
    albums = data["list"]
    for album in albums:
        # 下载n期
        if not n == -1:
            if n > 0:
                n -= 1
            elif n == 0:
                break
        title = album["title"]
        author = album["user"]["name"]
        description = album["content"]
        cover_url = album["video_thumb"]
        audio_url: str = album["video"]
        # 是否仅列出
        if list:
            print(title)
            print(description.replace("\n\n", "\n")) # 去除多余空行
            print("="*40)
        else:
            filename = f"{title}.mp4"
            filename2 = f"{title}.jpg"
            print(f"正在处理：{title}")
            if audio_url.strip() == "":
                print("本条动态没有视频文件，跳过")
                continue
            cover = None
            try:
                cover = requests.get(cover_url).content
                with open(filename2, "wb+") as file:
                    file.write(cover)
                print(f"封面下载完毕")
            except Exception as e:
                print(f"封面下载失败：{cover_url}")
                print(e)
            try:
                if not os.path.exists(filename):
                    # 没有下载过
                    source_file = requests.get(audio_url, headers=headers, cookies=cookies).content
                    with open(filename, "wb+") as file:
                        file.write(source_file)
                    print(f"{filename} 下载完成")
               #audio: eyed3.core.AudioFile = eyed3.load(filename)

            except Exception as e:
                print("下载歌曲失败")
                print(e)
            sleep(SLEEP_TIME + randint(0, 5))


def get_all_albums(album_id: str, list: bool):
    params = {
        'album_id': album_id,
        'lastRank': 0,
        'rankOrder': 'asc',
        'rankField': 'rank',
    }
    while True:
        resp = requests.get('https://afdian.net/api/user/get-album-post', headers=headers, params=params,
                            cookies=cookies).json()
        data = resp["data"]
        download_page(data, list, -1)
        params["lastRank"] += 10
        if list:
            sleep(randint(2, 5))
        else:
            sleep(SLEEP_TIME + randint(0, 5))
        if data["has_more"] == 0:
            # 遍历完毕
            break


# 获取倒数第n期节目
def get_latest_n(album_id: str, list: bool, n:int = 0):
    params = {
        'album_id': album_id,
        'lastRank': 0,
        'rankOrder': 'desc',
        'rankField': 'publish_sn',
    }
    resp = requests.get('https://afdian.net/api/user/get-album-post', headers=headers, params=params,
                        cookies=cookies).json()
    data = resp["data"]
    download_page(data, list, n)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="爱发电播客下载")
    parser.add_argument("--id", required=True, type=str, help="URL里的id")
    parser.add_argument("--list", action="store_true", help="仅列出，不下载")
    parser.add_argument("--all", action="store_true", help="下载全部")
    parser.add_argument("--latest", metavar="n", type=int, default=1, help="下载最新n期")
    args = parser.parse_args()
    if "auth_token" in os.environ:
        cookies["auth_token"] = os.environ["auth_token"]
    else:
        print("auth_token未配置")
        exit(1)
    if args.all:
        get_all_albums(args.id, args.list)
    if args.latest:
        get_latest_n(args.id, args.list, args.latest)