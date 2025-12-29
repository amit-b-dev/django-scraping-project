from datetime import datetime
from bs4 import BeautifulSoup
import numpy as np
import os,time,cv2,base64,requests,traceback,hashlib, re
from PIL import Image
from ..util.captchaDecorder import google_ocr
 
 
class CaptchaSolver:
 
    def __init__(self):
        self.captcha_dir = "captcha_image"
        self.captcha_path = os.path.join(self.captcha_dir, "captcha.png")
        os.makedirs(self.captcha_dir, exist_ok=True)

    def solve(self,captcha_res, max_retries=10):
        print("Enter captcha solver function.....")

        for _ in range(1, max_retries + 1):
            try:

                with open(self.captcha_path, "wb") as f:
                    f.write(captcha_res.content)

                with open(self.captcha_path, "rb") as f:
                    base64_image = base64.b64encode(f.read()).decode()

                start_time = datetime.now()
                captcha_text = google_ocr(base64_image).strip()
                print("Total Runtime:", (datetime.now() - start_time).total_seconds())
                return captcha_text,self.captcha_path,self.captcha_dir
 
            except:
                traceback.print_exc()
 
        return False
    
