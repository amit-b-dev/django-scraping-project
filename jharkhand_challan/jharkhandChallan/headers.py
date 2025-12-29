import time
class HeaderHelper:

    def searchChallanDetails_header(vehicle_no,captcha_text):

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "echallan.jhpolice.gov.in",
            "Origin": "https://echallan.jhpolice.gov.in",
            "Priority": "u=0, i",
            "Referer": "https://echallan.jhpolice.gov.in/payment/payonline",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
        }

        payload={
            "filter_by": "1",
            "vehicle_regt_no": vehicle_no,
            "captcha": captcha_text
        }

        return headers,payload