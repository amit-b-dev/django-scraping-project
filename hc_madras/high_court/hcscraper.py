import requests,traceback
from .parser import Extractor
from .code_flow import CodeFlow

class hcMadras:
    def __init__(self):
        self.base_url = "https://hcmadras.tn.gov.in/case_status_mas.php"
        self.session = requests.Session()
        self.flow = CodeFlow(self.session)
        self.extract = Extractor(self.session)


    def cnr_no_wise_data(self,cnr_no):
        try:
            print('The Script is Running......')
            soup,cookies = self.flow.load_home_page(self.base_url)
            res = self.flow.captcha_solver_and_retry(cnr_no,soup,cookies)
            all_tables = self.extract.extract_all_tables(res,cookies)

            return {"applications":all_tables}
        except:
            traceback.print_exc()
            return {"applications":[]}

