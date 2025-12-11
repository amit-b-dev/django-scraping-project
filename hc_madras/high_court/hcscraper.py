import requests

class hcMadras:
    def __init__(self):
        self.base_url = "https://hcmadras.tn.gov.in/case_status_mas.php"
        self.session = requests.Session()
        self.cookies = {}

        self.base_url = "https://hcmadras.tn.gov.in/case_status_mas.php"
    def init_home(self):
        res = self.session.get(self.base_url)
        