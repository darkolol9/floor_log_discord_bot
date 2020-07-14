import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_rsn(img):
    img = cv2.bitwise_not(img)
    text = pytesseract.image_to_string(img,config='--psm 11')
    print(text)
    return text
