# -*- coding: utf-8 -*-
import pandas as pd
import requests
import time

url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
yourcookie = 'rewardsn=; wxtokenkey=777; poc_sid=HMYKKmaj9KU1_MI_-a-AjmGM_66xKAGWNJscY8Tg; ua_id=Ye86MlJqTgx9OuuZAAAAADHpFtQ7K9e0UqneKG0or68=; wxuin=14036445826529; _clck=1r917vs|1|fl8|0; mm_lang=zh_CN; cert=8nWG7qGdcP2fxd0sEp6RccL_MsVN9NwT; uuid=e4ee867eda7dc01e9bdb8f6551645451; rand_info=CAESICWu4cReguJBR4STqu6lNkNo3XnN2WWbt45FlcyY0GOR; slave_bizuin=3905692628; data_bizuin=3905692628; bizuin=3905692628; data_ticket=yGmILgrZkcXkmf9Pkx4FGsx65/pMZsf9QWP9BpNgiZrYQ+G4jONgsuGEmdd3Fpr1; slave_sid=NGtKQ2xUMzhBY1poamZweXdudHgwWVM3YzNEd1Fjc1pfdm5Vdk1RdmxqcEE0ZXJ0WTliRHVPT1JxbkYzM0NuVjFqcG1oOFNKNTdyWVMxX1NsaEVvbVlXTW1LcGNZMWNyaDRCXzhnTkJnUWRITWNCd0JoVDJ5S2Z5WWhCazBsemxZeU5obDdLSmFEbjlhZmll; slave_user=gh_c70e495ae218; xid=b2c4183cd2d0ab73d89b81d9ff98a0b5; _clsk=wxeccb|1714038213975|2|1|mp.weixin.qq.com/weheat-agent/payload/record'
yourfakeid = 'MzIzNzQyMTI2OA=='
yourtoken = '1659690889'
headers = {
  "Cookie": yourcookie,
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
}
number = 0
data_list =[]
while True:
    data = {
        "token": yourtoken,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
        "action": "list_ex",
        "begin": number,
        "count": "5",
        "query": "",
        "fakeid": yourfakeid,
        "type": "9",
    }

    content_json = requests.get(url, headers=headers, params=data).json()
    number += 5
    if len(content_json["app_msg_list"]) == 0:
        break
    for item in content_json["app_msg_list"]:
        data_list.append({"title": item["title"], "url": item['link']})
    time.sleep(5)
df = pd.DataFrame(data_list)
df.to_excel('data.xlsx', index=False)