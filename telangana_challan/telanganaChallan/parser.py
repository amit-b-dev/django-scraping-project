from bs4 import BeautifulSoup
from datetime import datetime
import re

class Extractor:
    def __init__(self, session):
        self.session = session
    
    def extractChallanDetails(self,res):
        try:
            soup = BeautifulSoup(res.text,"html.parser")
            all_rows = soup.find(id='rtable').find_all('tr')
            tableData = []
            for row in all_rows:

                ths = row.find_all('th')
                if len(ths)==14:
                    cols = [i.get_text(" ",strip=True) for i in ths if i.get("colspan") != "4"]
                    cols.pop()

                tds = row.find_all('td')
                if len(tds)==15:
                    rowData = [i.get_text(" ",strip=True) for i in tds if i.get("colspan") != "4" and i.get_text(" ",strip=True)!="" ]
                    tableData.append(rowData)

            final_data = []
            for row in tableData:
                row_dict = dict(zip(cols, row))
                final_data.append(row_dict)
            
            return final_data
        except:
            return []

