import json
import requests
import time
import random
from tqdm import tqdm as tq

dir_path = './data/THU社区规划/'

err = open(dir_path + 'err.txt', 'a', encoding='utf-8')
cnt = 0
stp = random.randint(10, 40) * 5
for begin_id in tq(range(0, 55 + 1, 5)):
    # 每次登陆都要更改这里的 cookies 和 url 
    url = f'https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin={begin_id}&count=5&fakeid=Mzg3OTIzMTQzMg==&type=9&query=&token=254423072&lang=zh_CN&f=json&ajax=1'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
    cookies = {"RK" : "Pe8964EBb1",
"ptcz" : "560ed46a1e60cdfd7763eed0bbb112225e0707d55e3b309cfeeaf7a3826805b2",
"pgv_pvid" : "3494662338",
"pac_uid" : "0_20dbd25ad8a9c",
"ptui_loginuin" : "759651575",
"ua_id" : "wbsMIqfSTLgcLnQvAAAAABijQmwbgZQx-dPmb7nKkjI=",
"wxuin" : "57094563063032",
"noticeLoginFlag" : "1",
"mm_lang" : "zh_CN",
"rand_info" : "CAESIK6UwQDiXBDmqXgBG78/GVZcRPb99VnsulWBs35n30bL",
"slave_bizuin" : "3949394487",
"data_bizuin" : "3949394487",
"bizuin" : "3949394487",
"data_ticket" : "h7usos69H7tIyxDqjFx9C+lqyCBAUA7HlvLsKcje4PQcWNbnM2Q4Ur5NLgWBhGwX",
"slave_sid" : "M2Nkd2UybHZBZWF2cWFPUmNjalBLZXRwaDhlVHVCbjF2TmY5eHIzV3QzMktPaDdMVDRpUXZTUTdCQmI5cXhwX0ptUDJCV2pUcXlCS2dYdzczaFBQYVhBVUZqU21qOW1ZS2Fma1d1YmszTGV5aUlLSW1SVUZJaXh6Z3A5c2RGS1FZMVBnY2dYTGVOTldxSHFD",
"slave_user" : "gh_9611f719b693",
"xid" : "50b251a20b1a5b2324f992d7d4e94c83"
}
    req = requests.get(url, headers=headers, cookies=cookies)
    if req.status_code == 200:
        if len(req.text) < 80:
            print(f'freq control at {begin_id}, length of req.text is {len(req.text)}')
            break
        f = open(dir_path + 'jsons/' + str(begin_id) + '.json', 'w', encoding='utf-8')
        f.write(req.text)
        f.close()
        # if begin_id % 150 == 0:
        #     time.sleep(60 + random.random() * 30)
        # print(req.text)
    else:
        err.write(f'[ERROR] status {req.status_code} at {begin_id}')
    time.sleep(3 + random.random() * 2)
    cnt += 5
    if cnt == stp:
        stp += random.randint(10, 40) * 5
        time.sleep(60 + random.random() * 30)

err.close()