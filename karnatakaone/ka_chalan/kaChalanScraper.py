import requests,traceback,re
from .parser import Extractor
from .navigation import NavigationFlow


class KarnatakaoneChalan:
    def __init__(self):
        self.base_url = "https://www.karnatakaone.gov.in/#logi"
        self.session = requests.Session()
        self.extract = Extractor(self.session)
        self.flow = NavigationFlow(self.session)

    def send_otp(self,vehicle_no,mobile_no):
        try:
            cookies = self.flow.load_home_page(self.base_url)
            res,cookies = self.flow.guestLoginWithOutMob(cookies)

            res,cookies = self.flow.showCityList(cookies)
            cookies,city_url = self.extract.setNewCookies(res,vehicle_no)

            res = self.flow.selectCity(cookies,city_url)

            res = self.flow.serviceList(cookies)
            PoliceCollectionOfFine_url = self.extract.makePoliceCollectionOfFine_url(res)

            res = self.flow.selectPoliceFineUrl(cookies,PoliceCollectionOfFine_url)
            params = self.extract.extractParameterForSendOTP(res,mobile_no)
            res1 = self.flow.sendOTP(cookies,PoliceCollectionOfFine_url,params)
            params,nexttonext_requests = self.extract.extractParameterForVerifyOTP(res,res1,mobile_no)

            return {
                "OTP": "",
                "vehicle_no": vehicle_no, 
                "PoliceCollectionOfFine_url": PoliceCollectionOfFine_url,
                "params": params,
                "nexttonext_requests": nexttonext_requests,
                "cookies": cookies
            }
        except:
            traceback.print_exc()
            return {
                "status": "error",
                "message": "Failed to send OTP",
                "data": []
            }

    def verify_otp_and_fetch_chalan(self,vehicle_no,otp,PoliceCollectionOfFine_url,params,nexttonext_requests,cookies):
        try:
            params["OTP"]=otp
            nexttonext_requests["otp"]=otp

            res = self.flow.validateOTP(cookies,PoliceCollectionOfFine_url,params)
            if "Failed|InCorrect OTP" in res.text or "Failed|OTP is Expired" in res.text:
                return {"applications": [], "message": "Please Enter Correct OTP"}
            res = self.flow.policeFineDetailsPage(cookies,PoliceCollectionOfFine_url,nexttonext_requests)
            params,Token = self.extract.extractParameterForGetChalan(res,vehicle_no)

            res = self.flow.getAllChalanDetails(cookies,params,Token)
            data = self.extract.extractFromRes(res)
            return {"applications":data}

        except:
            traceback.print_exc()
            return {"applications":[]}

