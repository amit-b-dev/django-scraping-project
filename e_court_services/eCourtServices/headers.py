import time
class HeaderHelper:

    def getCaptchaText_Header(app_token):

        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "services.ecourts.gov.in",
            "Origin": "https://services.ecourts.gov.in",
            "Referer": "https://services.ecourts.gov.in/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
            "X-Requested-With": "XMLHttpRequest",
        }

        payload={
            "ajax_req": "true",
            "app_token": "",
        }

        return headers,payload
    
    def getCaseDetailsPage_Header(cnr_no,captcha_text,app_token):

        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "services.ecourts.gov.in",
            "Origin": "https://services.ecourts.gov.in",
            "Referer": "https://services.ecourts.gov.in/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
            "X-Requested-With": "XMLHttpRequest",
        }

        payload = {
                "cino": cnr_no,
                "fcaptcha_code": captcha_text,
                "ajax_req": "true",
                "app_token": app_token
            }

        return headers,payload
    
    def viewBusiness_header(result,Order_Date,Court_Number,srno,app_token):
        payload = {
            "court_code": result['court_code'],
            "state_code": result['state_code'],
            "dist_code": result['dist_code'],
            "nextdate1": "",
            "case_number1": result['cino'],
            "disposal_flag": "Disposed",
            "businessDate": Order_Date,
            "national_court_code": result['national_court_code'],
            "court_no": Court_Number,
            "search_by": "cnr",
            "srno": srno,
            "ajax_req": "true",
            "app_token": app_token
        }

        headers = {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Host": "services.ecourts.gov.in",
                "Origin": "https://services.ecourts.gov.in",
                "Referer": "https://services.ecourts.gov.in/",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
                "X-Requested-With": "XMLHttpRequest"
        }

        return headers,payload
    
    def getPdfDetails_header(params,app_token):
        payload = {
            "normal_v": params[0],
            "case_val": params[1],
            "court_code": params[2],
            "filename": params[3],
            "appFlag": params[4],
            "ajax_req": "true",
            "app_token": app_token
        }
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "services.ecourts.gov.in",
            "Referer": "https://services.ecourts.gov.in/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0"
        }

        return headers,payload
