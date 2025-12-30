import time
class HeaderHelper:

    def getCaptchaImage_header():

        headers = {
            "Accept": "image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "gujarathc-casestatus.nic.in",
            "Referer": "https://gujarathc-casestatus.nic.in/gujarathc/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0"
        }
        params={
            "ct": "S",
            "tm": int(time.time() * 1000)
        }

        return headers,params
    
    def verifyAndGetChallanDetails_header(case_no,captcha_text,ccin,servicecode="1"):

        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "gujarathc-casestatus.nic.in",
            "Origin": "https://gujarathc-casestatus.nic.in",
            "Referer": "https://gujarathc-casestatus.nic.in/gujarathc/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
            "X-Requested-With": "XMLHttpRequest"
        }


        payload = {
            "ccin": ccin,
            "servicecode": servicecode,
            "challengeString": captcha_text
        }

        return headers,payload