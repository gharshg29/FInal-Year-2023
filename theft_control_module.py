import cv2 
from matplotlib import pyplot as plt
import numpy as np
import imutils
import pytesseract
import easyocr
from deepface import DeepFace
def noplatecap():
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
	        file='C:/Users/hp/OneDrive - ABES/Desktop/Final Year Project/NumberPlate/p'+str(count)+'.jpg'
	        cv2.imwrite(file, img)
	        count +=1

	    cam.release
	    cv2.destroyAllWindows
def imgtotext():
	pytesseract.pytesseract.tesseract_cmd=r"C:/Program Files/Tesseract-OCR/tesseract.exe"
	image=cv2.imread('C:/Users/hp/OneDrive - ABES/Desktop/Final Year Project/NumberPlate/p0.jpg')
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
		print("Blurr Image")
		exit()
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
	
def facesaving(vehicleno,status):
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
	        file='C:/Users/hp/OneDrive - ABES/Desktop/Final Year Project/Images/'+str(vehicleno)+str(status)+'.jpg'
	        cv2.imwrite(file, img)
	        count +=1
	    cam.release
	    cv2.destroyAllWindows
def facematch(noplate):
	img1 = cv2.imread('C:/Users/hp/OneDrive - ABES/Desktop/Final Year Project/Images/'+str(noplate)+' entry'+'.jpg')
	img2 = cv2.imread('C:/Users/hp/OneDrive - ABES/Desktop/Final Year Project/Images/'+str(noplate)+' exit'+'.jpg')
	try:
		result=DeepFace.verify(img1,img2,enforce_detection=False)
		if result["verified"]==True:
			print("The Vehicle can go , person is same")
		else:
			print("The Vehicle can't go ,the person is not same")
	except:
		print("Something Went wrong")

print("Enter 1 for entry and 2 for exit")
n=int(input())
if n==1:
	noplatecap()
	vehicleno_entry=imgtotext()
	facesaving(vehicleno_entry," entry")
	print("vehicleno and face saved at entry")
if n==2:
	noplatecap()
	vehicleno_exit=imgtotext()
	facesaving(vehicleno_exit," exit")
	print("vehicleno and face saved at exit")
	facematch(vehicleno_exit)