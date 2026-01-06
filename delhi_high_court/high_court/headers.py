import time
class HeaderHelper:

    def getCaptchaImage_header():

        headers = {
            "Accept": "image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "judiciary.karnataka.gov.in",
            "Priority": "u=5, i",
            "Referer": "https://judiciary.karnataka.gov.in/",
            "Sec-Fetch-Dest": "image",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0"
        }
        params={
            str(int(time.time() * 1000)):""
        }

        return headers,params
    
    def verifyAndGetChallanDetails_header(case_code, case_no, case_year, captcha_text,_token):

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "delhihighcourt.nic.in",
            "Origin": "https://delhihighcourt.nic.in",
            "Priority": "u=0, i",
            "Referer": "https://delhihighcourt.nic.in/app/case-number",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0"
        }

        payload = {
            "_token": _token,
            "case_type": case_code,
            "case_number": case_no,
            "year": case_year,
            "randomid": captcha_text,
            "captchaInput": captcha_text
        }

        return headers,payload