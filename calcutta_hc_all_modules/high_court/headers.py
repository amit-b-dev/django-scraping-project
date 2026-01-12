class HeaderHelper:

    def captcha_header(): 
        headers = {
            "Accept": "image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Referer": "https://hcservices.ecourts.gov.in/",
            "Sec-Fetch-Dest": "image",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
        }

        return headers
    
    def getPDF_Header(): 
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "hcservices.ecourts.gov.in",
            "Referer": "https://hcservices.ecourts.gov.in/",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Priority": "u=0, i",
            "TE": "trailers",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
        }
        return headers
    
    def getCaseDetails_header(court_code, case_code, case_no, case_year, captcha_text):
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://hcservices.ecourts.gov.in",
            "Referer": "https://hcservices.ecourts.gov.in/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
            "X-Requested-With": "XMLHttpRequest",
        }

        payload = {
            "action_code": "showRecords",
            "state_code": "16",
            "dist_code": "1",
            "case_type": case_code,
            "case_no": case_no,
            "rgyear": case_year,
            "caseNoType": "new",
            "displayOldCaseNo": "NO",
            "captcha": captcha_text,
            "court_code": court_code
        }
        return headers,payload

    def oCivilCaseHistory_header(court_code, case_no1, cino, token):
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host":"hcservices.ecourts.gov.in",
            "Origin": "https://hcservices.ecourts.gov.in",
            "Priority":"u=0",
            "Referer": "https://hcservices.ecourts.gov.in/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
        }

        payload = {
            "court_code": court_code,
            "state_code": "16",
            "dist_code": "1",
            "case_no": case_no1,
            "cino": cino,
            "token": token,
            "appFlag": ""
        }

        return headers,payload

    def getCaseTypeCode_header(court_code):
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://hcservices.ecourts.gov.in",
            "Referer": "https://hcservices.ecourts.gov.in/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
            "X-Requested-With": "XMLHttpRequest",
        }

        payload = {
            "action_code": "fillCaseType",
            "state_code": "16",
            "dist_code": "1",
            "court_code": court_code
        }
                
        return headers,payload
    
    def dailyStatus_header(values):
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "hcservices.ecourts.gov.in",
            "Origin": "https://hcservices.ecourts.gov.in",
            "Referer": "https://hcservices.ecourts.gov.in/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Priority": "u=0",
            "TE": "trailers"
        }
        payload = {
            "court_code":  values[0],
            "dist_code": values[1],
            "nextdate1": values[2],
            "case_number1": values[3],
            "state_code": values[4],
            "disposal_flag": values[5],
            "businessDate": values[6],
            "court_no": values[7],
            "appFlag": "",
            "srno": values[8],
            "cino": values[9]
            }
        return headers,payload
