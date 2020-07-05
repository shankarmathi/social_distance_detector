from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2
import smtplib
import time
import threading
from playsound import playsound
from gtts import gTTS 

port = 465  # For SSL
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls() 
#provide ur login here 
message = "Covid pandamic is Outbreaking.Please Maintain social distancing."
language = 'en'
myobj = gTTS(text=message, lang=language, slow=False) 
myobj.save("welcome.mp3") 
shankarobj = gTTS(text="The Door is opened", lang=language, slow=False)
shankarobj.save("open.mp3") 
shobj = gTTS(text="The Door is closed", lang=language, slow=False)
shobj.save("close.mp3") 

def process():
	count=0
	global s
	while(True):
		global subjects
		print(subjects)
		if (len(subjects) >= 2):
			count+=1
			if count>=5 and count <=7:
				playsound('welcome.mp3')
			elif count>7:
				a=100
				b= id(100)
				#provide ur mail id here	
		else:
			count = 0
		key = cv2.waitKey(1) & 0xFF
		if key == ord("w"):
			break
		time.sleep(2)

def eye_aspect_ratio(eye):
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear
def main():	
	global subjects
	thresh = 0.25
	frame_check = 20
	detect = dlib.get_frontal_face_detector()
	predict = dlib.shape_predictor("C://Users//Welcome//Downloads//shape_predictor_68_face_landmarks.dat")

	(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
	(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
	cap=cv2.VideoCapture(0)
	flag=0
	prev= time.localtime(time.time())
	while True:
		ret, frame=cap.read()
		frame = imutils.resize(frame, width=450)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		subjects = detect(gray, 0)
		#print("NO Of Persons " + str(len(subjects)))
		for subject in subjects:
			shape = predict(gray, subject)
			shape = face_utils.shape_to_np(shape)#converting to NumPy Array
			leftEye = shape[lStart:lEnd]
			rightEye = shape[rStart:rEnd]
			leftEAR = eye_aspect_ratio(leftEye)
			rightEAR = eye_aspect_ratio(rightEye)
			ear = (leftEAR + rightEAR) / 2.0
			leftEyeHull = cv2.convexHull(leftEye)
			rightEyeHull = cv2.convexHull(rightEye)
			cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
			cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			exit()
	cv2.destroyAllWindows()
	cap.stop()
def close():
	f=0
	
	while(True):
		global subjects
		if len(subjects)>=2:
			if f==1:
				playsound('close.mp3')
				print("Door closed")
				f=0
		else:
			if  f==0:
				playsound('open.mp3')
				print("Door opened")
				f=1
		time.sleep(2)


t1 = threading.Thread(target=main, name='t1') 
t2 = threading.Thread(target=process, name='t2')
t3 = threading.Thread(target=close, name='t3')
subjects =[]
t1.start() 
n = input("Enter open or close").strip()
if n.lower() == "close":
	t3.start()
	t1.join()
	t3.join()
elif n.lower() == "open":
	t2.start()
	t1.join()
	t2.join()
else:
        print("INVALID INPUT")
        exit()
