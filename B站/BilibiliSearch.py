import time

from B站.utils import user_manager, remove, encrypt_wbi
from urllib.parse import quote

class BilibiliSearch:
    @staticmethod
    def search(keyword):
        pre_page = 42
        cursor = 1
        wbi = encrypt_wbi()
        url = (f"https://api.bilibili.com/x/web-interface/wbi/search/all/v2?"
               f"__refresh__=true&_extra=&context=&page={cursor}&page_size={pre_page}&"
               f"order=&duration=&from_source=&from_spmid=333.337&platform=pc&"
               f"highlight=1&single_column=0&keyword={quote(keyword)}&qv_id={wbi['qv_id']}&"
               f"ad_resource=5646&source_tag=3&web_location=1430654&w_rid={wbi['w_rid']}&wts={wbi['wts']}")

        ls = user_manager.get(url,
            cache=True
        )
        if len(ls.json()["data"]["result"]) == 0:
            return None
        result = ls.json()["data"]["result"]
        for item in result:
            if item['result_type'] == 'video':
                for video in item['data']:
                    yield video
        cursor += 1