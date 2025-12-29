import time
class HeaderHelper:

    def loadWelcomeJsp_header():
        headers = {
            "Accept": "image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "echallan.tspolice.gov.in",
            "Priority": "u=4, i",
            "Referer": "https://echallan.tspolice.gov.in/publicview/css/mobileview.css",
            "Sec-Fetch-Dest": "image",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
        }

        return headers
    
    def loadCaptcha_header():
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "echallan.tspolice.gov.in",
            "Referer": "https://echallan.tspolice.gov.in/publicview/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
            "X-Requested-With": "XMLHttpRequest",
        }
        params = {
            "ctrl": "sess",
            "req": "https://echallan.tspolice.gov.in/publicview/"
        }

        return headers,params
    
    def getCaptchaImage_header(csrf_token):
        headers = {
            "Accept": "image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "echallan.tspolice.gov.in",
            "Priority": "u=4, i",
            "Referer": "https://echallan.tspolice.gov.in/publicview/",
            "Sec-Fetch-Dest": "image",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
        }

        params = {
            "ctrl": "new",
            "_csrfToeknVehNo": csrf_token,
            "t": int(time.time() * 1000)
        }
        return headers,params
    
    def captchaSolverAndFetchChallanDetails_header(vehicle_no,captcha_text,csrf_token):

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "echallan.tspolice.gov.in",
            "Origin": "https://echallan.tspolice.gov.in",
            "Priority": "u=0",
            "Referer": "https://echallan.tspolice.gov.in/publicview/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
            "X-Requested-With": "XMLHttpRequest",
        }
        payload = {
            "ctrl": "tab1",
            "obj": vehicle_no,          # vehicle number
            "obj1": "",  # user-entered captcha
            "put": captcha_text,
            "_csrfToeknVehNo": csrf_token
        }

        return headers, payload