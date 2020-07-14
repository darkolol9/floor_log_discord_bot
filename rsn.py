import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_rsn(img):
    img = cv2.bitwise_not(img)
    img = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    scale_percent = 300 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    text = pytesseract.image_to_string(resized,config='--psm 6 ')
    #print(text)
    return text


