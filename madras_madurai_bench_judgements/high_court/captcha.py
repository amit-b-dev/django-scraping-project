from datetime import datetime
from bs4 import BeautifulSoup
import numpy as np
import os,time,cv2,base64,requests,traceback
from PIL import Image
from ..util.captchaDecorder import google_ocr
 
 
class CaptchaSolver:
 
    def __init__(self):
        pass
 
    def solve(self,captcha_res, max_retries=10):
        print("Enter captcha solver function.....")

        for _ in range(1, max_retries + 1):
            try:
                base64_image = base64.b64encode(captcha_res.content).decode()
                start_time = datetime.now()
                captcha_text = google_ocr(base64_image).strip()
                print("Total Runtime:", (datetime.now() - start_time).total_seconds())
                return captcha_text
 
            except:
                traceback.print_exc()
                pass
 
        return False
    
