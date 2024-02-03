import requests
from bs4 import BeautifulSoup
import re

session = requests.session()

profile_id = ''
insta_username = "aymansadiq10"
burp0_url = f"https://www.instagram.com:443/{insta_username}"
burp0_cookies = {"mid": "Zb27zwALAAG1XF6FxS5S3OxEgb0_", "ig_did": "40E84C42-49CF-4755-B82D-2DAF2E807DF8",
                 "datr": "z7u9ZVadspTsWThsZdpbCSvP", "ps_l": "0", "ps_n": "0",
                 "csrftoken": "6EPqSVoB0E2PtC5bC6WhKWlmoKbHQM70", "ds_user_id": "64624470825",
                 "sessionid": "64624470825%3AnPBQCs54el2NmJ%3A19%3AAYfrcwQ2HGnA1uP_t7ePZHhoT_njeaUnEL-QUuHV1A"}
burp0_headers = {"Dpr": "1", "Viewport-Width": "1121", "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\"",
                 "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Linux\"", "Sec-Ch-Ua-Platform-Version": "\"\"",
                 "Sec-Ch-Ua-Model": "\"\"", "Sec-Ch-Ua-Full-Version-List": "", "Sec-Ch-Prefers-Color-Scheme": "light",
                 "Upgrade-Insecure-Requests": "1",
                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36",
                 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                 "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
                 "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9",
                 "Priority": "u=0, i"}
res1 = session.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
profile_id_match = re.search(r'"profile_id":"(\d+)"', res1.text)

if profile_id_match:
    profile_id = profile_id_match.group(1)
    print("Profile ID:", profile_id)
else:
    print("Profile ID not found.")
burp0_url = "https://i.instagram.com:443/api/v1/feed/reels_media/"
burp0_headers = {"X-Ig-App-Locale": "en_US", "X-Ig-Device-Locale": "en_US", "X-Ig-Mapped-Locale": "en_US",
                 "X-Pigeon-Session-Id": "UFS-30520e23-e266-4524-85a0-fcb6353dd346-0",
                 "X-Pigeon-Rawclienttime": "1706936911.137", "X-Ig-Bandwidth-Speed-Kbps": "-1.000",
                 "X-Ig-Bandwidth-Totalbytes-B": "0", "X-Ig-Bandwidth-Totaltime-Ms": "0",
                 "X-Bloks-Version-Id": "8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb",
                 "X-Ig-Www-Claim": "hmac.AR3uJzb8t6VLltnBXQ2nRf7OumJdO0K1kwnUAPw_ZD3r7JTt",
                 "X-Bloks-Is-Layout-Rtl": "false", "X-Ig-Device-Id": "5090d207-5663-422c-ae6d-de376adff857",
                 "X-Ig-Family-Device-Id": "8a8b4b4d-fbdb-4fd2-8a71-41273fbd456e",
                 "X-Ig-Android-Id": "android-38ccb27adcf5a7b6", "X-Ig-Timezone-Offset": "-21600",
                 "X-Ig-Nav-Chain": "MainFeedFragment:feed_timeline:1:cold_start:1706936715.484::",
                 "X-Ig-Salt-Logger-Ids": "15335435,25624577,20119557,17301505,31784991,857816154,25101347,42991645,42991646,61669378",
                 "X-Fb-Connection-Type": "WIFI", "X-Ig-Connection-Type": "WIFI", "X-Ig-Capabilities": "3brTv10=",
                 "X-Ig-App-Id": "567067343352427", "Priority": "u=3",
                 "User-Agent": "Instagram 275.0.0.27.98 Android (29/10; 440dpi; 1080x2131; Xiaomi/xiaomi; Redmi Note 7 Pro; violet; qcom; en_US; 458229219)",
                 "Accept-Language": "en-US",
                 "Authorization": "Bearer IGT:2:eyJkc191c2VyX2lkIjoiNjQ2MjQ0NzA4MjUiLCJzZXNzaW9uaWQiOiI2NDYyNDQ3MDgyNSUzQXZFaVVUTmU3RTJiMHc4JTNBMCUzQUFZZHd5QUNvWXl0TDVTR2UxNXNqUmJIY05YS1VJRlgxSGM0UnlBNG9qUSJ9",
                 "X-Mid": "Zb3EPQABAAH_RnlfBHyFIjeN5ziw",
                 "Ig-U-Ig-Direct-Region-Hint": "ODN,64624470825,1738471573:01f777037d290c4a8182a3efd5d77a83fa33378c5f9f531f145a2c6de0708cabdc07bfd4",
                 "Ig-U-Ds-User-Id": "64624470825",
                 "Ig-U-Rur": "CCO,64624470825,1738472899:01f73f6bda5720932595ea956d71e4478d4fd51772723dd155f95fc604864e93d34765ea",
                 "Ig-Intended-User-Id": "64624470825",
                 "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                 "Accept-Encoding": "gzip, deflate, br", "X-Fb-Http-Engine": "Liger", "X-Fb-Client-Ip": "True",
                 "X-Fb-Server-Cluster": "True"}

burp0_data = {"signed_body": (
        "SIGNATURE.{\"exclude_media_ids\":\"[]\",\"supported_capabilities_new\":\"[{\\\"name\\\":\\\"SUPPORTED_SDK_VERSIONS\\\",\\\"value\\\":\\\"131.0,132.0,133.0,134.0,135.0,136.0,137.0,138.0,139.0,140.0,141.0,142.0,143.0,144.0,145.0,146.0,147.0,148.0,149.0,150.0,151.0,152.0,153.0,154.0,155.0,156.0,157.0,158.0,159.0\\\"},{\\\"name\\\":\\\"FACE_TRACKER_VERSION\\\",\\\"value\\\":\\\"14\\\"},{\\\"name\\\":\\\"segmentation\\\",\\\"value\\\":\\\"segmentation_enabled\\\"},{\\\"name\\\":\\\"COMPRESSION\\\",\\\"value\\\":\\\"ETC2_COMPRESSION\\\"},{\\\"name\\\":\\\"gyroscope\\\",\\\"value\\\":\\\"gyroscope_enabled\\\"}]\",\"source\":\"feed_timeline\",\"_uid\":\"64624470825\",\"_uuid\":\"5090d207-5663-422c-ae6d-de376adff857\",\"reel_ids\":[\"%s\"]}" % profile_id)}
res = session.post(burp0_url, headers=burp0_headers, data=burp0_data)
data = res.json()
stories = data['reels'][profile_id]['items']

story_count = 0
for story in stories:
    story_count += 1
    try:
        video_url = story['video_versions'][0]['url']
        response = requests.get(url=video_url)
        if response.status_code == 200:
            with open(f"{story_count}-{insta_username}_video.mp4", "wb") as file:
                file.write(response.content)
            print("Video downloaded successfully.")
            continue
        else:
            print(f"Failed to download video. Status code: {response.status_code}")
    except KeyError:
        pass

    try:
        photo_url = story['image_versions2']['candidates'][0]['url']
        response = requests.get(url=photo_url)

        if response.status_code == 200:
            with open(f"{story_count}-{insta_username}-photo.jpeg", "wb") as file:
                file.write(response.content)
            print("Photo downloaded successfully.")
        else:
            print(f"Failed to download Photo. Status code: {response.status_code}")
    except KeyError:
        pass
