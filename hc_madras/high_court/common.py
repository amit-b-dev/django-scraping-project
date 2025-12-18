import os

from bs4 import BeautifulSoup
from .headers import HeaderHelper
from .captcha import CaptchaSolver


class CommonFlow:

    def __init__(self, session):
        self.session = session
        self.solver = CaptchaSolver()
    
    def load_home_page(self, url):
        res = self.session.get(url)
        cookies = self.session.cookies.get_dict()
        soup = BeautifulSoup(res.text, "html.parser")
        
        return soup,cookies

    def captcha_solver_and_retry(self, cnr_no, soup, cookies):
        for _ in range(10):
            headers = HeaderHelper.captcha_header()
            captcha_url = "https://hcmadras.tn.gov.in"+soup.find(id='cnr_captcha_img')['src']
            captcha_res = self.session.get(captcha_url, headers=headers,cookies=cookies)

            captcha_text,captcha_path,captcha_dir = self.solver.solve(captcha_res)
            headers,payloads = HeaderHelper.get_details_header(cnr_no,captcha_text)

            url = "https://hcmadras.tn.gov.in/case_status_cnr_result.php"
            res = self.session.post(url, headers=headers,data=payloads, cookies=cookies)

            soup = BeautifulSoup(res.text, "html.parser")
            error_div = soup.find("div", class_="commentform").get_text(strip=True)
            if error_div=='Captcha not matching':
                continue
            if os.path.exists(captcha_path):
                os.remove(captcha_path)
            if os.path.isdir(captcha_dir):
                os.rmdir(captcha_dir)
            break

        return res
