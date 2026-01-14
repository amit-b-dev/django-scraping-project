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
    
    def verifyAndGetChallanDetails_header(bench_code, case_code, case_no, case_year, captcha_text):

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "judiciary.karnataka.gov.in",
            "Origin": "https://judiciary.karnataka.gov.in",
            "Priority": "u=0",
            "Referer": "https://judiciary.karnataka.gov.in/rep_judgmentcase.php",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
            "X-Requested-With": "XMLHttpRequest"
        }

        payload = {
            "bench": f"1,2,3@{case_code}@{case_no}@{case_year}@{bench_code}@{captcha_text}"
        }
        
        return headers,payload