class HeaderHelper:

    def guestLoginWithOutMob_header(): 
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "www.karnatakaone.gov.in",
            "Referer": "https://www.karnatakaone.gov.in/",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
        }
        return headers
    
    def showCityList_header(): 
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "www.karnatakaone.gov.in",
            "Referer": "https://www.karnatakaone.gov.in/PortalHome",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
            "X-Requested-With": "XMLHttpRequest",
        }
        return headers

    def selectCity_header():
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "www.karnatakaone.gov.in",
            "Referer": "https://www.karnatakaone.gov.in/PortalHome",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
            "X-Requested-With": "XMLHttpRequest",
        }
        return headers

    def serviceList_header():
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "www.karnatakaone.gov.in",
            "Referer": "https://www.karnatakaone.gov.in/PortalHome/Index/Bengaluru",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
            "X-Requested-With": "XMLHttpRequest",
        }
        return headers

    def selectPoliceCollectionFine_header():
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "www.karnatakaone.gov.in",
            "Referer": "https://www.karnatakaone.gov.in/PortalHome/ServiceList",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
            "X-Requested-With": "XMLHttpRequest",
        }

        return headers
    
    def sendOTP_header(PoliceCollectionOfFine_url):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "www.karnatakaone.gov.in",
            "Referer": PoliceCollectionOfFine_url,
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
            "X-Requested-With": "XMLHttpRequest",
        }
        # params = {
        #     "Mobile": mobile_no,
        #     "Flag": flag,
        #     "_": time
        # }
        return headers

    def otpValidation_header(PoliceCollectionOfFine_url):
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "www.karnatakaone.gov.in",
            "Referer": PoliceCollectionOfFine_url,
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
            "X-Requested-With": "XMLHttpRequest",
        }
        # params = {
        #     "Mobile": mobile_no,
        #     "OTP": otp,
        #     "RequestID": RequestID,
        #     "_": time
        # }
        return headers

    def PoliceFineDetails_header(PoliceCollectionOfFine_url,nexttonext_requests):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "www.karnatakaone.gov.in",
            "Referer": PoliceCollectionOfFine_url,
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
        }

        payload = {
            "Hidden_Mobile": nexttonext_requests["Hidden_Mobile"],
            "Hidden_RequestID": nexttonext_requests["Hidden_RequestID"],
            "Hidden_ServiceID": nexttonext_requests["Hidden_ServiceID"],
            "Hidden_Flag": nexttonext_requests["Hidden_Flag"],
            "Hidden_OTPValidation": nexttonext_requests["Hidden_OTPValidation"],
            "__RequestVerificationToken": nexttonext_requests["__RequestVerificationToken"],
            "MobileNo": nexttonext_requests["MobileNo"],
            "OTP": nexttonext_requests["otp"]
        }

        return headers,payload

    def searchRegNoWise_header(Token):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "www.karnatakaone.gov.in",
            "Referer": "https://www.karnatakaone.gov.in/PoliceCollectionOfFine/PoliceCollectionOfFineLogin",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
            "X-Requested-With": "XMLHttpRequest",
            "X-XSRF-Token": Token
        }
        # params = {
        #     "CaptchaResponse": "",
        #     "CityServiceId": "59",
        #     "DuplicateCheckRequired": "Y",
        #     "FetchType": "APICALL",
        #     "SearchBy": "REGNO",
        #     "SearchValue": "KA03KC1829",
        #     "ServiceCode": "BPS",
        # }

        return headers

