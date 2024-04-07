from B站.BilibiliVideo import BilibiliVideo
from B站.utils import user_manager


class BilibiliInterface:
    def __init__(self):
        self.audio = 30280
        self.quality: int = 32 if not user_manager.mid else 80
        self.view_online_watch = True
        self.source = "main"

    def view_video(self, bvid, no_favorite=False):
        video = BilibiliVideo(
            bvid=bvid, quality=self.quality, view_online_watch=self.view_online_watch, source=self.source
        )
        return video