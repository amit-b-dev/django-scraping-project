from datetime import datetime
from bs4 import BeautifulSoup
import numpy as np
import os,time,cv2,base64,requests,traceback
from PIL import Image
from ..util.captchaDecorder import google_ocr
 
 
class CaptchaSolver:
 
    def __init__(self):
        self.captcha_dir = "captcha_image"
        self.captcha_path = os.path.join(self.captcha_dir, "captcha.png")
        os.makedirs(self.captcha_dir, exist_ok=True)
 
    def solve(self,captcha_res, max_retries=10):
        print("Enter captcha solver function.....")

        try:
            base64_image = base64.b64encode(captcha_res.content).decode()
            start_time = datetime.now()
            captcha_text = google_ocr(base64_image).strip()
            print("Total Runtime:", (datetime.now() - start_time).total_seconds())
            return captcha_text,self.captcha_path,self.captcha_dir
 
        except:
            traceback.print_exc()
            pass
 
        return False
    
