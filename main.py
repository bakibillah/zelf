import requests
import re
from selenium.webdriver.chrome.service import Service
import time
from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import subprocess
import os
from webdriver_manager.chrome import ChromeDriverManager
from collections import OrderedDict


class ScrapeInstaStory:
    def __init__(self, username, password):
        self.insta_username = None
        self.cookie_header = OrderedDict()
        self.username = username
        self.password = password
        self.session = requests.session()

    def login(self):

        """
        * Instagram web doesn't have very sophisticated bot detection, so i am using here selenium.
        * for other site that have cloudflare, akamai or Imperva bot detection implemented will need different set up.
        Here as i focused on downloading Instagram story, so i did not implement that system as Instagram allowed us to
        login using selenium
        * to bypass bot detection we should use PyChromeDevTools library.
        * We used requests library here as HTTP Client but it will be detected as bot by cloudflare or akamai. They check
        TLS Fingerprint, to spoof tls fingerprint we can use requests_tls library. Here i used requests as Instagram does
        not check tls fingerprint, so i faced no blocj here.
        * For instagram we can intercept Instagram android network traffic and extract the access_token and using the API
        directly. for most of the cases it will be much faster and CPU-Memory efficient
        * Here the chrome opening code is valid for debian based Linux distros. for Mac and Windows there will be sightly
        different command
        * Here i used incognito mode of the chrome to demonstrate a login flow but in the production environment we may
         not use incognito mode as we will save our profile path and reuse them
         * Here I used a chrome profile that has already been opened at least one. if you set the chrome profile path to something
         else or run the code on a machine where this profile ($HOME/insta-scraper) has not been opened at least once then
         first run of the code will not work. from the second run it will work. this issue can be overcomed by opening
         a headless chrome then close it then again open it but i skipped that implementation here. So if you run this code
         in a new machine please either set ($HOME/profile) to your profile path that has already been opened once or
         first run the code then stop the code and run it again. I think handling various chrome initial pop up is out of
         this task.
         * In the production environment we will once login and save the cookies and will continue to use untill that gets
         invalidated
        """
        command = ("google-chrome --user-data-dir=$HOME/insta-scraper --incognito --remote-debugging-port=9222 "
                   "--remote-allow-origins=http://localhost:9222 --blink-settings=imagesEnabled=true")
        subprocess.Popen(command, shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, close_fds=True)
        time.sleep(2)

        options = webdriver.ChromeOptions()
        options.add_experimental_option("debuggerAddress", f'127.0.0.1:{9222}')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        try:
            driver.get('https://instagram.com')
            time.sleep(1)
            username = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.NAME, "username"))
            username.clear()
            username.send_keys(self.username)
            password = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.NAME, "password"))
            password.clear()
            password.send_keys(self.password)
            submit_user = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, "//button[@type='submit']"))
            submit_user.click()
            time.sleep(2)
            do_not_save = WebDriverWait(driver, 30).until(
                lambda x: x.find_elements(By.CSS_SELECTOR, 'button[type="button"]'))
            do_not_save[0].click()
            time.sleep(10)
            insta_cookies = driver.get_cookies()
            self.cookie_header = {cookie["name"]: cookie["value"] for cookie in insta_cookies}
            print(self.cookie_header)
            return True
        except Exception as e:
            print(e)
        finally:
            driver.close()
            driver.quit()

    def get_profile_id(self, insta_username):
        _url = f"https://www.instagram.com:443/{insta_username}"
        headers_profile_id = {"Dpr": "1", "Viewport-Width": "1121",
                              "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\"",
                              "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Linux\"",
                              "Sec-Ch-Ua-Platform-Version": "\"\"",
                              "Sec-Ch-Ua-Model": "\"\"", "Sec-Ch-Ua-Full-Version-List": "",
                              "Sec-Ch-Prefers-Color-Scheme": "light",
                              "Upgrade-Insecure-Requests": "1",
                              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36",
                              "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                              "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
                              "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate",
                              "Accept-Language": "en-US,en;q=0.9",
                              "Priority": "u=0, i"}
        res1 = self.session.get(_url, headers=headers_profile_id, cookies=self.cookie_header)
        profile_id_match = re.search(r'"profile_id":"(\d+)"', res1.text)

        if profile_id_match:
            matched_profile_id = profile_id_match.group(1)
            print("Profile ID:", matched_profile_id)
            return matched_profile_id
        else:
            print("Profile ID not found.")
            return False

    def download_story(self, profileid, insta_username):

        output_directory = "story_media"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        url_reels_media = f"https://www.instagram.com:443/api/v1/feed/reels_media/?reel_ids={profileid}"
        headers_story = {"Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\"",
                         "X-Ig-Www-Claim": "hmac.AR2maYFFpIx-PKPFOGGT5yndfqCkB07Kl_03YW51lpnbuF2c",
                         "Sec-Ch-Ua-Platform-Version": "\"\"", "X-Requested-With": "XMLHttpRequest", "Dpr": "1",
                         "Sec-Ch-Ua-Full-Version-List": "", "Sec-Ch-Prefers-Color-Scheme": "light",
                         "X-Csrftoken": "6EPqSVoB0E2PtC5bC6WhKWlmoKbHQM70", "Sec-Ch-Ua-Platform": "\"Linux\"",
                         "X-Ig-App-Id": "936619743392459", "Sec-Ch-Ua-Model": "\"\"", "Sec-Ch-Ua-Mobile": "?0",
                         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36",
                         "Viewport-Width": "1121", "Accept": "*/*", "X-Asbd-Id": "129477",
                         "Sec-Fetch-Site": "same-origin",
                         "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.instagram.com/",
                         "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Priority": "u=1, i"}
        try:
            res = self.session.get(url_reels_media, headers=headers_story, cookies=self.cookie_header)
            if res.status_code != 200:
                print('something went wrong, downloading story has failed')
                return False
            data = res.json()

            stories = data['reels']
            if len(stories) == 0:
                print('No stories found for the selected Instagram user')
                return
            stories = data['reels'][profileid]['items']

            story_count = 0
            for story in stories:
                story_count += 1
                try:
                    video_url = story['video_versions'][0]['url']
                    response = requests.get(url=video_url)
                    if response.status_code == 200:
                        with open(f"{output_directory}/{story_count}-{insta_username}_video.mp4", "wb") as file:
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
                        with open(f"{output_directory}/{story_count}-{insta_username}-photo.jpeg", "wb") as file:
                            file.write(response.content)
                        print("Photo downloaded successfully.")
                    else:
                        print(f"Failed to download Photo. Status code: {response.status_code}")
                except KeyError:
                    pass
        except Exception as e:
            print(e)

    def like_post(self, media_id="3289475632610071772"):
        fb_dtsg = ""
        url2 = "https://www.instagram.com:443/"
        headers2 = {"Dpr": "1", "Viewport-Width": "1121",
                         "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\"", "Sec-Ch-Ua-Mobile": "?0",
                         "Sec-Ch-Ua-Platform": "\"Linux\"", "Sec-Ch-Ua-Platform-Version": "\"\"",
                         "Sec-Ch-Ua-Model": "\"\"", "Sec-Ch-Ua-Full-Version-List": "",
                         "Sec-Ch-Prefers-Color-Scheme": "light", "Upgrade-Insecure-Requests": "1",
                         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36",
                         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                         "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
                         "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br",
                         "Accept-Language": "en-US,en;q=0.9", "Priority": "u=0, i"}
        res_dtsg = self.session.get(url2, headers=headers2, cookies=self.cookie_header)

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
                         "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9",
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
        res_like = self.session.post(_url, headers=_headers, cookies=self.cookie_header, data=_data)


if __name__ == '__main__':
    target_username = input("Enter the username of a target user: ").strip()
    # Initialize the class ScrapeInstaStory with a valid instagram username & password, here we assumed instagram user
    # does not have two-factor authentication enabled.
    insta_scraper = ScrapeInstaStory('mahdizubayer@gmail.com', 'as598249')
    login_status = insta_scraper.login()
    if login_status:
        profile_id = insta_scraper.get_profile_id(insta_username=target_username)
        if profile_id:
            insta_scraper.download_story(profileid=profile_id, insta_username=target_username)
    else:
        print('Login to instagram failed')
