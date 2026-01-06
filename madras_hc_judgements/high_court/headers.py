class HeaderHelper:

    def captcha_header(): 
        headers = {
            "Accept": "image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Referer": "https://hcmadras.tn.gov.in/cause_judment_mas.php",
            "Sec-Fetch-Dest": "image",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
            "Host": "hcmadras.tn.gov.in",
        }
        return headers
    
    def getPDF_Header(value_id): 
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "hcmadras.tn.gov.in",
            "Origin": "https://hcmadras.tn.gov.in",
            "Referer": "https://hcmadras.tn.gov.in/cause_judment_mas.php",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-User": "?1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
        }
        payload = {
            "fileName": value_id
        }
        return headers,payload
    
    def getCaseDetails_header(case_code, case_no, case_year, captcha_text):
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://hcmadras.tn.gov.in",
            "Referer": "https://hcmadras.tn.gov.in/cause_judment_mas.php",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
            "X-Requested-With": "XMLHttpRequest",
            "Host": "hcmadras.tn.gov.in",
        }

        payload = {
            "RegCase_type": case_code,
            "RegCase_no": case_no,
            "RegCase_year": case_year,
            "caseno_captcha": captcha_text
        }
        return headers,payload

