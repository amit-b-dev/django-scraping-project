from bs4 import BeautifulSoup
from datetime import datetime
import re,json

class Extractor:
    def __init__(self, session):
        self.session = session

    def fetchCaseDetails(self,res):

        soup = BeautifulSoup(res.text,'html.parser')
        soup.find(class_="table-responsive")['class']
        all_tr = soup.find(class_="table-responsive").find_all('tr')

        table_data = []
        for i in range(1,len(all_tr)-1):
                values = [j.get_text(strip=True).replace('Click to View','') for j in all_tr[i].find_all('td')]
                short_file_url = all_tr[i].find_all('td')[-1].find('a')['href']
                complete_file_url = f"https://bombayhighcourt.nic.in/{short_file_url}"
                table_data.append({
                    "CORAM":values[0],
                    "ORDER/JUDGEMENT DATE":values[1],
                    "PAGES":values[2],
                    "UPLOAD DATE":values[3],
                    "File":complete_file_url,
                })
        return table_data