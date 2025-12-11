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
 
    def convert_image_back_to_white_bg(self):
        img = Image.open(self.captcha_path)

        if img.mode == 'RGBA':
            # Create white background
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3])  # Paste using alpha channel
        else:
            bg = img.convert("RGB")

        bg.save(self.captcha_path)

    def clean_captcha(self):
        img = cv2.imread(self.captcha_path)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
 
        mask = cv2.inRange(hsv, np.array([20, 80, 80]), np.array([35, 255, 255]))
 
        if cv2.countNonZero(mask) > 60:
            cleaned = cv2.inpaint(img, mask, 3, cv2.INPAINT_NS)
            cv2.imwrite(self.captcha_path, cleaned)
        else:
            cv2.imwrite(self.captcha_path, img)
 
    def solve(self,img_res, max_retries=10):
        print("Enter captcha solver function.....")

        for _ in range(1, max_retries + 1):
            try:
                with open(self.captcha_path, "wb") as f:
                    f.write(img_res.content)
                self.convert_image_back_to_white_bg()
                self.clean_captcha()
 
                with open(self.captcha_path, "rb") as f:
                    base64_image = base64.b64encode(f.read()).decode()
                start_time = datetime.now()
                captcha_text = google_ocr(base64_image).strip()
                print("Total Runtime:", (datetime.now() - start_time).total_seconds())
                return captcha_text,self.captcha_path,self.captcha_dir
 
            except:
                traceback.print_exc()
                pass
 
        return False
    
