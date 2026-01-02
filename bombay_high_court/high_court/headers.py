import time
class HeaderHelper:

    def loadIndexPage_header():
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "bombayhighcourt.nic.in",
            "Priority": "u=0, i",
            "Referer": "https://bombayhighcourt.nic.in/",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0"
        }

        return headers
    
    def loadCaseNoWise_header():

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "bombayhighcourt.nic.in",
            "Priority": "u=0, i",
            "Referer": "https://bombayhighcourt.nic.in/index.php",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0"
        }

        return headers
    
    def getCaptchaText_header():

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "bombayhighcourt.nic.in",
            "Priority": "u=0, i",
            "Referer": "https://bombayhighcourt.nic.in/index.php",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0"
        }

        return headers
   
    def loadCaseDetails_header(Case_No,CSRFName, CSRFToken,captcha_text):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "bombayhighcourt.nic.in",
            "Origin": "https://bombayhighcourt.nic.in",
            "Priority": "u=0, i",
            "Referer": "https://bombayhighcourt.nic.in/ord_qrywebcase.php",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0"
        }

        payload = {
            "CSRFName": CSRFName,
            "CSRFToken": CSRFToken,
            "pageno": "1",
            "m_sideflg": "C",
            "m_sr": "R",
            "m_skey": "AO",
            "m_no": Case_No,
            "m_yr": "2020",
            "captchaflg": "",
            "captcha_code": captcha_text,
            "submit1": "Submit"
        }

        return headers, payload
   