import os
import csv
import cv2
import pandas as pd
import datetime
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import tkinter
from tkinter import *
from tkinter import messagebox
from Capture_Image import takeImages
from Train_Image import TrainImages

# from Recognize import recognize_attendence

root = Tk()
root.geometry('450x690')
root.resizable(width=False, height=False)
root.title("Attendance Monitoring System")
root.configure(bg="SkyBlue1")
fname = StringVar()
rollno = StringVar()
mail = StringVar()


def display():
    global ffname
    ffname = entry1.get()
    print(ffname)

    global roln
    roln = entry3.get()
    print(roln)

    global mmail
    mmail = entry2.get()
    print(mmail)

    sid = str(roln)[-4:]
    print(sid)

    global Lb1
    Lb1 = Listbox(root, height=1, width=11, font=("bold", 12), relief="flat")
    Lb1.insert(1, sid)
    Lb1.place(x=170, y=215)

    takeImages(sid, ffname)

    messagebox.showinfo("Success", "New User Registration Successful!")


def Openfolder():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Attendance")
    os.startfile(path)


def train():
    TrainImages()


def recognize():
    recognize_attendence()


def send_mail():
    mail()


def mail(filename, rec):
    fromaddr = "mlbeproject123@gmail.com"
    toaddr = rec

    # instance of MIMEMultipart 
    msg = MIMEMultipart()

    # storing the senders email address   
    msg['From'] = fromaddr

    # storing the receivers email address  
    msg['To'] = toaddr

    # storing the subject  
    msg['Subject'] = "Attendance Record"

    # string to store the body of the mail 
    body = "This is an auto-generated mail and is a part of the project Face Recognition Based Attendance System. Kindly find the attached attendance record file."

    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent  
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

    attachment = open(path, "rb")

    # instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form 
    p.set_payload((attachment).read())

    # encode into base64 
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg' 
    msg.attach(p)

    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security 
    s.starttls()

    # Authentication 
    s.login(fromaddr, "mlbeproject@123#")

    # Converts the Multipart msg into a string 
    text = msg.as_string()

    # sending the mail 
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session 
    s.quit()

    print("Mail sent!")


# --------------------------------------------------------------------------------------
def recognize_attendence():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    recognizer.read("TrainingImageLabel" + os.sep + "Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("StudentDetails" + os.sep + "StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)

    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])

            if conf < 50:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(
                    ts).strftime('%H:%M:%S')
                aa = df.loc[df['Id'] == Id]['Name'].values
                tt = str(Id) + "-" + aa
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]

            else:
                Id = 'Unknown'
                tt = str(Id)
            if conf > 75:
                noOfFile = len(os.listdir("ImagesUnknown")) + 1
                cv2.imwrite("ImagesUnknown" + os.sep + "Image" + str(noOfFile) +
                            ".jpg", im[y:y + h, x:x + w])
            cv2.putText(im, str(tt), (x, y + h), font, 1, (255, 255, 255), 2)
        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('im', im)
        if cv2.waitKey(1) == ord('q'):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")
    global fileName
    fileName = "Attendance" + os.sep + "Attendance_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
    attendance.to_csv(fileName, index=False)
    cam.release()
    cv2.destroyAllWindows()
    mail(fileName, mmail)
    print("Attendance Successful")


def synopsis():
    syn = Tk()
    syn.geometry('500x500')
    syn.resizable(width=False, height=False)
    syn.title("About")
    syn.configure(bg="SkyBlue1")
    label09 = Label(syn, text="Project Guide", relief="solid", bg="dark blue", fg="white", width=17, font=("bold", 10))
    label09.place(x=20, y=20)


def details():
    top = Tk()
    top.geometry('390x190')
    top.resizable(width=False, height=False)
    top.title("About")
    top.configure(bg="SkyBlue1")
    label07 = Label(top, text="Project Guide", relief="solid", bg="dark blue", fg="white", width=17, font=("bold", 10))
    label07.place(x=20, y=20)
    label08 = Label(top, text="Dr.Sanjay Singh Thakur", relief="solid", bg="dark blue", fg="white", width=20,
                    font=("bold", 10))
    label08.place(x=200, y=20)
    label06 = Label(top, text="Group Members", height=6, relief="solid", bg="dark blue", fg="white", width=15,
                    font=("bold", 12))
    label06.place(x=20, y=50)
    label02 = Label(top, text="1.Sidhant Medar", relief="solid", bg="dark blue", fg="white", width=20,
                    font=("bold", 10))
    label02.place(x=200, y=50)
    label03 = Label(top, text="2.Jayendra Deshmukh", relief="solid", bg="dark blue", fg="white", width=20,
                    font=("bold", 10))
    label03.place(x=200, y=82)
    label04 = Label(top, text="3.Harshal Mahadik", relief="solid", bg="dark blue", fg="white", width=20,
                    font=("bold", 10))
    label04.place(x=200, y=113)
    label05 = Label(top, text="4.Shantanu Ingle", relief="solid", bg="dark blue", fg="white", width=20,
                    font=("bold", 10))
    label05.place(x=200, y=144)


def clear():
    Lb1.delete(0, 'end')
    entry1.delete(0, 'end')
    entry2.delete(0, 'end')
    entry3.delete(0, 'end')


# >>>GUI PART 1
label0 = Label(root, text="New User Registration Form", borderwidth=1, relief="solid", bg="dark blue", fg="white",
               width=25, font=("bold", 20))
label0.place(x=20, y=30)

label1 = Label(root, text="First Name", bg="dark blue", fg="white", width=10, font=("bold", 12))
label1.place(x=20, y=95)
entry1 = Entry(root, width=42, textvar=fname)
entry1.place(x=170, y=95)

label2 = Label(root, text="Email-ID", bg="dark blue", fg="white", width=10, font=("bold", 12))
label2.place(x=20, y=175)
entry2 = Entry(root, width=42, textvar=mail)
entry2.place(x=170, y=175)

label3 = Label(root, text="Roll", bg="dark blue", fg="white", width=10, font=("bold", 12))
label3.place(x=20, y=135)
entry3 = Entry(root, width=42, textvar=rollno)
entry3.place(x=170, y=135)

label3 = Label(root, text="User ID", bg="dark blue", fg="white", width=10, font=("bold", 12))
label3.place(x=20, y=215)

label4 = Label(root, text="-------------------------------------------------------", bg="SkyBlue1", fg="dark blue",
               font=("bold", 20)).place(x=0, y=330)
##270 pe notification
button1 = Button(root, text='Submit', borderwidth=2, width=10, font=("bold", 12), fg="dark blue",
                 command=display).place(x=90, y=305)

button2 = Button(root, text='Send Mail', borderwidth=2, width=10, font=("bold", 12), fg="dark blue",
                 command=mail).place(x=250, y=305)

##>>GUI PART 2
label01 = Label(root, text="Recognition Portal", borderwidth=1, relief="solid", bg="dark blue", fg="white", width=20,
                font=("bold", 20))
label01.place(x=60, y=370)

button3 = Button(root, text='Recognize', height=3, width=15, fg="dark blue", font=("bold", 16),
                 command=recognize).place(x=120, y=430)

button5 = Button(root, text='Train', width=20, fg="dark blue", font=("bold", 14), command=train).place(x=100, y=540)

button6 = Button(root, text='Attendance Records', width=20, fg="dark blue", font=("bold", 14),
                 command=Openfolder).place(x=100, y=590)

##>>GUI PART 0
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="About", menu=filemenu)
filemenu.add_command(label="Synopsis", command=synopsis)
filemenu.add_separator()
filemenu.add_command(label="Group Members", command=details)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.destroy)
root.config(menu=menubar)

root.mainloop()
