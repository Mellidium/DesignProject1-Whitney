from tkinter import *
from tkinter import messagebox
import pymysql
import pandas as pd
import TrainedModelTesting
from threading import Thread
from multiprocessing import Queue
import queue


def hide_all():
    btnGP.pack_forget()
    btnB.pack_forget()
    btnL.pack_forget()
    btnTT.pack_forget()
    btnUP.pack_forget()
    btnCL.pack_forget()
    photoLabel.pack_forget()
    usernameEntry.pack_forget()
    passwordEntry.pack_forget()
    userText.pack_forget()
    passText.pack_forget()
    btnCancel.pack_forget()
    btnConfirmLogin.pack_forget()
    btnConfirmCreate.pack_forget()
    btnLogout.pack_forget()
    standard_video.pack_forget()
    hand_video.pack_forget()
    resultLabel.pack_forget()
    btnStartGame.pack_forget()
    btnReset.pack_forget()


def guided_practice():
    hide_all()
    photoLabel.pack()
    btnB.pack()
    standard_video.pack()
    hand_video.pack()
    resultLabel.pack()


def unassisted_practice():
    hide_all()
    btnB.pack()
    standard_video.pack()
    hand_video.pack()
    resultLabel.pack()
    print("Hello2")


def time_trial():
    hide_all()
    btnB.pack()
    standard_video.pack()
    hand_video.pack()
    resultLabel.pack()
    btnStartGame.pack()
    print("Hello3")


def login():
    hide_all()
    userText.pack()
    usernameEntry.pack()
    passText.pack()
    passwordEntry.pack()
    btnConfirmLogin.pack()
    btnCancel.pack()
    print("Login")


def logout():
    if usernameString.get() == "User: Not Logged In":
        messagebox.showinfo("Error!", "No user is currently logged in")
    else:
        messagebox.showinfo("Success!", "%s has been succesfully logged out" % usernameString.get())
        usernameString.set("User: Not Logged In")


def create_account():
    print("Creaet login")
    hide_all()
    userText.pack()
    usernameEntry.pack()
    passText.pack()
    passwordEntry.pack()
    btnConfirmCreate.pack()
    btnCancel.pack()
    print(usernameEntry.get())
    print(passwordEntry.get())


def clear():
    hide_all()
    Tk.update(window)
    btnGP.pack()
    btnUP.pack()
    btnTT.pack()
    btnCL.pack()
    btnL.pack()
    btnLogout.pack()
    standard_video.pack()
    hand_video.pack()
    resultLabel.pack()
    usernameEntry.delete(0, 'end')
    passwordEntry.delete(0, 'end')


def send_login():
    query = "SELECT * FROM logins WHERE username='%s'" % (usernameEntry.get())

    if usernameEntry.get() == "" or passwordEntry.get() == "":
        messagebox.showerror("Error!", "One or more fields is unfilled.")
    else:
        result = pd.read_sql(query, con=conn)
        if result.empty != True:
            if result.get_value(0, col="password") == passwordEntry.get():
                usernameString.set("User: %s" % usernameEntry.get())
                messagebox.showinfo("Success!", "%s has been logged in!" % usernameString.get())
                clear()
            else:
                messagebox.showerror("Error!", "Password is incorrect.")
        else:
            messagebox.showerror("Error!", "No such user exists.")

    #network, check if user is taken or if user exists


def send_create():
    queryInsert = "INSERT INTO logins (username, password) VALUES ('%s', '%s')" % (usernameEntry.get(), passwordEntry.get())
    queryAnalyze = "SELECT * FROM logins WHERE username='%s'" % (usernameEntry.get())
    passTest = passwordEntry.get()

    if usernameEntry.get() == "" or passwordEntry.get() == "":
        messagebox.showerror("Error!", "One or more fields is unfilled.")
    else:
        result = pd.read_sql(queryAnalyze, con=conn)
        if result.empty == True:
            if len(passTest) < 6:
                messagebox.showerror("Error!", "Password must contain at least 6 characters.")
            else:
                cursor = conn.cursor()
                cursor.execute(queryInsert)
                conn.commit()
                cursor.close()
                messagebox.showinfo("Success!", "Account created. Login to your new account from the home page!")
                clear()
        else:
            messagebox.showerror("Error!", "User with that username already exists.")


def refresh_image():
    try:
        frame2 = PhotoImage(file="hand_images/TestFiles/GUI_display.png")
        frame_hand2 = PhotoImage(file="hand_images/TestFiles/bitwise_hand.png")
        standard_video.configure(image=frame2)
        standard_video.image = frame2
        hand_video.configure(image=frame_hand2)
        hand_video.image = frame_hand2
        Tk.update(window)
    except:
        Tk.update(window)
    window.after(1, refresh_image)


def get_data():
    try:
        letter = results.get(False)
        resultLabel.configure(text=("%s" % letter[0]).capitalize())
    except queue.Empty:
        pass
    window.after(500, get_data)


def start_game():
    hide_all()


def reset_frame():
    TrainedModelTesting.reset = True


#connect to sql server first
host="asltranslationdb.cd7r6ezvw3xo.us-east-2.rds.amazonaws.com"
port=3306
dbname="userinfo"
user="admin"
password="tFFQCUO12321"
conn = pymysql.connect(host, user=user,port=port, passwd=password, db=dbname)

window = Tk()
window.state('zoomed')

options = Frame(window)
options.pack(side=RIGHT)
cameras = Frame(window)
cameras.pack(side=LEFT)
information = Frame(window)
information.pack(side=BOTTOM)

#create Queue to get data from threads
results = Queue()

#run the hand gesture recognition
c = Thread(target=TrainedModelTesting.GUIcall, args=(results,))
c.start()
frame = PhotoImage(file="loading.png")
frame_hand = PhotoImage(file="loading.png")
try:
    frame = PhotoImage(file="hand_images/TestFiles/GUI_display.png")
    frame_hand = PhotoImage(file="hand_images/TestFiles/bitwise_hand.png")
except:
    Tk.update(window)
standard_video = Label(cameras, image=frame)
hand_video = Label(cameras, image=frame_hand)
resultLabel = Label(cameras, font=("Calibri", 64), text="Waiting...")


#variables
usernameString = StringVar()
usernameString.set("User: Not Logged In")

#images
chart = PhotoImage(file="asl_chart.png")
photoLabel = Label(options, image=chart)

#logins
userText = Label(text="Username")
passText = Label(text="Password")
loggedInText = Label(window, textvariable=usernameString)
usernameEntry = Entry(window, width=20, bg="white")
passwordEntry = Entry(window, width=20, bg="white", textvariable=password, show="*")
btnCancel = Button(window, text='Cancel', command=clear, width=15, height=1, bg="white")
btnConfirmLogin = Button(window, text='Login', command=send_login, width=15, height=1, bg="white")
btnConfirmCreate = Button(window, text='Create Account', command=send_create, width=15, height=1, bg="white")


#buttons
btnB = Button(options, text='Back', command=clear, width=20, height=3, bg="white")
btnGP = Button(options, text='Guided Practice', command=guided_practice, width = 20, height = 3, bg="white")
btnUP = Button(options, text='Unassisted Practice', command=unassisted_practice, width=20, height=3, bg="white")
btnTT = Button(options, text='Time Trial', command=time_trial, width=20, height=3, bg="white")
btnL = Button(options, text='Login', command=login, width=20, height=3, bg="white")
btnCL = Button(options, text='Create Account', command=create_account, width=20, height=3, bg="white")
btnLogout = Button(options, text='Logout', command=logout, width=20, height=3, bg="white")
btnStartGame = Button(window, text='Start Game!', command=start_game, width=20, height=3, bg="white")
btnReset = Button(options, text='Reset Frame', command=reset_frame, width=20, height=3, bg="white")


btnGP.pack()
btnUP.pack()
btnTT.pack()
btnCL.pack()
btnL.pack()
btnLogout.pack()
btnReset.pack()
loggedInText.pack(side=TOP)
standard_video.pack()
hand_video.pack()
resultLabel.pack()

get_data()
refresh_image()
window.mainloop()