
import cv2
import pytesseract
import easyocr
import imutils
from deepface import DeepFace
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

pytesseract.pytesseract.tesseract_cmd = r"C:/Users/Kshitij Garg/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"
vehicleno=0
def show_instructions():
    instructions = [
        "1. Click the 'Capture Entry Image' button to capture the entry image.",
        "2. The captured image will be displayed in a new window.",
        "3. Press the spacebar to capture the image.",
        "4. After capturing the image, the number plate will be processed and displayed below.",
        "5. Optionally, capture the driver's image by clicking 'Capture Driver Image (Exit)'.",
        "6. The captured number plates will be compared to verify if the person is the same.",
        "7. The result will be printed in the console window.",
    ]
    instruction_text = "\n".join(instructions)
    instructions_label.config(text=instruction_text)

def capture_image():
    cam = cv2.VideoCapture(0)
    count = 0
    while True:
        ret, img = cam.read()
        cv2.imshow("Test", img)
        if not ret:
            break
        k=cv2.waitKey(1)
        if k%256==27:
            #For Esc key
            print("Close")
            break
        elif k%256==32:
            #For Space key
            print("Image saved")
            file='./NumberPlate/p'+str(count)+'.jpg'
            cv2.imwrite(file, img)
            count +=1

        cam.release
        cv2.destroyAllWindows

def process_image():
    pytesseract.pytesseract.tesseract_cmd=r"C:/Users/Kshitij Garg/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"
    image=cv2.imread('./NumberPlate/p0.jpg')
    image=imutils.resize(image,width=500)
    # cv2.imshow("Original Image",image)
    # cv2.waitKey(0)    
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Gray Image",gray)
    # cv2.waitKey(0)
    
    gray=cv2.bilateralFilter(gray, 11, 17, 17)
    # cv2.imshow("Smooth Image",gray)
    # cv2.waitKey(0)
    
    edged = cv2.Canny(gray, 170, 200)
    # cv2.imshow("Edged Image",edged)
    # cv2.waitKey(0)
    
    cnts , new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    image1=image.copy()
    cv2.drawContours(image1,cnts,-1,(0,255,0),3)
    # cv2.imshow("Contoured Image",image1)
    # cv2.waitKey(0)
    
    cnts=sorted(cnts,key=cv2.contourArea, reverse=True)[:30]
    NumberPlateCount=None
    image2=image.copy()
    cv2.drawContours(image2,cnts,-1,(0,255,0),3)
    # cv2.imshow("Top 30 Contoured",image2)
    # cv2.waitKey(0)
    
    count=0
    name=1
    for i in cnts:
        perimeter=cv2.arcLength(i,True)
        approx=cv2.approxPolyDP(i,0.02*perimeter,True)
        if(len(approx)==4):
            NumberPlateCount=approx
            x,y,w,h=cv2.boundingRect(i)
            crp_img=image[y:y+h,x:x+w]
            cv2.imwrite(str(name)+'.png',crp_img)
            name+=1
            break
    cv2.drawContours(image,[NumberPlateCount],-1,(0,255,0),3)
    # cv2.imshow("Final Image",image)
    # cv2.waitKey(0)
    
    crop_img_loc='1.png'
    text=pytesseract.image_to_string(crop_img_loc,lang='eng')
    if len(text)==0:
        print("Blurr Image Capture Again")
    else:
        ttext=text.strip()
        res=[]
        es="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 "
        for i in ttext:
            if i in es:
                res.append(i)
        ans="".join(res)
        finalnoplate=ans.strip()
        return ans    
def save_image(vehicleno,status):
    cam = cv2.VideoCapture(0)
    count = 0
    while True:
        ret, img = cam.read()
        cv2.imshow("Test", img)
        if not ret:
            break
        k=cv2.waitKey(1)
        if k%256==27:
            #For Esc key
            print("Close")
            break
        elif k%256==32:
            #For Space key
            print("Image saved")
            file='./Images/'+str(vehicleno)+str(status)+'.jpg'
            cv2.imwrite(file, img)
            count +=1
        cam.release
        cv2.destroyAllWindows


def match_faces(noplate):
    img1 = cv2.imread('./Images/'+str(noplate)+' entry'+'.jpg')
    img2 = cv2.imread('./Images/'+str(noplate)+' exit'+'.jpg')
    text=""
    try:
        result=DeepFace.verify(img1,img2,enforce_detection=False)
        if result["verified"]==True:
            text="The Vehicle can go , person is same"
            exit_number_plate_label.config(text="Status:  " + text)
        else:
            text="The Vehicle can't go ,the person is not same"
            exit_number_plate_label.config(text="Status:  " + text)
    except:
        print("Something Went wrong")

def Entry_capture():
    capture_image()
    number_plate = process_image()
    vehicleno=number_plate
    if number_plate:
        entry_number_plate_label.config(text="Number Plate: " + number_plate)
        save_image(vehicleno," entry")

def Exit_capture():
    capture_image()
    number_plate = process_image()
    vehicleno=number_plate
    if number_plate:
        save_image(vehicleno," exit")
        match_faces(number_plate)

root = tk.Tk()
root.title("Vehicle Administration and Theft Control")

canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

instructions_label = tk.Label(scrollable_frame, text="")
instructions_label.pack(pady=10,padx=10)

entry_button = tk.Button(scrollable_frame, text="At Entry", command=Entry_capture)
entry_button.pack(pady=10)

entry_number_plate_label = tk.Label(scrollable_frame, text="Number Plate: ")
entry_number_plate_label.pack()


exit_button = tk.Button(scrollable_frame, text="At Exit", command=Exit_capture)
exit_button.pack(pady=10)

exit_number_plate_label = tk.Label(scrollable_frame, text="Status: ")
exit_number_plate_label.pack()


show_instructions()
root.mainloop()