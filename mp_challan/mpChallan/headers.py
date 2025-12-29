import time
class HeaderHelper:

    def getCaptchaImageAndSolver_header():

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "echallan.mponline.gov.in",
            "Referer": "https://echallan.mponline.gov.in/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
            "X-Requested-With": "XMLHttpRequest",
        }

        return headers
    
    def verifyAndGetChallanDetails_header(vehicle_no, captcha_text, csrf_token):

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "echallan.mponline.gov.in",
            "Referer": "https://echallan.mponline.gov.in/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
            "X-Requested-With": "XMLHttpRequest",
        }

        files = {
            "number": (None, vehicle_no),
            "captcha_text": (None, captcha_text),
            "csrf_token": (None, csrf_token)
        }

        return headers,files