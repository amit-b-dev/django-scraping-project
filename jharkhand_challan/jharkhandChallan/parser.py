from bs4 import BeautifulSoup
from datetime import datetime
import re

class Extractor:
    def __init__(self, session):
        self.session = session
    
    def fetchChallanDetails(self,res):
        try:
            chalan_details=[]
            soup = BeautifulSoup(res.text,"html.parser")
            challan_available = soup.find_all(class_="alert alert-warning")
            if challan_available:
                if "Record not available" in challan_available[0]:
                    chalan_details="No Challan Found"
            
            return chalan_details
        except:
            chalan_details=[]

