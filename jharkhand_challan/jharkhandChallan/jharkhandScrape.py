import requests,traceback,re
from .parser import Extractor
from .navigation import NavigationFlow


class JharkhandChallan:
    def __init__(self):
        self.session = requests.Session()
        self.extract = Extractor(self.session)
        self.flow = NavigationFlow(self.session)

    def getChallanDetails(self,vehicle_no):
        try:
            res, cookies = self.flow.loadHomePage()
            res = self.flow.searchChallanDetails(vehicle_no,cookies,res)
            # Extracter function
            chalan_details = self.extract.fetchChallanDetails(res)

            return {"applications":chalan_details}

        except:
            traceback.print_exc()
            return {"applications":[]}



