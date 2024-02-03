import requests
import re

session = requests.session()


def like_post(media_id="3289475632610071772"):
    fb_dtsg = ""
    url2 = "https://www.instagram.com:443/"
    cookies = {"mid": "Zb27zwALAAG1XF6FxS5S3OxEgb0_", "ig_did": "40E84C42-49CF-4755-B82D-2DAF2E807DF8",
                     "datr": "z7u9ZVadspTsWThsZdpbCSvP", "ps_l": "0", "ps_n": "0",
                     "csrftoken": "6EPqSVoB0E2PtC5bC6WhKWlmoKbHQM70", "ds_user_id": "64624470825",
                     "sessionid": "64624470825%3AnPBQCs54el2NmJ%3A19%3AAYf0fk_xXMHhTAPbgFog-JO96fCWVmScnOyP7y-APQ"}

    headers2 = {"Dpr": "1", "Viewport-Width": "1121",
                "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\"", "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": "\"Linux\"", "Sec-Ch-Ua-Platform-Version": "\"\"",
                "Sec-Ch-Ua-Model": "\"\"", "Sec-Ch-Ua-Full-Version-List": "",
                "Sec-Ch-Prefers-Color-Scheme": "light", "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
                "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-US,en;q=0.9", "Priority": "u=0, i"}
    res_dtsg = session.get(url2, headers=headers2, cookies=cookies)

    regex_pattern = r'"token":"(.*?)"'

    match = re.search(regex_pattern, res_dtsg.text)

    if match:
        fb_dtsg = match.group(1)
        print("Extracted fb_dtsg:", fb_dtsg)
    else:
        print("Token not found.")

    _url = "https://www.instagram.com:443/api/graphql"

    _headers = {"Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\"",
                "X-Fb-Friendly-Name": "usePolarisLikeMediaLikeMutation", "Sec-Ch-Ua-Platform-Version": "\"\"",
                "Dpr": "1", "Sec-Ch-Ua-Full-Version-List": "", "Sec-Ch-Prefers-Color-Scheme": "light",
                "X-Csrftoken": "6EPqSVoB0E2PtC5bC6WhKWlmoKbHQM70", "Sec-Ch-Ua-Platform": "\"Linux\"",
                "X-Ig-App-Id": "936619743392459", "Sec-Ch-Ua-Model": "\"\"", "Sec-Ch-Ua-Mobile": "?0",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36",
                "Viewport-Width": "1121", "Content-Type": "application/x-www-form-urlencoded",
                "X-Fb-Lsd": "BYXau8Tws4tzyrQgsjlZKG", "X-Asbd-Id": "129477", "Accept": "*/*",
                "Origin": "https://www.instagram.com", "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.instagram.com/",
                "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9",
                "Priority": "u=1, i"}

    _data = {"av": "17841464764758058", "__d": "www", "__user": "0", "__a": "1", "__req": "t",
             "__hs": "19756.HYP:instagram_web_pkg.2.1..0.1", "dpr": "1", "__ccg": "UNKNOWN",
             "__rev": "1011207331", "__s": "6opxdx:7lzafk:3jdiup", "__hsi": "7331333718056784082",
             "__dyn": "7xeUjG1mxu1syUbFp60DU98nwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO2O1Vw8G1nzUO0n24oaEd86a3a1YwBgao6C0Mo2iyovw8OfK0EUjwGzEaE7622362W2K0zK5o4q3y1Sx-0iS2Sq2-azqwt8dUaob82cwMwrUdUbGwmk1xwmo6O1FwlE6PhA6bxy4UjK5V8",
             "__csr": "hYO1r222chN_4jh7syV6yitpd9tIGXlV6J5G9Vrl4XBJQm4AiFK-uijLGpb9iTt6zk4FHJmpeiQjpaumazXVoVkaLhqx6QlejCy9rCCXybAybwgpoZzUiw05fgyU2ox64Zwqy075g0OC07bqx1hpnhFE2Sg56q2217xe0le4U0Wm0x9780tqaw4aw71w5jIB08-00A6E",
             "__comet_req": "7",
             "fb_dtsg": "NAcPO7QnbQuh7eYUpeWxvG1_21_oNLLZKRIdlQfJrl5jInnIU7ZtENw:17843683195144578:1706933258",
             "jazoest": "26349", "lsd": "BYXau8Tws4tzyrQgsjlZKG", "__spin_r": "1011207331",
             "__spin_b": "trunk", "__spin_t": "1706959148", "fb_api_caller_class": "RelayModern",
             "fb_api_req_friendly_name": "usePolarisLikeMediaLikeMutation",
             "variables": ("{\"media_id\":\"%s\"}" % media_id), "server_timestamps": "true",
             "doc_id": "6496452950454065"}
    res_like = session.post(_url, headers=_headers, cookies=cookies, data=_data)

    print(res_like.status_code)


like_post()
