
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


burp0_url = f"https://www.instagram.com:443/api/v1/feed/reels_media/?reel_ids={profile_id}"
burp0_cookies = {"mid": "Zb27zwALAAG1XF6FxS5S3OxEgb0_", "ig_did": "40E84C42-49CF-4755-B82D-2DAF2E807DF8", "datr": "z7u9ZVadspTsWThsZdpbCSvP", "ps_l": "0", "ps_n": "0", "csrftoken": "6EPqSVoB0E2PtC5bC6WhKWlmoKbHQM70", "ds_user_id": "64624470825", "sessionid": "64624470825%3AnPBQCs54el2NmJ%3A19%3AAYf0fk_xXMHhTAPbgFog-JO96fCWVmScnOyP7y-APQ", "rur": "\"CCO\\05464624470825\\0541738479408:01f7444af05d1775fff20b2c86f21266038c0e33aefb20ca1bacd9da45c44dc411f77a7a\""}
burp0_headers = {"Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\"", "X-Ig-Www-Claim": "hmac.AR2maYFFpIx-PKPFOGGT5yndfqCkB07Kl_03YW51lpnbuF2c", "Sec-Ch-Ua-Platform-Version": "\"\"", "X-Requested-With": "XMLHttpRequest", "Dpr": "1", "Sec-Ch-Ua-Full-Version-List": "", "Sec-Ch-Prefers-Color-Scheme": "light", "X-Csrftoken": "6EPqSVoB0E2PtC5bC6WhKWlmoKbHQM70", "Sec-Ch-Ua-Platform": "\"Linux\"", "X-Ig-App-Id": "936619743392459", "Sec-Ch-Ua-Model": "\"\"", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36", "Viewport-Width": "1121", "Accept": "*/*", "X-Asbd-Id": "129477", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.instagram.com/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Priority": "u=1, i"}
res = session.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)

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
