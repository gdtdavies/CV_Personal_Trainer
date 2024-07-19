import cv2
import cvzone
import numpy as np
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
from tkinter import *
from datetime import datetime

root = Tk()
root.title("Eye Blink Application")
dimension = 400
root.minsize(dimension, dimension)  # width, height
root.maxsize(dimension, dimension)
root.configure(background="darkgreen")
root.geometry("400x400+50+50")

color1 = "#307D7E"
logo_frame = Frame(root, bg=color1)
logo_frame.pack()
lblTitle = Label(logo_frame, text="Eye Blink Detection App", bg=color1, fg='white', relief=RAISED)
lblTitle.pack(side="left")
# Change font and size of label
lblTitle.config(font=("Font", 24))
# image1 = PhotoImage(file="logo1.gif")
# img1 = image1.subsample(3, 3)
# lblLogo1 = Label(logo_frame, image=img1, bg="white", relief=SUNKEN).pack(side="right")

color2 = "#31906E"
entry_name = Frame(root, bg=color2)
entry_name.pack()
Label(entry_name, text="Name:", bg=color2).pack(side="left", padx=5)
entry_name = Entry(entry_name, bd=3)
entry_name.pack(side='right')

entry_age = Frame(root, bg=color2)
entry_age.pack()
Label(entry_age, text="Age:", bg=color2).pack(side="left", padx=5, pady=3)
entry_age = Entry(entry_age, bd=3)
entry_age.pack(side='right')

entry_sex = Frame(root, bg=color2)
entry_sex.pack()
Label(entry_sex, text="Sex:", bg=color2).pack(side="left", padx=5, pady=3)
entry_sex = Entry(entry_sex, bd=3)
entry_sex.pack(side='right')

entry_threshold = Frame(root, bg=color2)
entry_threshold.pack()
Label(entry_threshold, text="Threshold:", bg=color2).pack(side="left", padx=5, pady=3)
entry_threshold = Entry(entry_threshold, bd=3)
entry_threshold.pack(side='right')

cap = cv2.VideoCapture(0)
start_time = None
blink_counter = 0
last_blink_state = False

def startRecord():
    global start_time, blink_counter, cooldown, last_blink_time, entry_name, entry_age, entry_sex
    print("Recording has been started")
    start_time = datetime.now()
    blink_counter = 0
    cap=cv2.VideoCapture(0)
    detector = FaceMeshDetector(maxFaces=1)
    plotY = LivePlot(640,360,[25,50])

    idList = [22,23,24,26,110,157,158,159,160,161,130,243]
    ratioList=[]
    blinkThres = float(entry_threshold.get()) if entry_threshold.get() else 35

    blinkCounter=0
    counter=0

    color = (255,0,255)
    

    while True:
        success,img = cap.read()
        #img = cv2.resize(img,(640,360))
        img, faces = detector.findFaceMesh(img,draw=False)
        if faces:
            face = faces[0]
            for id in idList:
                cv2.circle(img,face[id],5,color,cv2.FILLED)

            leftUp=face[159]
            leftDown=face[23]

            leftEyeLeftCorner=face[130]
            leftEyeRightCorner=face[243]

            lengthVer,_=detector.findDistance(leftUp, leftDown)
            lengthHor,_=detector.findDistance(leftEyeLeftCorner, leftEyeRightCorner)

            cv2.line(img,leftUp,leftDown,(0,200,0),3)
            cv2.line(img,leftEyeLeftCorner,leftEyeRightCorner,(0,200,0),3)

            ratio =int(100*(lengthVer/lengthHor))
            ratioList.append(ratio)
            avgThres=3
            if len(ratioList)>avgThres:
                ratioList.pop(0)
            ratioAvg=sum(ratioList)/len(ratioList)

            if ratioAvg < blinkThres and counter ==0:
                blinkCounter +=1
                color=(0,200,0)
                counter=1

            if counter !=0:
                counter +=1
                if counter >10:
                    counter=0
                    color=(255,0,255)

            cvzone.putTextRect(img,f'Blink Count: {blinkCounter}',(50,100),colorR=color)
            imgPlot=plotY.update(ratioAvg,color)
            img=cv2.resize(img,(640,360))
            imgStack=cvzone.stackImages([img,imgPlot],2,1)
            cv2.imshow("Image", imgStack)
        else:
            img = cv2.resize(img,(640,360))
            imgStack = cvzone.stackImages([img,img],2,1)

        key=cv2.waitKey(25)
        if key == 27:
            break


entry_name.bind("<KeyRelease>", lambda event: enable_start_button())
entry_age.bind("<KeyRelease>", lambda event: enable_start_button())
entry_sex.bind("<KeyRelease>", lambda event: enable_start_button())
entry_threshold.bind("<KeyRelease>", lambda event: enable_start_button())

def enable_start_button(event=None):
    if entry_name.get() and entry_age.get() and entry_sex.get() and entry_threshold.get():
        btnStart.config(state=NORMAL)
    else:
        btnStart.config(state=DISABLED)
        
def writeData(entry_name, entry_age, entry_sex):
    global start_time, blink_counter, last_blink_time, file_handle
    while True:
        duration = datetime.now() - start_time if start_time else None
        if duration:
            duration_str = str(duration)
            duration_str = duration_str.split('.')[0]
        else:
            duration_str = "Recording not started"
        bpm = blink_counter / ((datetime.now() - last_blink_time).total_seconds() / 60) if last_blink_time else None
        if bpm:
            file_handle.seek(0)
            file_handle.write(f"DateTime: {datetime.now()}, Duration: {duration_str}, Number of Blinks: {blink_counter}, Blinks per Minute: {bpm}, Name: {entry_name}, Age: {entry_age}, Sex: {entry_sex}\n")
            file_handle.truncate()
        time.sleep(1)  # Update data every second

btnStart = Button(root, text="Start", command=startRecord, state=DISABLED)
btnStart.pack(side="left", padx=5)
btnWrite = Button(root, text="Write Data", command=writeData)
btnWrite.pack(side="left", padx=5)

root.mainloop()

cap.release()
cv2.destroyAllWindows()