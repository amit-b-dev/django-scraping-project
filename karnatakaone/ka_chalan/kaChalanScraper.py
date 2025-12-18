import requests,traceback,re
from .parser import Extractor
from .navigation import NavigationFlow


class KarnatakaoneChalan:
    def __init__(self):
        self.base_url = "https://www.karnatakaone.gov.in/#logi"
        self.session = requests.Session()
        self.extract = Extractor(self.session)
        self.flow = NavigationFlow(self.session)

    def send_otp(self,mobile_no):
        try:
            cookies = self.flow.load_home_page(self.base_url)
            res,cookies = self.flow.guestLoginWithOutMob(cookies)

            res,cookies = self.flow.showCityList(cookies)
            cookies = self.extract.setNewCookies(res)

            res = self.flow.selectCity(cookies)

            res = self.flow.serviceList(cookies)
            PoliceCollectionOfFine_url = self.extract.makePoliceCollectionOfFine_url(res)

            res = self.flow.selectPoliceFineUrl(cookies,PoliceCollectionOfFine_url)
            params = self.extract.extractParameterForSendOTP(res,mobile_no)
            res1 = self.flow.sendOTP(cookies,PoliceCollectionOfFine_url,params)
            params,nexttonext_requests = self.extract.extractParameterForVerifyOTP(res,res1,mobile_no)

            return {
                "OTP": "",
                "reg_no": "", 
                "PoliceCollectionOfFine_url": PoliceCollectionOfFine_url,
                "params": params,
                "nexttonext_requests": nexttonext_requests,
                "cookies": cookies
            }
        except:
            traceback.print_exc()
            return {"applications":[]}

    def verify_otp_and_fetch_chalan(self,reg_no,otp,PoliceCollectionOfFine_url,params,nexttonext_requests,cookies):
        try:
            params["OTP"]=otp
            nexttonext_requests["otp"]=otp

            res = self.flow.validateOTP(cookies,PoliceCollectionOfFine_url,params)
            res = self.flow.policeFineDetailsPage(cookies,PoliceCollectionOfFine_url,nexttonext_requests)
            params,Token = self.extract.extractParameterForGetChalan(res,reg_no)

            res = self.flow.getAllChalanDetails(cookies,params,Token)
            data = self.extract.extractFromRes(res)
            return {"applications":data}

        except:
            traceback.print_exc()
            return {"applications":[]}

