from bs4 import BeautifulSoup
from datetime import datetime

class Extractor:
    def __init__(self, session):
        self.session = session

    # def get_all_transacton_rows(self, soup11,upd_s_no=0):
    #     all_tr = soup11.find(id='tabView:tableTax_data').find_all('tr')
    #     return all_tr
    
    def extract_receipt_button_for_timeline(self, soup11,upd_s_no=0):
        all_tr = soup11.find(id='tabView:tableTax_data').find_all('tr')
        dynamic_id = all_tr[upd_s_no].find('button')['id']
        trans_id = all_tr[upd_s_no].find_all('td')[3].text
        return dynamic_id, trans_id,all_tr

    def extract_receipt_button(self, all_tr_for_s_no,upd_s_no=0):
        dynamic_id = all_tr_for_s_no[upd_s_no].find('button')['id']
        trans_id = all_tr_for_s_no[upd_s_no].find_all('td')[3].text
        return dynamic_id, trans_id
    

    def get_all_transaction_data(self, all_pages_soup):
        transactions = []
        all_tr_for_s_no = []

        for soup in all_pages_soup:
            all_tr = soup.find_all('tr')

            if len(all_tr) == 16:
                all_tr.pop(0)

            for tr in all_tr:
                all_tr_for_s_no.append(tr)
                tds = tr.find_all("td")

                if len(tds) < 7:
                    continue

                trans_date_str = tds[5].text.strip()

                transaction = {
                    "Sl No": tds[0].text.strip(),
                    "Regn No": tds[1].text.strip(),
                    "Trans Desc": tds[2].text.strip(),
                    "Trans ID": tds[3].text.strip(),
                    "Trans Amt": tds[4].text.strip(),
                    "Trans Date": trans_date_str,
                    "Status": tds[6].text.strip(),
                    # helper field for sorting
                    "_trans_date_obj": datetime.strptime(
                        trans_date_str, "%d-%b-%Y"
                    )
                }

                if "Transfer of Ownership" in transaction["Trans Desc"]:
                    transaction["CMV form_29"] = "available"
                else:
                    transaction["CMV form_29"] = "not available"

                transactions.append(transaction)

        transactions.sort(
            key=lambda x: x["_trans_date_obj"],
            reverse=True
        )

        # Remove helper key
        for t in transactions:
            t.pop("_trans_date_obj", None)

        return transactions, all_tr_for_s_no

    # def get_all_transaction_data(self, all_pages_soup):
    #     transactions=[]
    #     all_tr_for_s_no=[]
    #     for soup in all_pages_soup:
    #         all_tr = soup.find_all('tr')
    #         if len(all_tr)==16:
    #             all_tr.pop(0)
    #         for tr in all_tr:
    #             all_tr_for_s_no.append(tr)
    #             tds = tr.find_all("td")
    #             if len(tds) < 7:
    #                 continue

    #             transaction = {
    #                 "Sl No": tds[0].text.strip(),
    #                 "Regn No": tds[1].text.strip(),
    #                 "Trans Desc": tds[2].text.strip(),
    #                 "Trans ID": tds[3].text.strip(),
    #                 "Trans Amt": tds[4].text.strip(),
    #                 "Trans Date": tds[5].text.strip(),
    #                 "Status": tds[6].text.strip()
    #             }
    #             if transaction["Trans Desc"]=="Transfer of Ownership" or "Transfer of Ownership" in transaction["Trans Desc"]:
    #                 transaction["CMV form_29"] = "available"
    #             else:
    #                 transaction["CMV form_29"] = "not available"
    #             transactions.append(transaction)
                
    #     return transactions,all_tr_for_s_no

    def get_all_transaction_data1(self, all_pages_soup):
        transactions=[]
        all_tr_for_s_no=[]
        s_no_for_form_29=[]
        for soup in all_pages_soup:
            all_tr = soup.find_all('tr')
            if len(all_tr)==16:
                all_tr.pop(0)
            for tr in all_tr:
                all_tr_for_s_no.append(tr)
                tds = tr.find_all("td")
                if len(tds) < 7:
                    continue

                transaction = {
                    "Sl No": tds[0].text.strip(),
                    "Regn No": tds[1].text.strip(),
                    "Trans Desc": tds[2].text.strip(),
                    "Trans ID": tds[3].text.strip(),
                    "Trans Amt": tds[4].text.strip(),
                    "Trans Date": tds[5].text.strip(),
                    "Status": tds[6].text.strip()
                }
                if transaction["Trans Desc"]=="Transfer of Ownership" or "Transfer of Ownership" in transaction["Trans Desc"]:
                    transaction["CMV form_29"] = "available"
                    s_no_for_form_29.append(transaction["Sl No"])
                else:
                    transaction["CMV form_29"] = "not available"
                transactions.append(transaction)
                
        return s_no_for_form_29,all_tr_for_s_no

    def extract_form_29_button(self, soup12):
        
        form_29_exists_or_not = form_29_btn_id = None
        view_state = soup12.find("input", {"id": "j_id1:javax.faces.ViewState:0"})["value"]
        
        try:
            form_29_btn_id = soup12.find_all(class_='ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only display-none')[2]['id']
            if soup12.find_all(class_='ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only display-none')[2].get_text(strip=True)!="Print CMV form_29":
                form_29_exists_or_not = "form 29 is not available"
        except IndexError:
            form_29_exists_or_not = "form 29 is not available"
        
        return form_29_btn_id, view_state,form_29_exists_or_not

    def print_receipt_data(self, soup12):

        table = soup12.find("table", class_="datatable-panel feeRecieptPrintReport bottom-space")
        rows = table.find_all("tr")

        table_data = {}
        for tr in rows:
            tds = tr.find_all("td")
            if len(tds) >= 2:
                label = tds[0].get_text(strip=True).replace(":", "")
                value = tds[1].get_text(strip=True)
                table_data[label] = value
                
            if len(tds) >= 4:
                label2 = tds[2].get_text(strip=True).replace(":", "")
                value2 = tds[3].get_text(strip=True)
                table_data[label2] = value2
        return table_data

    def safe_get(lst, idx):
        return lst[idx] if len(lst) > idx else ""

    def extract_form29(self,soup):

        b = [tag.get_text(strip=True).replace("\xa0", " ") for tag in soup.find_all("b")]
        try:combined_date = datetime.strptime(f"{b[2]} {b[3]} {b[4]}", "%d %b %Y").strftime("%Y-%m-%d")
        except:combined_date=""
        return {
            "seller_name":      Extractor.safe_get(b, 0),
            "seller_address":   Extractor.safe_get(b, 1),
            "sold_date":        combined_date,
            "vehicle_number":   Extractor.safe_get(b, 5),
            "maker":            Extractor.safe_get(b, 6),
            "chassis_number":   Extractor.safe_get(b, 7),
            "engine_number":    Extractor.safe_get(b, 8),
            "buyer_name":       Extractor.safe_get(b, 9),
            "buyer_parent":     Extractor.safe_get(b, 10),
            "buyer_address":    Extractor.safe_get(b, 11)
        }
    
    def get_Newest_Form29(self,transactions):
        try:
            for tr in transactions:
                if "Transfer of Ownership" in tr["Trans Desc"]:
                    s_no = int(tr["Sl No"])
                    return s_no
            return None
        except:
            return None

