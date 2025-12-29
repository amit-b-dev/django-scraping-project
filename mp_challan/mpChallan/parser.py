from bs4 import BeautifulSoup
from datetime import datetime
import re

class Extractor:
    def __init__(self, session):
        self.session = session
    
    def fetchChallanDetails(self,res):
        try:
            if "No Challan Found" in res.text:
                chalan_details="No Challan Found"
            
            return chalan_details
        except:
            chalan_details=[]
