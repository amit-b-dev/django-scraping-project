from bs4 import BeautifulSoup
from datetime import datetime
import re,time, json

class Extractor:
    def __init__(self, session):
        self.session = session
    
    def setNewCookies(self,res):
        soup = BeautifulSoup(res.text,"html.parser")
        onclick = soup.find(id="cities").find_all("li")[0].find("a")["onclick"]
        value = re.search(r"SelectCity\('(.+?)'\)", onclick).group(1)
        mojibake = value.encode("utf-8").decode("latin-1")
        cookies = self.session.cookies.get_dict()
        cookies['kOneColor']=""
        cookies['KOneUserCity']=mojibake

        return cookies
    
    def makePoliceCollectionOfFine_url(self,res):
        soup=BeautifulSoup(res.text,"html.parser")
        all_li = soup.find(id="collapse1")
        a_tag = all_li.find("a",string=lambda s: s and "Traffic Police Violation Fine" in s)
        PoliceCollectionOfFine_url = "https://www.karnatakaone.gov.in/"+a_tag['href']

        return PoliceCollectionOfFine_url
    
    def extractParameterForSendOTP(self,res,mobile_no):
        soup=BeautifulSoup(res.text,"html.parser")
        flag = soup.find(id="hdn_Flag")["value"]
        params = {
            "Mobile": mobile_no,
            "Flag": flag,
            "_": int(time.time() * 1000)
        }
        return params
    
    def extractParameterForVerifyOTP(self,res,res1,mobile_no,otp=""):
        soup=BeautifulSoup(res.text,"html.parser")
        RequestID = res1.text.split('|')[2]
        params = {
            "Mobile": mobile_no,
            "OTP": otp,
            "RequestID": RequestID,
            "_": int(time.time() * 1000)
        }
        nexttonext_requests={
            "Hidden_RequestID" : res1.text.split('|')[2],
            "Hidden_Mobile" : res1.text.split('|')[3],
            "Hidden_ServiceID" : soup.find(id="Hidden_ServiceID")["value"],
            "Hidden_Flag" : soup.find(id="hdn_Flag")["value"],
            "Hidden_OTPValidation" : soup.find(id="hdn_OTPValid")["value"],
            "__RequestVerificationToken" : soup.find("input",{"name":"__RequestVerificationToken"})["value"],
            "MobileNo" : mobile_no,
            "otp" : otp
        }
        return params,nexttonext_requests
    
    def extractParameterForGetChalan(self,res,reg_no):
        soup=BeautifulSoup(res.text,"html.parser")
        Token =  soup.find("input",{"name":"__RequestVerificationToken"})["value"]
        params = {
            "CaptchaResponse": "",
            "CityServiceId": "59",
            "DuplicateCheckRequired": "Y",
            "FetchType": "APICALL",
            "SearchBy": "REGNO",
            "SearchValue": reg_no,
            "ServiceCode": "BPS",
        }
        # nexttonext_requests={
        #     "Hidden_RequestID" : res.text.split('|')[2],
        #     "Hidden_Mobile" : res.text.split('|')[3],
        #     "Hidden_ServiceID" : soup.find(id:"Hidden_ServiceID")["value"],
        #     "Hidden_Flag" : soup.find(id:"hdn_Flag")["value"],
        #     "Hidden_OTPValidation" : soup.find(id:"hdn_OTPValid")["value"],
        #     "__RequestVerificationToken" : soup.find("input",{"name":"__RequestVerificationToken"})["value"],
        #     "MobileNo" : mobile_no,
        #     "otp" : otp
        # }
 

        return params,Token
    
    def extractFromRes(self,res):
        data = json.loads(res.text)
        mainDict = data.get("PoliceFineDetailsList", [])
        results = []
        for item in mainDict:
            results.append({
                "notice_no": item.get("NoticeNo"),
                "vehicle_no": item.get("RegistrationNo"),
                "violation_date": item.get("ViolationDate"),
                "violation_time": item.get("ViolationTime"),
                "place": item.get("PointName"),
                "offence": item.get("OffenceDescription"),
                "fine_amount": item.get("FineAmount"),
                "name": item.get("Name"),
                "address": item.get("Address")
            })

        print(results)

        return results