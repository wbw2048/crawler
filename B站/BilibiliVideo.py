import os
import reprlib
import requests
from B站.utils import user_manager, av2bv, bv2av, validate_title
from tqdm import tqdm
class BilibiliVideo:
    def __init__(
            self,
            bvid: str = "",
            aid: int = 0,
            epid: str = "",
            season_id: str = "",
            quality=80,
            view_online_watch=True,
            audio_quality=30280,
            bangumi=False,
            source="backup"
    ):
        if not any([bvid, aid, epid, season_id]):
            raise Exception("Video id can't be null.")
        self.bvid = bvid if bvid else av2bv(aid)
        self.aid = aid if aid else bv2av(bvid)
        self.epid = epid
        self.season_id = season_id
        self.bangumi = bangumi
        self.quality = quality
        self.audio_quality = audio_quality
        self.view_online_watch = view_online_watch
        self.author_mid = self.get_author_mid()
        self.source = source
        self.see_message = False
    def get_author_mid(self):
        return user_manager.get(
            "https://api.bilibili.com/x/web-interface/view/detail?bvid=" + self.bvid,
            cache=True,
        ).json()["data"]["Card"]["card"]["mid"]

    def download_video_list(self, base_dir=""):
        url = "https://api.bilibili.com/x/web-interface/view/detail?bvid=" + self.bvid
        request = user_manager.get(url, cache=True)
        video = request.json()["data"]["View"]["pages"]
        title = request.json()["data"]["View"]["title"]
        pic = request.json()["data"]["View"]["pic"]
        total = len(video)
        count = 0
        for i in video:
            count += 1
            print(f"{count} / {total}")
            cid = i["cid"]
            part_title = i["part"]
            if not self.download_one(
                    cid, pic, title=title, part_title=part_title, base_dir=base_dir
            ):
                return False
        return True

    def download_one(
            self,
            cid: int,
            pic_url: str,
            title: str = "",
            part_title: str = "",
            base_dir: str = "",
            save_path: str = "download"
    ):
        if not self.bangumi:
            url = f"https://api.bilibili.com/x/player/playurl?cid={cid}&qn={self.quality}&bvid={self.bvid}"
        else:
            url = f"https://api.bilibili.com/pgc/player/web/playurl?qn={self.quality}&cid={cid}&ep_id={self.bvid}"

        req = user_manager.get(url)
        download_url = req.json()["data" if not self.bangumi else "result"]["durl"][0][
            "url"
        ]
        if base_dir:
            download_dir = save_path+"/" + base_dir + "/"
        else:
            download_dir = save_path+"/"
        res = user_manager.get(download_url, stream=True)
        length = float(res.headers["content-length"])
        if not os.path.exists("download"):
            os.mkdir("download")
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        dts = download_dir + validate_title(part_title) + ".mp4"
        if os.path.exists(dts):
            return -100
        file = open(dts, "wb")
        progress = tqdm(
            total=length,
            initial=os.path.getsize(dts),
            unit_scale=True,
            desc=reprlib.repr(validate_title(part_title)).replace("'", "") + ".mp4",
            unit="B",
        )
        retries = 3

        while retries > 0:
            try:
                for chuck in res.iter_content(chunk_size=1024):
                    file.write(chuck)
                    progress.update(1024)
                break
            except KeyboardInterrupt:
                file.close()
                os.remove(dts)
                if len(os.listdir(download_dir)) == 0:
                    os.rmdir(download_dir)
                print("取消下载.")
                return False
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
                file.close()
                os.remove(dts)
                print("超时下载跳过")
        if not file.closed:
            file.close()
        return True

    def select_video(self):
        r = user_manager.get(
            "https://api.bilibili.com/x/web-interface/view/detail?bvid=" + self.bvid,
            cache=True,
        )
        if r.json()["code"] != 0:
            print("获取视频信息错误!")
            print(r.json()["code"])
            print(r.json()["message"])
            return
        video = r.json()["data"]["View"]["pages"]
        title = r.json()["data"]["View"]["title"]
        pic = r.json()["data"]["View"]["pic"]
        if len(video) == 1:
            return (
                video[0]["cid"],
                title,
                video[0]["part"],
                pic,
                r.json()["data"]["View"]["stat"]["evaluation"],
            )