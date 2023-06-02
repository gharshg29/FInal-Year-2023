import cv2
import pytesseract
import easyocr
import imutils
from deepface import DeepFace

pytesseract.pytesseract.tesseract_cmd = r"C:/Users/Kshitij Garg/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"

def capture_image(file_path):
    cam = cv2.VideoCapture(0)
    count = 0
    while True:
        ret, img = cam.read()
        cv2.imshow("Test", img)
        if not ret:
            break
        k = cv2.waitKey(1)
        if k % 256 == 27:
            # For Esc key
            print("Close")
            break
        elif k % 256 == 32:
            # For Space key
            print("Image saved")
            file = file_path + 'p' + str(count) + '.jpg'
            cv2.imwrite(file, img)
            count += 1

    cam.release
    cv2.destroyAllWindows

def process_image(file_path):
    image = cv2.imread(file_path)
    image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 170, 200)
    cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
    NumberPlateCount = None
    for i in cnts:
        perimeter = cv2.arcLength(i, True)
        approx = cv2.approxPolyDP(i, 0.02 * perimeter, True)
        if len(approx) == 4:
            NumberPlateCount = approx
            x, y, w, h = cv2.boundingRect(i)
            crp_img = image[y:y + h, x:x + w]
            cv2.imwrite(file_path, crp_img)
            break

    crop_img_loc = file_path
    text = pytesseract.image_to_string(crop_img_loc, lang='eng')
    if len(text) == 0:
        print("Blurred Image")
        exit()
    else:
        ttext = text.strip()
        res = []
        valid_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 "
        for char in ttext:
            if char in valid_chars:
                res.append(char)
        final_number_plate = "".join(res).strip()
        return final_number_plate

def save_image(vehicleno, status):
    cam = cv2.VideoCapture(0)
    count = 0
    while True:
        ret, img = cam.read()
        cv2.imshow("Test", img)
        if not ret:
            break
        k = cv2.waitKey(1)
        if k % 256 == 27:
            # For Esc key
            print("Close")
            break
        elif k % 256 == 32:
            # For Space key
            print("Image saved")
            file = 'Images/' + str(vehicleno) + str(status) + '.jpg'
            cv2.imwrite(file, img)
            count += 1
        cam.release
        cv2.destroyAllWindows

def match_faces(noplate):
    img1 = cv2.imread('Images/' + str(noplate) + ' entry.jpg')
    img2 = cv2.imread('Images/' + str(noplate) + ' exit.jpg')
    try:
        result = DeepFace.verify(img1, img2, enforce_detection=False)
        if result["verified"] == True:
            text = "The vehicle can go, person is the same"
        else:
            text = "The vehicle can't go, the person is not the same"
        return text
    except:
        print("Something went wrong")

def entry_capture():
    capture_image('NumberPlate/p0.jpg')
    number_plate = process_image('NumberPlate/p0.jpg')
    vehicleno = number_plate
    if number_plate:
        return number_plate

def exit_capture():
    capture_image('NumberPlate/p1.jpg')
    number_plate = process_image('NumberPlate/p1.jpg')
    vehicleno = number_plate
    if number_plate:
        save_image(vehicleno, " exit")
        result = match_faces(number_plate)
        return result
